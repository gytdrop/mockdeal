# Interface Contract (Data & API Agreements) — VantageOps

> **CRITICAL RULE FOR AKTHAR & ASHRITH**:
> 1. `vantage_core` is **FROZEN** after initial baseline setup. Extends native `sale.order` and `sale.order.line`.
> 2. **Akthar** works EXCLUSIVELY inside `custom_addons/vantage_governance/`.
> 3. **Ashrith** works EXCLUSIVELY inside `custom_addons/vantage_fulfillment/`.
> 4. Do not rebuild native Odoo functionality: rely on `sale`, `mail.activity`, `portal`, and `sale_stock`.

---

## 1. Shared Foundation: `vantage_core` (Base Models: `sale.order` & `sale.order.line`)

| Model | Field Name | Type | Description |
| :--- | :--- | :--- | :--- |
| `sale.order` | `blended_risk_score` | `Float` | Order-wide aggregate risk metric based on discount deviations |
| `sale.order` | `risk_approval_state` | `Selection` | `['draft', 'pending_approval', 'approved', 'rejected']` |
| `sale.order` | `is_recurring_hybrid` | `Boolean` | True if quote contains both one-time products and recurring subscription lines |
| `sale.order.line` | `line_risk_score` | `Float` | Individual line penalty based on discount vs permissible margin |
| `sale.order.line` | `is_subscription_item` | `Boolean` | True if product is categorized as a recurring subscription |
| `menus.xml` | `menu_vantage_root` | Menu Item | Top-level 9-grid application launcher and navbar tabs (Dashboard, Quotations, Approvals, Fulfillment, Subscriptions, Invoices, Deal Health, Reports, Products) |

---

## 2. Commercial Control: `vantage_governance` (Akthar)

| Target | Identifier | Type | Description |
| :--- | :--- | :--- | :--- |
| `res.partner` | `customer_tier` | `Selection` | Contractual tier: `bronze` (5%), `silver` (10%), `gold` (15%) |
| `sale.order` | `negotiation_rounds` | `Integer` | Count of customer counter-offers (circuit breaker limit: 3) |
| `sale.order` | `max_negotiation_rounds` | `Integer` | Configurable round limit (default: 3) |
| `sale.order` | `is_negotiation_locked` | `Boolean` | Set to True when negotiation rounds exceed maximum permitted |
| `sale.order` | `last_counter_offer` | `Char` | Audit text of latest customer counter-offer |
| `sale.order` | `deal_health` | `Selection` | `healthy` (green), `stalled` (yellow, >3d), `margin_bleed` (red) |
| `sale.order` | `days_inactive` | `Integer` | Elapsed days since last modification |
| `sale.order` | `discount_anomaly` | `Boolean` | Flagged True if average order line discount is >= 20% |
| `sale.order` | `action_confirm()` | Method Override | Blocks confirmation if risk is high and unapproved; raises `UserError` and schedules `mail.activity` |
| `sale.order` | `action_manager_approve()` | Method | Tier-1 approval. If risk <= 10, marks approved; if risk > 10, auto-escalates to `pending_finance` |
| `sale.order` | `action_finance_approve()` | Method | Tier-2 final approval by Finance Director for severe risk deals |
| `sale.order` | `action_manager_reject()` | Method | Rejects deal, resolves activities, and logs feedback to Chatter |
| `sale.order` | `action_nudge_rep()` | Method | Dispatches automated reminder activity to sales rep for stalled quotes |
| `sale.order` | `action_customer_counter_offer()` | Method | Intercepts portal counter, increments rounds, recalculates risk, logs to chatter |
| `vantage.sales.dashboard` | Model (`_name`) | Model | Executive Sales Cockpit model computing real-time pipeline, risk, approval, fulfillment, and revenue metrics |
| `vantage.sales.dashboard` | `action_view_approvals()` | Method | Direct action drill-down from dashboard KPI card to pending approval quotations |
| `portal` | `sale_order_portal_template` | QWeb XML XPath | Injects counter-offer card & circuit breaker alert into portal view |
| `sale.view_quotation_tree` | `view_quotation_tree_inherit_vantage` | XML Tree | Injects Risk, Approval state, and Deal Health badges into quotation list |
| `sale.view_sales_order_filter` | `view_sales_order_filter_inherit_vantage` | XML Search | Injects filters for Pending Manager, Pending Finance, Stalled Deals, Margin Bleed |
| `sale.view_sale_order_kanban` | `view_sale_order_kanban_inherit_vantage` | XML Kanban | Injects Deal Health status badge onto quotation kanban cards |
| `dashboard_views.xml` | `view_vantage_sales_dashboard_form` | XML Form View | Full-width Bootstrap 5 executive sales cockpit with KPI cards, live badges, and quick action launchpads |

