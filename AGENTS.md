# VantageOps Agent Guidelines & Team Governance

This repository enforces an **isolated modular Odoo architecture** extending native Odoo models (`sale.order`, `sale.order.line`, `product.template`, `portal`) for a 2-person engineering team (**Akthar** and **Ashrith**).
Every developer and AI coding agent (Antigravity, Claude, or any LLM assistant) operating in this codebase MUST strictly follow these rules to ensure zero code conflicts, zero unverified commits, and seamless delivery.

---

## 🛑 Ironclad Rule: Repository Roles & Freeze on `VantageOps`

1. **`mockdeal` IS THE ACTIVE WORKSPACE & CANVAS**:
   - Location: `/home/gytdrop/Documents/HACKATHONS/2026/odoo hackathon/odoo gujarat`
   - Remote: `https://github.com/gytdrop/mockdeal.git`
   - **ALL development, testing, staging, and commits MUST take place HERE.**

2. **`VantageOps` IS THE FROZEN FINAL DELIVERY DESTINATION**:
   - Location: `/home/gytdrop/Documents/HACKATHONS/2026/odoo hackathon/odoo gujarat/VantageOps` (git-ignored inside mockdeal)
   - Remote: `https://github.com/gytdrop/VantageOps.git`
   - **STRICT PROHIBITION**: **NO AGENT IS PERMITTED TO RUN `git add`, `git commit`, OR STAGE ANYTHING DIRECTLY INSIDE `VantageOps`.**
   - **CLEAN CODE ONLY RULE**: `VantageOps` must strictly contain ONLY clean project code (`custom_addons`). Under no circumstances should agent logs (`.log`), summaries, or agent-related markdown files (`AGENTS.md`, `SUMMARY.md`, `EXPLAINER.md`, etc.) be copied or retained in `VantageOps`.
   - Code is promoted and copied to `VantageOps` ONLY after a feature has been fully implemented, verified, and explicitly instructed by the user.

3. **STRICT AFTAB RESTRICTION**:
   - **Aftab is strictly restricted from `VantageOps`.**
   - If the user/persona is **Aftab** (or "I am Aftab" / "I am Afteb"):
     - **NO WORK IN `VantageOps`**: Aftab is strictly forbidden from working in, editing, staging, or creating files inside the `VantageOps` repository.
     - **NO PUSH TO `VantageOps`**: Aftab is strictly forbidden from executing `git push` or pushing any code/branches to the `VantageOps` remote repository.
     - All of Aftab's work, testing, and commits must remain strictly confined to `mockdeal`.

---

## 📝 Mandatory Logging Protocol (`antigravity.log`, `claude.log`, `workonmyperiod.log`)

Every AI agent working in this repository MUST maintain and update the following logs:

1. **Agent-Specific Logs**:
   - If running as **Antigravity**: Write every commit, milestone, or log request into `antigravity.log`.
   - If running as **Claude**: Write every commit, milestone, or log request into `claude.log`.
2. **Global Session Log (`workonmyperiod.log`)**:
   - Every agent MUST append an entry to `workonmyperiod.log` on every commit, when a work period completes, or when the user says **"write log"**.
3. **Standard Log Entry Format**:
   ```
   [YYYY-MM-DD HH:MM:SS] [AGENT: Antigravity|Claude] [PERSONA: Akthar|Ashrith]
   ACTION: <Commit hash / Task summary>
   DETAILS: <Precise description of code, models, or views created/modified>
   STATUS: <Verified / In Progress / Blocked>
   ------------------------------------------------------------------------------
   ```

---

## 1. Team Directory & Ownership Structure

Custom modules are located strictly under `custom_addons/`:

```
custom_addons/
├── vantage_core/          # FROZEN BASE: Shared data model extensions on sale.order & sale.order.line.
├── vantage_governance/    # AKTHAR'S MODULE: Margin Governance, Approvals, Chatter Escalations & Portal Negotiation.
└── vantage_fulfillment/   # ASHRITH'S MODULE: Multi-Warehouse Auto-Split, Backorder Forking & Live Upsell Engine.
```

