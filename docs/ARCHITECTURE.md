# Architecture: Serverless Agentic Governance Controller

## 📖 Overview
The Serverless Agentic Governance Controller acts as a fail-closed circuit breaker for autonomous AI workloads. It intercepts LLM API requests, enforces real-time fiscal guardrails, and prevents runaway cloud token spend through atomic budget decrements.

## 🏗️ System Components

1. **The Workload (AI Agents):** Python or Node.js autonomous agents generating dynamic prompts.
2. **The Control Plane (API Gateway):** The internal enforcement point. Handles authentication, rate limiting, and routes all authorized traffic.
3. **The Governance Controller (Vercel):** Serverless edge functions executing business logic and policy enforcement.
4. **The Atomic State Store (Upstash / Serverless Redis):** A low-latency caching layer operating over REST to prevent serverless connection pool exhaustion.
5. **The Data Plane (Vertex AI / OpenAI):** The upstream LLM providers.

## 🚦 Request Flow & Settlement Lifecycle

1. **The Request Hook:** An AI agent fires a prompt. It is forced through the internal API Gateway to prevent shadow IT.
2. **Pre-Flight Check (Fail-Closed):** The Gateway queries the Vercel Governance Controller. 
   * *State Check:* Does this specific agent have sufficient budget? 
   * *Guardrail:* If the Redis lookup times out or fails, the system strictly **fails closed** and denies the request. Fiscal safety supersedes availability.
3. **The Execution:** Authorized requests are securely routed to the LLM provider.
4. **The Settlement (Async Webhook):** The Gateway intercepts the LLM response, extracts the exact token usage from the response headers, and fires an asynchronous webhook back to the Governance Controller.
5. **Atomic Decrement:** The Governance Controller updates the agent's budget in Redis using an atomic transaction, eliminating race conditions even when 50+ concurrent agent threads execute simultaneously.

## 🛡️ Key Architectural Decisions (ADRs)

* **Serverless Redis over TCP Redis:** Elected to use Upstash (REST-based Redis) over standard TCP Redis to eliminate connection pool exhaustion during massive parallel Vercel function invocations.
* **Fail-Closed Posture:** The system intentionally degrades gracefully by blocking AI requests during governance outages, protecting the core business P&L from infinite-loop hallucinations.