---

## 3. Operational Execution: `vantage_fulfillment` (Ashrith)

| Target | Identifier | Type | Description |
| :--- | :--- | :--- | :--- |
| `sale.order.line` | `free_qty_today` | `Float` | Real-time available stock in order's primary warehouse |
| `sale.order.line` | `requires_split` | `Boolean` | Computed True when `free_qty_today < product_uom_qty` |
| `sale.order.line` | `deficit_qty` | `Float` | Deficit quantity exceeding primary warehouse available stock |
| `sale.order.line` | `is_split_parent` | `Boolean` | True if line was truncated to available stock during auto-split |
| `sale.order.line` | `is_split_child` | `Boolean` | True if line was created to route backordered deficit to secondary WH |
| `sale.order.line` | `fulfillment_warehouse_id` | `Many2one` | Regional `stock.warehouse` assigned for this specific line |
| `sale.order.line` | `margin_delta` | `Float` | Net dollar margin contribution (`subtotal - cost * qty`) |
| `sale.order.option` | `margin_delta` | `Float` | Net dollar profit contribution for Optional Products line |
| `sale.order` | `has_split_requirement` | `Boolean` | Computed True if any line item requires warehouse splitting |
| `sale.order` | `secondary_warehouse_id` | `Many2one` | Alternative warehouse targeted for backorder fulfillment splits |
| `sale.order` | `billing_schedule_ids` | `One2many` | Relation to `vantage.billing.schedule` installment records |
| `sale.order` | `billing_schedule_count` | `Integer` | Computed count of scheduled billing periods |
| `sale.order` | `available_upsell_ids` | `Many2many` | Matching `vantage.upsell.rule` recommendations for cart products |
| `vantage.billing.schedule` | Model (`_name`) | Model | Installment milestone tracking (hardware 1-time + 12 monthly cycles) |
| `vantage.upsell.rule` | Model (`_name`) | Model | Pairing rules: `source_product_id`, `recommended_product_id`, profit impact |
| `sale.order` | `action_split_fulfillments()` | Method | Splits lines with stock deficits: truncates primary line & forks secondary backorder line |
| `sale.order` | `action_generate_billing_schedule()` | Method | Autonomously creates one-time hardware + 12 monthly subscription schedules |
| `vantage.upsell.rule` | `action_apply_upsell()` | Method | 1-click button inserting recommended upsell product directly into quotation |
| `vantage.billing.schedule` | `action_mark_invoiced()` | Method | Marks billing milestone period status as 'invoiced' |
| `sale.view_order_form` | `page_ashrith_fulfillment` | XML Form Tab | Injects "Fulfillment & Warehouses" tab into quotation form |
| `sale.view_order_form` | `page_billing_schedule` | XML Form Tab | Injects "Hybrid Billing Schedule" tab with period list and invoice triggers |
| `sale.view_order_form` | `page_smart_upsell` | XML Form Tab | Injects "Smart Upsells" tab with real-time pairing recommendations |
| `sale.product_menu_catalog` | `menu_vantage_upsell_rules` | Menu Item | Adds "Upsell Rules" menu under Sales -> Products |