### Module Assignment
| Teammate | Assigned Addon Module | Technical Focus |
| :--- | :--- | :--- |
| **Akthar** | `custom_addons/vantage_governance/` | Margin Governance, `action_confirm` block, `mail.activity` escalations, QWeb Portal counter-offer UI, circuit-breaker negotiation logic. |
| **Ashrith** | `custom_addons/vantage_fulfillment/` | `_compute_split_requirement()`, `action_split_fulfillments()` multi-warehouse stock routing, Optional Products `margin_delta` live upsell. |

---

## 2. Zero-Conflict Protocols

1. **`vantage_core` is 100% FROZEN after initial setup**:
   - `vantage_core` defines shared fields on `sale.order` (`blended_risk_score`, `risk_approval_state`, `is_recurring_hybrid`) and `sale.order.line`.
   - **DO NOT MODIFY `vantage_core`** once established. Any feature-specific logic or UI belongs in your assigned module.

2. **Strict File Isolation**:
   - **If working as Akthar**: You are STRICTLY FORBIDDEN from editing any file under `custom_addons/vantage_fulfillment/` or `custom_addons/vantage_core/`.
   - **If working as Ashrith**: You are STRICTLY FORBIDDEN from editing any file under `custom_addons/vantage_governance/` or `custom_addons/vantage_core/`.

3. **Data Model Inheritance (`_inherit`)**:
   - Always extend existing Odoo native models (`sale.order`, `sale.order.line`) using `_inherit`:
     ```python
     class SaleOrderGovernance(models.Model):
         _inherit = 'sale.order'
     ```

4. **XML View Extension via Unique XPath**:
   - Never override base views entirely. Always inherit using `inherit_id="sale.view_order_form"` and `<xpath>`.
   - Use distinct tab page names inside `<notebook>`:
     - Akthar adds `<page name="page_akthar_approvals" string="Risk &amp; Approvals">`
     - Ashrith adds `<page name="page_ashrith_fulfillment" string="Fulfillment &amp; Splitting">`

5. **Interface Contract Synchronization**:
   - Consult [CONTRACT.md](CONTRACT.md) before declaring any fields or methods.
   - Do not use field names or method names reserved for the other teammate.

---

## 3. Persona Dispatcher Protocol

When a user or prompt indicates **"I am Akthar"**, **"I am Ashrith"**, or **"I am Aftab"** (or "I am Afteb"), the AI agent MUST execute this exact protocol:

### Trigger: "I am Akthar"
1. **Identify**: Acknowledge role as Akthar (Lead on Commercial Control: `vantage_governance`).
2. **Restrict Scope**: Confine all file changes exclusively to `custom_addons/vantage_governance/`.
3. **Inspect Progress**: Check `CONTRACT.md` and `EXECUTION_PLAN.md` for current milestone status.
4. **Present Work Package**: Display the specific sub-tasks queued for Akthar.
5. **Execute & Log**: Perform the task, test locally, commit to `mockdeal`, and append to `antigravity.log`/`claude.log` and `workonmyperiod.log`.

### Trigger: "I am Ashrith"
1. **Identify**: Acknowledge role as Ashrith (Lead on Operational Execution: `vantage_fulfillment`).
2. **Restrict Scope**: Confine all file changes exclusively to `custom_addons/vantage_fulfillment/`.
3. **Inspect Progress**: Check `CONTRACT.md` and `EXECUTION_PLAN.md` for current milestone status.
4. **Present Work Package**: Display the specific sub-tasks queued for Ashrith.
5. **Execute & Log**: Perform the task, test locally, commit to `mockdeal`, and append to `antigravity.log`/`claude.log` and `workonmyperiod.log`.

### Trigger: "I am Aftab" (or "I am Afteb")
1. **Identify**: Acknowledge role as Aftab (Restricted Contributor).
2. **Enforce Hard Restrictions**: **STRICTLY PROHIBITED FROM TOUCHING VantageOps.** Aftab is forbidden from working in `VantageOps`, modifying files in `VantageOps`, or running `git push` to `VantageOps`.
3. **Restrict Scope**: Confine all activities and edits strictly to `mockdeal`.
4. **Inspect Progress**: Check current task requirements in `mockdeal`.
5. **Execute & Log**: Perform work strictly within `mockdeal`, test locally, commit only to `mockdeal`, and append to `antigravity.log`/`claude.log` and `workonmyperiod.log`.
