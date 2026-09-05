# ⚡ VantageOps Hackathon Execution Blueprint

## 1. The Strategy: "Native Odoo Gigs"
Do not rebuild native Odoo functionality. We are exploiting core Odoo patterns to deliver the massive scope outlined in the wireframes in under 400 lines of Python.

| VantageOps Feature | We Write (The Delta) | Odoo Native Engine Handing the Rest |
| :--- | :--- | :--- |
| **Approval Routing** | Risk Score Math + `action_confirm` block | `mail.activity` (Chatter tasks & logging) |
| **Portal Negotiation** | `<xpath>` input field + RPC method | `portal` + `mail.thread` (Customer UI & security) |
| **Upsell Engine** | `margin_contribution` field | `sale_management` (Optional Products UI) |
| **WH Stock Split** | Auto-split line computation | `sale_stock` (Auto-generates pickings per WH) |

---

## 2. Resources & Repositories
*   **Target Environment:** Local Odoo DB for testing $\rightarrow$ GitHub $\rightarrow$ Assigned Online DB for judging.
*   **Reference Repo 1:** `https://github.com/odoo/odoo` (Core reference for `sale.order` and `sale_portal_templates.xml`).
*   **Reference Repo 2:** `https://github.com/OCA/sale-workflow` (Inspect `sale_exception` for approval blocking mechanics).

---

## 3. Division of Labor & UI Mapping

### 🧠 Shared Foundation (`vantage_core`)
*Both members pull this first.*
*   **Models:** Extends `sale.order` and `sale.order.line`.
*   **Logic:** Calculates `blended_risk_score`, defines `risk_approval_state`, and sets `is_recurring_hybrid`.
*   **UI Target:** Powers the central Sales Dashboard metrics.

### 👤 Member 1: Commercial Control (`vantage_governance`) - Akthar [STATUS: 100% COMPLETE]
*   **Focus Areas:** "Risk & Approvals" tab, Two-Tier Governance, Customer Tiers, Deal Health, and Customer Negotiation.
*   **Task 1 (Backend):** Override `action_confirm()`. If risk is high and unapproved, raise `UserError` and schedule a `mail.activity` for the manager/finance director. (✅ Done)
*   **Task 2 (Two-Tier Approval Chain):** Frontline Sales Manager signs off (score <= 10). If score > 10, auto-escalates to Finance Director (`action_finance_approve`). (✅ Done)
*   **Task 3 (Customer Tier Dynamic Floors):** Extends `res.partner` with Bronze (5%), Silver (10%), and Gold (15%) discount ceilings. (✅ Done)
*   **Task 4 (Deal Health & Rep Anomaly Tracker):** Real-time `deal_health` badges (`healthy`, `stalled`, `margin_bleed`), `days_inactive` tracking, and `action_nudge_rep` task dispatcher. (✅ Done)
*   **Task 5 (Frontend/QWeb):** Inherit `sale_order_portal_content` using QWeb XML to add counter-offer input and circuit-breaker lock card. (✅ Done)
*   **Task 6 (Logic):** Write `action_customer_counter_offer()` to intercept portal input, recalculate risk, log to chatter, and lock negotiation at 3 rounds. (✅ Done)

### 👤 Member 2: Operational Execution (`vantage_fulfillment`) - Ashrith [STATUS: 100% COMPLETE]
*   **Focus Areas:** "Fulfillment & Warehouses", "Hybrid Billing Schedule", "Smart Upsells", and Backorder Splits.
*   **Task 1 (Backend):** Write `_compute_split_requirement()` and `_compute_free_qty_today()` to check location-context stock against `product_uom_qty` and calculate `deficit_qty`. (✅ Done)
*   **Task 2 (Logic):** Write `action_split_fulfillments()` to split a line item into two if stock is short, pointing the deficit line to a secondary warehouse. (✅ Done)
*   **Task 3 (Hybrid Billing Engine):** `vantage.billing.schedule` model & `action_generate_billing_schedule()` autonomously separating 1-time hardware charges from 12 monthly subscription cycles. (✅ Done)
*   **Task 4 (Live Smart Upsell Engine):** `vantage.upsell.rule` model and `action_apply_upsell()` for 1-click cart insertion with live profit delta contribution. (✅ Done)
*   **Task 5 (Frontend/XML):** Add `margin_delta` to line items & Optional Products, and add `page_billing_schedule` & `page_smart_upsell` tabs. (✅ Done)

---

## 4. The Development Loop (Zero Conflict Rule)
1.  **Code & Test Locally:** Start local Odoo with `--dev=reload` and `-d <local_db>`.
2.  **Commit Isolation:** Member 1 (Akthar) only commits inside `vantage_governance`. Member 2 (Ashrith) only commits inside `vantage_fulfillment`.
3.  **Sync:** Push to GitHub `main` branch.
4.  **Deploy:** Pull to the production server and upgrade modules via UI (Apps $\rightarrow$ Update Apps List) or CLI.
