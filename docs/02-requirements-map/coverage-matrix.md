# Acceptance Criteria Coverage Matrix

> Source: [Acceptance Criteria Coverage Matrix](https://mindyworkflows.atlassian.net/wiki/pages/5341219) · Content ID `5341219`

**Purpose:** Verify that Acceptance Criteria are defined for all 6 MVP User Stories. Detailed AC wording is maintained in Jira.

**Status:** BASELINED — 6/6 Stories covered | 40/40 AC defined.

This page tracks scope coverage and QA planning input—not test execution evidence.

---

## 1. Coverage Summary

| **User Story** | **Jira ID** | **AC Range** | **AC Count** | **Key Areas Covered** | **Status** |
| --- | --- | --- | --- | --- | --- |
| **US-01 — View Subscription & Plans** | [SUB-4](https://mindyworkflows.atlassian.net/browse/SUB-4) | `AC-PLAN-01.1–01.6` | 6 | Context, usage quotas, plan catalogue, RBAC permissions | BASELINE |
| **US-02 — Preview & Confirm Upgrade** | [SUB-5](https://mindyworkflows.atlassian.net/browse/SUB-5) | `AC-UPG-02.1–02.6` | 6 | Eligibility, pricing & VAT, proration, 15-minute TTL, confirmation | BASELINE |
| **US-03 — Complete Upgrade & View Outcome** | [SUB-6](https://mindyworkflows.atlassian.net/browse/SUB-6) | `AC-UPG-03.1–03.6` | 6 | Payment capture, entitlement activation, outcome, duplicate prevention | BASELINE |
| **US-04 — Schedule Downgrade** | [SUB-7](https://mindyworkflows.atlassian.net/browse/SUB-7) | `AC-DOWN-04.1–04.8` | 8 | Quota impact, soft enforcement, cycle-end schedule, execution-time revalidation | BASELINE |
| **US-05 — Cancel Scheduled Downgrade** | [SUB-8](https://mindyworkflows.atlassian.net/browse/SUB-8) | `AC-DOWN-05.1–05.5` | 5 | Cancellation eligibility, plan retention, SCR closure, audit | BASELINE |
| **US-06 — Recover from Payment Failure** | [SUB-9](https://mindyworkflows.atlassian.net/browse/SUB-9) | `AC-REC-06.1–06.9` | 9 | 30-day Grace Period, retry, read-only restriction, restoration, duplicate prevention | BASELINE |
| **Total Scope (MVP)** | **6 Stories** | — | **40 AC** | **100% Story Coverage** | READY FOR DEV & QA PLANNING |

---

## 2. Verification Rules

- **Traceability invariant:** Every User Story in the committed MVP scope must have an approved AC range before moving to `In Development`.
- **Single source of truth:** This matrix supports scope audit and test-effort planning. Detailed Given–When–Then criteria and test execution evidence remain in Jira and the configured test-management tool.

