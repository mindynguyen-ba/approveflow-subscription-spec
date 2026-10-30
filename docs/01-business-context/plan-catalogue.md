# Plan Catalogue & Entitlement Matrix

> Source: [Plan Catalogue & Entitlement Matrix](https://mindyworkflows.atlassian.net/wiki/pages/8192008) · Content ID `8192008` · Version `5` · Status `current`

**Specification purpose:** This page is the configuration reference for ApproveFlow MVP plan hierarchy, commercial terms, usage quotas, feature entitlements, transition classification and downgrade enforcement. It supports pricing preview, entitlement activation and validation.

# 1. Pricing Strategy & Market Benchmark

ApproveFlow is positioned for Vietnamese content agencies and marketing teams: below global collaboration-suite pricing while remaining comparable to local business-management SaaS products.

| Reference | Reference Point | Positioning for ApproveFlow |
| --- | --- | --- |
| [Notion](https://www.notion.com/pricing) | Plus: USD 10/member/month; Business: USD 20/member/month. | ApproveFlow is simulated as a more accessible option for local SMB teams. |
| [1Office](https://1office.vn/bang-gia) | Approximately 60,000–150,000 VND/user/month across referenced products. | Local references support the simulated range of **39,000–149,000 VND per active member/month**. |
| [Base Service](https://base.vn/app/service) | 70,000 VND/account/month when purchased separately. |  |
| [MISA AMIS Công việc](https://amis.misa.vn/9920/) | 8,600,000 VND/year for up to 20 accounts. |  |

# 2. Plan Tier Hierarchy & Commercial Terms

| Plan Code | Plan | Tier Rank | Price / Active Member / Month | Target Customer |
| --- | --- | --- | --- | --- |
| `TIER_STARTER` | **Starter** | 1 | **39,000 VND** | Small teams getting started. |
| `TIER_BASIC` | **Basic** | 2 | **79,000 VND** | Growing teams managing multiple projects. |
| `TIER_PRO` | **Pro** | 3 | **149,000 VND** | Teams requiring advanced automation and governance. |

## Commercial Rules

- **Billing cycle and currency:** monthly billing only, in VND; catalogue prices exclude VAT.
- **Billable unit:** active workspace members. Guest approvers are not billable.
- **Upgrade timing:** immediate after verified payment success.
- **Downgrade timing:** scheduled for the end of the current billing cycle.

# 3. Usage Quotas Matrix

**Enforcement types:** `CAP` = hard ceiling; `PERIODIC` = resets each billing month; `RETENTION` = history-retention duration.

| **Quota Key (System ID)** | **Entity** | **Enforcement** | **Starter** | **Basic** | **Pro** |
| --- | --- | --- | --- | --- | --- |
| `QUOTA_GUEST_APPROVERS` | Client guest approvers | `CAP` | 3 guests | 20 guests | 100 guests |
| `QUOTA_ACTIVE_PROJECTS` | Active projects | `CAP` | 10 projects | 50 projects | Unlimited |
| `QUOTA_STORAGE` | Storage allocation | `CAP` | 5 GB | 50 GB | 500 GB |
| `QUOTA_FILE_SIZE` | Maximum single-file size | `CAP` | 25 MB | 250 MB | 2 GB |
| `QUOTA_AUTOMATION_RUNS` | Automation runs | `PERIODIC` | 200 runs/month | 2,000 runs/month | 20,000 runs/month |
| `QUOTA_ACTIVE_AUTOMATIONS` | Active automation workflows | `CAP` | 3 workflows | 20 workflows | Unlimited |
| `QUOTA_VERSION_HISTORY` | Version-history trail | `RETENTION` | 7 days | 30 days | 180 days |
| `QUOTA_INTEGRATIONS` | External app integrations | `CAP` | 1 integration | 5 integrations | Unlimited |

# 4. Feature Entitlements Matrix

The value type tells Engineering how each entitlement should be represented: boolean flag, access level, enum, set, duration or response target.

| **Feature Key (System ID)** | **Capability** | **Value Type** | **Starter** | **Basic** | **Pro** |
| --- | --- | --- | --- | --- | --- |
| `FEAT_BOARD_VIEWS` | List, board and calendar views | `BOOLEAN` | Yes | Yes | Yes |
| `FEAT_TIMELINE_GANTT` | Timeline and Gantt | `BOOLEAN` | No | Yes | Yes |
| `FEAT_AUTOMATION` | Workflow automation | `LEVEL` | Basic | Standard | Advanced |
| `FEAT_APPROVAL_FLOWS` | Approval workflows | `BOOLEAN` | No | Yes | Yes |
| `FEAT_REPORT_DASH` | Dashboard reporting | `LEVEL` | Basic | Standard | Advanced |
| `FEAT_API_ACCESS` | Developer API access | `ACCESS_LEVEL` | None | Read only | Read and write |
| `FEAT_WEBHOOKS` | Outbound webhooks | `BOOLEAN` | No | No | Yes |
| `FEAT_CUSTOM_ROLES` | Custom roles | `BOOLEAN` | No | No | Yes |
| `FEAT_AUDIT_LOG` | Security audit log | `RETENTION` | 7 days | 30 days | 365 days |
| `FEAT_DATA_EXPORT` | Data export formats | `SET` | CSV | CSV, XLSX | CSV, XLSX, API |
| `FEAT_SLA_SUPPORT` | Support response target | `DURATION` | 48 hours | 24 hours | 8 hours |

# 5. Transition Rules & Evaluation Logic

Plan-change classification is derived from tier rank rather than hard-coded plan-name pairs:

```
rank_delta = target_rank - current_rank
rank_delta > 0  → UPGRADE — immediate after payment success
rank_delta < 0  → DOWNGRADE — scheduled at cycle boundary
rank_delta = 0  → NO_CHANGE — request blocked
```

| **Current \\ Target** | **Starter (1)** | **Basic (2)** | **Pro (3)** |
| --- | --- | --- | --- |
| Starter (1) | No Change — Blocked | **Upgrade — Immediate** | **Upgrade — Immediate** |
| Basic (2) | **Downgrade — Scheduled** | No Change — Blocked | **Upgrade — Immediate** |
| Pro (3) | **Downgrade — Scheduled** | **Downgrade — Scheduled** | No Change — Blocked |

## Transition Constraints

- Do not create a Subscription Change Request (**SCR**) when current and target tiers are identical.
- Allow no more than one active, non-terminal SCR per workspace.
- Upgrade activation requires verified payment success; failed payment keeps the current tier and entitlements.

# 6. Downgrade Over-Quota Enforcement Policy

**Invariant: preserve data and restrict new writes.** A downgrade must never delete existing customer data.

| **Policy** | **Required Behaviour** |
| --- | --- |
| **Data Preservation** | Preserve existing projects, files, members and configuration. No direct deletion is allowed. |
| **Access Retention** | Existing data remains available for viewing and download. |
| **Write Restriction** | Block new projects, file uploads, integrations or automation activity that would exceed the target-tier limit. |
| **Restriction Exit** | Remove the restriction when usage falls within the target quota or the workspace upgrades again. |
| **Graceful Feature Degradation** | Disable unsupported features such as webhooks or custom roles while retaining their stored configuration for future restoration. |

**Validation trace:** downgrade data-integrity scenarios and `SQL-06` verify the zero-data-loss invariant.

