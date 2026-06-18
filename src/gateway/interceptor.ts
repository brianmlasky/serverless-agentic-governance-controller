// src/gateway/interceptor.ts
import fetch from 'node-fetch'; // Or native fetch in Node 18+

/**
 * Principal Flex: The AI Proxy Interceptor
 * * This middleware sits between the internal AI workloads and the external LLM providers.
 * It enforces fail-closed pre-flight budget checks and handles asynchronous token settlement.
 */
export async function aiGatewayInterceptor(req, res) {
    // 1. Extract identity from the internal workload
    const agentId = req.headers['x-internal-agent-id'];
    const llmPayload = req.body;

    if (!agentId) {
        return res.status(401).json({ error: "Missing x-internal-agent-id header." });
    }

    // ==========================================
    // STEP 1: PRE-FLIGHT CHECK (Fail-Closed)
    // ==========================================
    try {
        // We set a strict 1000ms timeout. If Vercel/Redis is down, we fail closed.
        const authCheck = await fetch(`https://your-sagc-endpoint.vercel.app/api/budget/check?agentId=${agentId}`, {
            signal: AbortSignal.timeout(1000)
        });
        
        if (!authCheck.ok) {
            // 402 Payment Required is the mathematically correct HTTP status for empty budgets
            return res.status(402).json({ error: "Governance Guardrail: Insufficient Token Budget." });
        }
    } catch (error) {
        // Catch network timeouts or controller downtime
        console.error(`[Guardrail] Pre-flight check failed/timed out for ${agentId}`);
        return res.status(403).json({ error: "Governance Guardrail: Controller Unreachable. Failsafe activated." });
    }

    // ==========================================
    // STEP 2: EXECUTION (Route to LLM)
    // ==========================================
    // Notice: The workload NEVER sees the OpenAI API key. We inject it here.
    const startTime = Date.now();
    const llmResponse = await fetch('https://api.openai.com/v1/chat/completions', {
        method: 'POST',
        headers: { 
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${process.env.OPENAI_API_KEY}` 
        },
        body: JSON.stringify(llmPayload)
    });
    
    const responseData = await llmResponse.json();
    const latency = Date.now() - startTime;

    // ==========================================
    // STEP 3: THE SETTLEMENT (Async Webhook)
    // ==========================================
    // Extract exact token usage from the OpenAI response payload
    const tokensUsed = responseData.usage?.total_tokens || 0;
    
    if (tokensUsed > 0) {
        // THE FLEX: Fire-and-Forget. 
        // We DO NOT `await` this fetch. We do not block the client from receiving its response.
        fetch('https://your-sagc-endpoint.vercel.app/api/budget/settle', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ agentId, tokensUsed })
        }).catch(err => {
            // If the settlement fails, log it to a dead-letter queue for reconciliation
            console.error(`[Reconciliation Required] Settlement failed for ${agentId}:`, err);
        });
    }

    // ==========================================
    // STEP 4: RETURN TO WORKLOAD
    // ==========================================
    // Append governance telemetry to the headers for the requesting agent's observability
    res.setHeader('x-sagc-tokens-consumed', tokensUsed);
    res.setHeader('x-sagc-llm-latency-ms', latency);
    
    return res.status(200).json(responseData);
}