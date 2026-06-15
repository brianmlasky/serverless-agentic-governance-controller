# Whiteboard View 1: The Critical Path

**Purpose:** To visually demonstrate that the SAGC introduces negligible latency to the user experience by decoupling synchronous schema validation from asynchronous financial logging.

## Mermaid Sequence Diagram

```mermaid
sequenceDiagram
    autonumber
    actor U as End User
    participant IG as API Gateway (Ingress)
    participant App as App / AI Agent Pod
    box VPC Egress & Governance
    participant OPA as SAGC Sidecar (OPA)
    participant Cache as Redis (Token State)
    end
    participant LLM as Vendor API (OpenAI/Anthropic)
    participant SIEM as Async Event Queue (Kafka)

    U->>IG: AI Feature Request
    IG->>App: Authenticate & Route
    App->>OPA: Outbound LLM Call (Intercepted)
    
    rect rgb(240, 248, 255)
    Note over OPA,Cache: Synchronous Evaluation Path (Sub-millisecond)
    OPA->>OPA: Schema Validation & DLP Redaction
    OPA->>Cache: Check FinOps Budget via TTL/Hash
    Cache-->>OPA: Budget OK
    end

    OPA->>LLM: Forward via mTLS
    LLM-->>OPA: Return Generative Payload
    OPA->>OPA: Egress Validation (Prevent Executable Code)
    OPA-->>App: Validated Response
    App-->>U: Render UI State
    
    Note over OPA,SIEM: Asynchronous Decoupled Operations
    OPA-)SIEM: Fire-and-Forget (Payload Hashes, Metrics)