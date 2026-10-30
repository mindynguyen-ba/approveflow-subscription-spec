# ROI & Measurement Plan

> Source: [ROI & Measurement Plan](https://mindyworkflows.atlassian.net/wiki/pages/66158) · Content ID `66158` · Version `7` · Status `current`

Define how ApproveFlow MVP business value would be evaluated after release. The [Business Success Metrics](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/229417/Scope+Stakeholders+Success+Metrics) define success; this page connects each metric to its evidence, owner and Day-90 decision.

## 1. Projected Operational Capacity

| **Workflow** | **Baseline hypothesis** | **Target reduction / self-service** | **Monthly capacity released** |
| --- | --- | --- | --- |
| **Subscription-change tickets** | 800 tickets/month × 20 minutes manual handling | 70% self-service | **186.7 hours/month** |
| **Billing & invoice disputes** | 40 disputes/month × 30 minutes handling | 50% reduction | **10.0 hours/month** |
| **Total operational capacity** | Time redirected to higher-complexity support work | — | **≈196.7 hours/month** |

**Interpretation:** “Capacity released” means time available for other work. It does not imply staff reduction or realized cost saving. Plan prices and entitlements remain defined in the [Plan Catalogue and Entitlement Matrix](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/8192008/Plan+Catalogue+Entitlement+Matrix).

## 2. Core Success Metrics

| **Value pillar** | **Metrics** | **Target** | **Evidence source** | **Owner** |
| --- | --- | --- | --- | --- |
| **A. Velocity & Adoption**Can customers complete changes quickly without support? | **BSM-01** Self-Service Completion **BSM-02** Support-Assisted Rate **BSM-03** Median Upgrade Activation Time | ≥ 80% ≤ 20% ≤ 5 minutes | `Subscription Change Request (SCR)` events Support tickets + SCRs `Payment Attempt` → `Entitlement Activation` timestamps | Product Support Ops Product Ops |
| **B. Data Integrity & Guardrails**Does the system apply the correct entitlement and effective date? | **BSM-06** Entitlement Activation Accuracy **BSM-07** Restriction Accuracy **BSM-04** Scheduled Downgrade Completion | 100% 100% ≥ 95% | `Subscription` vs `Entitlement Activation` audit `Invoice` + `Access Transition` audit `SCR` at effective date | Product Ops Platform Ops Platform Ops |
| **C. Recovery & Disputes**Can failed payment and access states recover safely? | **BSM-05** Payment Recovery Within Grace Period **BSM-08** Median Access Restoration Time | Benchmark first Benchmark first | `Invoice` + `Access Transition` `Payment Attempt` + `Access Transition` | Finance/Billing Platform Ops |

**OP-01 — Operational capacity released** is calculated from eligible ticket volume × average manual handling time × achieved self-service/reduction rate, using Support time tracking.

## 3. Day-90 Evaluation & Guardrails

### Evaluation method

- Capture a 4–12 week pre-release baseline where historical data exists.
- Compare equivalent volumes: per eligible flow or per 1,000 workspaces.
- Segment by plan and workspace size before drawing conclusions.
- Review early signals at Day 30/60 and make the scale decision at Day 90.
- Rate each metric NOT MEASURED → MET / AT RISK / NOT MET.
    - `NOT MEASURED` — Insufficient evidence to evaluate.
    - `MET` — Actual result meets the target.
    - `AT RISK` — Target is not yet met, but the trend indicates it may still be achieved.
    - `NOT MET` — Target is missed and corrective action is required.

### Zero-tolerance guardrails

1. **0 duplicate charges**
2. **0 invalid downgrades**
3. **0 downgrade-driven data deletion**

If any guardrail is breached, pause expansion and open a root-cause investigation before proceeding.

### Decision at Day 90

Product and Operations review target attainment, guardrail breaches and support feedback, then choose one outcome: **scale**, **adjust the workflow**, or **investigate a failed hypothesis**.

**Financial ROI:** not estimated because reliable labor-cost, implementation-cost and production-volume baselines are unavailable. It may be added later using approved confidential inputs.

