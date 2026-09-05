# DealFlow360 Agent Guidelines & Team Governance

This repository enforces an **isolated modular Odoo architecture** for a 2-person engineering team (**Akthar** and **Ashrith**).
Every developer and AI coding agent operating in this codebase MUST strictly follow these rules to ensure zero code conflicts and seamless delivery.

---

## 1. Team Directory & Ownership Structure

Custom modules are located strictly under `custom_addons/`:

```
custom_addons/
├── hackathon_core/          # FROZEN BASE: Shared data models, base views, and core menus.
├── hackathon_feature_a/     # AKTHAR'S MODULE: Pricing Governance, Approvals, Portal & Deal Health.
└── hackathon_feature_b/     # ASHRITH'S MODULE: Multi-Warehouse Splitting, Hybrid Billing & Upsell Engine.
```

### Module Assignment
| Teammate | Assigned Addon Module | Technical Focus |
| :--- | :--- | :--- |
| **Akthar** | `custom_addons/hackathon_feature_a/` | Discount Ceilings, Blended Risk Score, Multi-tier Approvals (Manager + Finance), Customer Negotiation Portal, Deal Health & Anomaly Dashboard. |
| **Ashrith** | `custom_addons/hackathon_feature_b/` | Multi-Warehouse Stock Allocation, Split Fulfillment Engine, Hybrid Billing (One-time vs Subscription Schedules), Live Upsell Recommendations. |

---

## 2. Ironclad Rules (Zero-Conflict Protocol)

1. **`hackathon_core` is 100% FROZEN**:
   - `hackathon_core` defines the foundational models (`dealflow.quote`, `dealflow.quote.line`, `dealflow.product`).
   - **DO NOT MODIFY `hackathon_core`**. Any feature-specific fields, logic, or buttons MUST be added via inheritance (`_inherit`) inside your assigned module.

2. **Strict File Isolation**:
   - **If working as Akthar**: You are STRICTLY FORBIDDEN from editing any file under `custom_addons/hackathon_feature_b/` or `custom_addons/hackathon_core/`.
   - **If working as Ashrith**: You are STRICTLY FORBIDDEN from editing any file under `custom_addons/hackathon_feature_a/` or `custom_addons/hackathon_core/`.

3. **Data Model Inheritance (`_inherit`)**:
   - Always extend existing models using `_inherit`:
     ```python
     class DealflowQuoteFeatureA(models.Model):
         _inherit = 'dealflow.quote'
         blended_risk_score = fields.Float(string='Blended Risk Score')
     ```
   - New stand-alone models must have unique prefixes:
     - Akthar: `dealflow.discount.tier`, `dealflow.approval.log`, `dealflow.deal.health`
     - Ashrith: `dealflow.warehouse`, `dealflow.fulfillment.split`, `dealflow.billing.schedule`, `dealflow.upsell.rule`

4. **XML View Extension via Unique XPath**:
   - Never override base views entirely. Always inherit using `inherit_id` and `<xpath>`.
   - Use distinct tab page names inside `<notebook>`:
     - Akthar adds `<page name="page_akthar_approvals" string="Risk &amp; Approvals">`
     - Ashrith adds `<page name="page_ashrith_fulfillment" string="Fulfillment &amp; Splitting">`

5. **Interface Contract Synchronization**:
   - Consult [CONTRACT.md](CONTRACT.md) before declaring any fields or methods.
   - Do not use field names or method names reserved for the other teammate.

6. **Git Branching Strategy**:
   - Akthar commits on branch `feature/akthar-pricing-approval` (or pushes directly to his feature folder).
   - Ashrith commits on branch `feature/ashrith-fulfillment-billing` (or pushes directly to his feature folder).

---

## 3. Persona Dispatcher Protocol

When a user or prompt indicates **"I am Akthar"** or **"I am Ashrith"**, the AI agent MUST execute this exact protocol:

### Trigger: "I am Akthar"
1. **Identify**: Acknowledge role as Akthar (Lead on Pricing Governance, Approvals, Portal & Deal Health).
2. **Restrict Scope**: Confine all file changes exclusively to `custom_addons/hackathon_feature_a/`.
3. **Inspect Progress**: Check `CONTRACT.md` and `MASTER_PLAN.md` for current milestone status.
4. **Present Work Package**: Display the specific sub-tasks queued for Akthar.
5. **Execute Immediately**: Begin implementing the next pending sub-task without delay.

### Trigger: "I am Ashrith"
1. **Identify**: Acknowledge role as Ashrith (Lead on Warehouse Fulfillment Splitting, Hybrid Billing & Upsells).
2. **Restrict Scope**: Confine all file changes exclusively to `custom_addons/hackathon_feature_b/`.
3. **Inspect Progress**: Check `CONTRACT.md` and `MASTER_PLAN.md` for current milestone status.
4. **Present Work Package**: Display the specific sub-tasks queued for Ashrith.
5. **Execute Immediately**: Begin implementing the next pending sub-task without delay.
