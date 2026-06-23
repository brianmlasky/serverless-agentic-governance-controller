# ADR 020: Dynamic FinOps Alerting (Anomaly Detection)

## Status
Accepted

## Context
While hard budget limits prevent fiscal ruin, unexpected spikes in token burn rates can exhaust an agent's monthly budget in minutes, causing premature denial of service. Relying solely on a $0 balance to detect anomalies is an anti-pattern.

## Decision
We implement proactive, dynamic alerting using Prometheus and Alertmanager.
1. The API Gateway will emit custom Prometheus metrics tracking token consumption per agent (`sagc_token_spend_total`).
2. We will deploy a `PrometheusRule` that calculates the 5-minute moving average of the burn rate.
3. If the burn rate exceeds the predefined standard deviation for that specific agent profile, a High Priority alert is routed to the SRE team via Slack/PagerDuty.

## Consequences
* **Positive:** Shifts FinOps from a reactive "billing shock" model to a proactive "incident response" model.
* **Negative:** Requires tuning alert thresholds to avoid alert fatigue from legitimate high-burst agent workloads.
