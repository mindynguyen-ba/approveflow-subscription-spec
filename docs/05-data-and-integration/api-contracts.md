# API Contracts

> Source: [API, SQL & Sequence Analysis](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/229453) · Content ID `229453`

DESIGNED — NOT EXECUTED Business-level contracts for analysis and testing. No endpoint call, database query, integration test or production validation has been executed.

**Scope:** Defines business boundaries, outcomes and traceability. It does not replace implementation-level OpenAPI/Swagger specifications.

# 1. API Inventory & Boundaries

**Payment boundary:** ApproveFlow never collects or stores raw payment credentials. Payment-method updates run in the Payment Processor-hosted flow; ApproveFlow receives only an active payment-method reference and verified callback results.

| **ID** | **Action** | **Method & route** | **Type** | **Minimum input** | **Traceability** |
| --- | --- | --- | --- | --- | --- |
| **API-01** | View Subscription Context | `GET /workspaces/{workspace_id}/subscription-context` | Query | Path: `workspace_id` | `US-01`, `US-06` |
| **API-02** | Preview Plan Change | `POST /subscriptions/{subscription_id}/change-previews` | Command | `target_plan_id` | `US-02`, `US-04` |
| **API-03** | Manage SCR: create / cancel | `POST /subscriptions/{subscription_id}/change-requests` `POST /change-requests/{change_request_id}/cancel` | Command | `preview_id`, `idempotency_key` `reason` | `US-03`, `US-04`, `US-05` |
| **API-04** | Retry Payment | `POST /invoices/{invoice_id}/payment-attempts` | Command | `payment_method_reference_id`, `idempotency_key` | `US-06` |
| **API-05** | Process Payment Callback | `POST /webhooks/payment-results` | Callback | `event_id`, `provider_transaction_id`, `payment_attempt_id`, `invoice_id`, `result`, `amount`, `currency`, `occurred_at` | `US-03`, `US-06` |

**Inventory-only interactions:** `API-06` View SCR Status; `API-07` View Available Plans; `API-08` View Usage & Quota. Their delivery-level routes and schemas remain intentionally deferred to OpenAPI.

- **API-02:** creates an expiring quote only; it does not persist an SCR or change Subscription state.
- **API-03:** revalidates the preview, authorization and eligibility. Upgrade starts at `PAYMENT_PENDING`; downgrade starts at `SCHEDULED`. Only one non-terminal SCR is allowed per Subscription.
- **API-04:** creates one `INITIATED` Payment Attempt. Invoice and Subscription state stay unchanged until a verified callback arrives.
- **API-05:** validates signature, payment identity, amount and currency; processes each result once; downstream activation/restoration failures must be retriable without charging again.

# 2. Error Mapping

Canonical response shape: `{"error_code":"STRING","message":"STRING"}`.

| **Error code** | **HTTP** | **Expected handling** | **API** |
| --- | --- | --- | --- |
| `AUTH_SESSION_REQUIRED` | 401 | Require authentication | 01–04 |
| `SUB_ACCESS_FORBIDDEN` | 403 | Hide or disable the action | 01–04 |
| `SUB_WORKSPACE_NOT_FOUND` | 404 | Show unavailable state | 01 |
| `SUB_SUBSCRIPTION_NOT_FOUND` | 404 | Show unavailable state | 01–02 |
| `SUB_CONTEXT_UNAVAILABLE` | 500 | Show load error and retry | 01 |
| `SUB_TARGET_PLAN_INVALID` | 400 | Return to plan selection | 02 |
| `SUB_CHANGE_NOT_ELIGIBLE` | 409 | Show blocking reason | 02 |
| `SUB_CHANGE_REQUEST_CONFLICT` | 409 | Show existing request | 02–03 |
| `SUB_PRICING_UNAVAILABLE` | 500 | Disable confirmation and retry | 02 |
| `SUB_PREVIEW_EXPIRED` | 409 | Recalculate preview | 03 |
| `SUB_CHANGE_STATE_INVALID` | 409 | Refresh request status | 03 |
| `SUB_CANCELLATION_DEADLINE_PASSED` | 409 | Show execution status | 03 |
| `SUB_IDEMPOTENCY_CONFLICT` | 409 | Return the original result or reject conflicting input | 03–04 |
| `SUB_INVOICE_NOT_PAYABLE` | 409 | Refresh invoice status | 04 |
| `SUB_PAYMENT_METHOD_INVALID` | 400 | Return to the processor-hosted payment-method flow | 04 |
| `SUB_PAYMENT_IN_PROGRESS` | 409 | Show pending status | 04 |
| `SUB_PAYMENT_PROCESSOR_UNAVAILABLE` | 500 | Allow safe retry | 04 |
| `PAYMENT_CALLBACK_SIGNATURE_INVALID` | 401 | Reject and log callback | 05 |
| `PAYMENT_ATTEMPT_NOT_FOUND` | 404 | Reject and investigate | 05 |
| `PAYMENT_RESULT_MISMATCH` | 422 | Reject, record mismatch and investigate | 05 |
| `PAYMENT_CALLBACK_PROCESSING_FAILED` | 500 | Retry without charging again | 05 |

`DUPLICATE_CALLBACK` is not an error. Return the original processing result as an idempotent success.


