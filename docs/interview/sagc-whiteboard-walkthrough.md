# Whiteboard Walkthrough: Serverless Agentic Governance Controller

**Visual Asset:** `![SAGC Architecture](../../assets/whiteboard.jpg)`

## The Hook (Setting the Stage)
*"Right now, autonomous AI agents are a massive financial liability. If an AI agent hallucinates an infinite loop, it can burn thousands of dollars in an hour calling an LLM. I designed a Serverless Agentic Governance Controller to act as a fail-closed circuit breaker. It treats token spend exactly like a real-time banking transaction."*

## Phase 1: The Control Flow (Tracing the Purple Line)
1. **The Request Hook:** *"When an agent fires a prompt, it cannot go directly to Vertex AI or OpenAI. It is forced through our internal API Gateway. This prevents shadow IT and ensures no hardcoded API keys exist in the wild."*
2. **Pre-Flight Check:** *"The Gateway pauses the request and queries our Vercel Governance Controller. It asks one question: 'Does this specific agent have sufficient budget?'"*
3. **The Flex (Fail-Closed):** *"If our cache lookup times out, the system strictly fails closed. The request is denied. We prioritize fiscal safety over availability."*

## Phase 2: The Settlement (Tracing the Dashed Line)
4. **Execution:** *"If authorized, the request hits the LLM. The Gateway intercepts the response and extracts the exact token usage from the headers."*
5. **The Flex (Atomic Decrement):** *"The Gateway fires an async webhook to Vercel to settle the bill. A common mistake here is using a standard GET/SET loop, which causes race conditions if 50 agents run concurrently. Instead, I pushed the settlement logic directly into Upstash Redis using a custom Lua script. This guarantees mathematical atomicity for every token decrement, while the REST interface ensures we never exhaust the database connection pool during serverless cold starts."*