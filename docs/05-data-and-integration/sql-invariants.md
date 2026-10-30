# SQL Invariants

> Source: [API, SQL & Sequence Analysis](https://mindyworkflows.atlassian.net/wiki/spaces/~712020023d2d45822847ceae0a13314552bb4b/pages/229453) · Content ID `229453` · Version `16` · Status `current`

**Status:** DESIGNED — NOT EXECUTED

# 4. Database Invariant Validations

These queries detect invalid data states. In normal operation, every query must return **0 rows**.

```sql
-- SQL-01 · One current Subscription per Workspace
SELECT workspace_id, COUNT(*) AS current_subscription_count
FROM subscription
WHERE status IN ('ACTIVE', 'PAST_DUE', 'RESTRICTED')
GROUP BY workspace_id
HAVING COUNT(*) > 1;

-- SQL-02 · One non-terminal SCR per Subscription
SELECT subscription_id, COUNT(*) AS open_request_count
FROM subscription_change_request
WHERE status IN (
  'PAYMENT_PENDING', 'PAYMENT_FAILED',
  'ACTIVATION_PENDING', 'ACTIVATION_FAILED', 'SCHEDULED'
)
GROUP BY subscription_id
HAVING COUNT(*) > 1;

-- SQL-03 · Applied Upgrade requires successful Entitlement Activation
SELECT cr.change_request_id, cr.subscription_id, cr.status
FROM subscription_change_request cr
WHERE cr.change_type = 'UPGRADE'
  AND cr.status = 'APPLIED'
  AND NOT EXISTS (
    SELECT 1
    FROM entitlement_activation ea
    WHERE ea.change_request_id = cr.change_request_id
      AND ea.status = 'APPLIED'
  );

-- SQL-04 · Failed Upgrade payment must not change the current plan
SELECT DISTINCT
  cr.change_request_id,
  s.subscription_id,
  s.current_plan_id,
  cr.target_plan_id
FROM subscription_change_request cr
JOIN subscription s ON s.subscription_id = cr.subscription_id
JOIN payment_attempt pa ON pa.change_request_id = cr.change_request_id
WHERE cr.change_type = 'UPGRADE'
  AND cr.status = 'PAYMENT_FAILED'
  AND pa.status = 'FAILED'
  AND s.current_plan_id = cr.target_plan_id;

-- SQL-05 · External payment transaction must be unique
SELECT provider_transaction_id, COUNT(*) AS duplicate_count
FROM payment_attempt
WHERE provider_transaction_id IS NOT NULL
GROUP BY provider_transaction_id
HAVING COUNT(*) > 1;

-- SQL-06 · ACTIVE Subscription must not have a PAST_DUE Invoice
SELECT s.subscription_id, i.invoice_id, i.status AS invoice_status
FROM subscription s
JOIN invoice i ON i.subscription_id = s.subscription_id
WHERE s.status = 'ACTIVE'
  AND i.status = 'PAST_DUE';

-- SQL-07 · RESTRICTED requires an expired unpaid Invoice
SELECT s.subscription_id, s.status
FROM subscription s
WHERE s.status = 'RESTRICTED'
  AND NOT EXISTS (
    SELECT 1
    FROM invoice i
    WHERE i.subscription_id = s.subscription_id
      AND i.status = 'PAST_DUE'
      AND i.grace_expires_at <= CURRENT_TIMESTAMP
  );

-- SQL-08 · Scheduled Downgrade must not apply before effective_at
SELECT change_request_id, status, effective_at, completed_at
FROM subscription_change_request
WHERE change_type = 'DOWNGRADE'
  AND status = 'APPLIED'
  AND completed_at < effective_at;
--SQL-08 limitation: detecting execution after cancellation requires immutable transition history or an audit-event table; the current schema exposes only final status and completed_at.
```

