# PoC Automation

> Source: [10. Technical PoC — Paid Upgrade Activation Monitoring](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/14909445) · Content ID `14909445` · Version `9` · Status `current`

> Packaging gate: the Confluence page has no Postman or n8n JSON attachment. The page links to an external Postman workspace and states that the n8n workflow is retained locally; therefore the two JSON deliverables are intentionally not fabricated.

**Status:** PROTOTYPED — MANUAL VERIFICATION COMPLETE

**Traceability:** [SUB-6](https://mindyworkflows.atlassian.net/browse/SUB-6) · [BR-UPG-01](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/98325/Business+Rules+Decision+Tables) · `AC-UPG-03.2–03.4` · `DEC-UPG-01`

**Boundary & verification:** This page records author-run manual simulations using Postman mock APIs and a local n8n workflow. The 5-minute threshold is a demonstration parameter, not an approved production SLA. No independently accessible run artifact or production integration is included; implementation readiness still requires Engineering, DevOps and Security validation.

# 1. Problem Statement & Monitoring Concept

Paid upgrade completion is asynchronous: payment can be confirmed before the target-plan entitlement is applied. The operational risk is a paid upgrade whose entitlement is incorrect or remains pending beyond the monitoring threshold.

```
Postman Mock APIs
        │ webhook / poll
        ▼
n8n Workflow Prototype
├── Read Subscription Change Request (SCR) and payment result
├── Read Entitlement Activation (EA)
├── Match workspace, target plan and elapsed time (Δt)
└── Classify outcome and route the proposed operational alert
```

**Prototype artifacts:** [ApproveFlow Activation Mock API](https://mindy-workflows-4402981.postman.co/workspace/af7a4bfd-a892-4d38-8534-cee67ef4f9e4/collection/59058682-f1c3c4a6-ed79-43f7-99f2-5cd9b1b03669) · n8n workflow retained in the author’s local environment.

# 2. Evaluation Matrix & Domain Mapping

Monitoring outcomes describe the result of a check; domain states remain authoritative service data. The monitor must not overwrite an SCR or EA state without an explicit downstream result.

| **Monitoring outcome** | **Evaluation logic** | **Domain-state interpretation** | **Alert severity** | **Action** |
| --- | --- | --- | --- | --- |
| `MATCHED` | Workspace and target plan match; activation completed within threshold. | SCR: `APPLIED` EA: `APPLIED` | None | Close the check. |
| `WITHIN_WAIT` | Activation remains pending and Δt ≤ 5 minutes. | SCR: `ACTIVATION_PENDING` EA: `PENDING` | None | Continue the next check cycle. |
| `EXCEPTION` | Δt \> 5 minutes, or the applied plan does not match the purchased plan. | Keep authoritative states unchanged pending reconciliation. | **P1 / High** | Alert Platform Admin; reconcile payment, SCR and entitlement. |
| `SKIPPED` | Payment is not confirmed. | No entitlement evaluation is performed. | None | End the check. |
| `DATA_WARNING` | EA record is missing, or `workspace_id` does not match. | No automatic state change. | **P2 / Medium** | Alert Finance/Support for data-consistency review. |
| `READ_ERROR` | Entitlement API returns HTTP 500 or cannot be reached. | No automatic state change. | **P2 / Medium** | Alert Platform Admin and retry the read safely. |

**Elapsed-time calculation**

```
Completed activation: Δt = entitlement_activation.completed_at − payment_attempt.confirmed_at
Pending activation:   Δt = checked_at − payment_attempt.confirmed_at
```

# 3. Scenario Test Suite & Prototype Results

Expected and actual outcomes below were recorded from local manual workflow runs.

| **Test ID** | **Scenario** | **Mock input** | **Expected** | **Actual** | **Verdict** |
| --- | --- | --- | --- | --- | --- |
| T01 | Correct target plan applied | Plan: PRO; Δt = 45s | `MATCHED` | `MATCHED` | **PASS** |
| T02 | Activation pending within threshold | EA: PENDING; Δt = 2m 15s | `WITHIN_WAIT` | `WITHIN_WAIT` | **PASS** |
| T03 | Activation pending beyond threshold | EA: PENDING; Δt = 6m 10s | `EXCEPTION` | `EXCEPTION` | **PASS** |
| T04 | Payment not confirmed | Non-success payment result | `SKIPPED` | `SKIPPED` | **PASS** |
| T05 | Workspace identity mismatch | `ws_001` vs `ws_002` | `DATA_WARNING` | `DATA_WARNING` | **PASS** |
| T06 | Entitlement API unavailable | HTTP 500 | `READ_ERROR` | `READ_ERROR` | **PASS** |
| T07 | Entitlement record missing | HTTP 404 | `DATA_WARNING` | `DATA_WARNING` | **PASS** |
| T08 | Purchased and applied plans differ | Target: PRO; applied: BASIC | `EXCEPTION` | `EXCEPTION` | **PASS** |

**Result:** 8/8 scenarios matched the expected classification. T08 validates wrong-plan detection; it does not simulate an explicit downstream activation-failure response.

# 4. Technical Artifacts & Engineering Handover

### Alert payload contract

```json
{
  "monitoring_event": "UPGRADE_ACTIVATION_CHECK",
  "workspace_id": "ws_001",
  "change_request_id": "cr_001",
  "classification": "EXCEPTION",
  "severity": "P1_HIGH",
  "elapsed_seconds": 370,
  "threshold_seconds": 300,
  "requires_reconciliation": true,
  "observed_at": "2026-10-25T14:59:00Z"
}
```

**Safe webhook sink:** <https://httpbin.org/post>. It is used only to inspect test payload shape; no live credential is documented.

### Engineering handover decisions

1. Replace the local n8n prototype with either a scheduled background worker or an event-driven consumer of verified payment-success events.
2. Define retry limits and exponential backoff for `WITHIN_WAIT` and `READ_ERROR`; the prototype does not baseline these values.
3. Preserve the no-duplicate-charge invariant: monitoring and entitlement retry must never initiate a second payment.
4. Persist correlation IDs and outcome history so Operations can trace payment, SCR, EA and alert events end to end.

