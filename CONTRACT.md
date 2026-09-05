# Interface Contract (Data & API Agreements)

> **CRITICAL RULE FOR AKTHAR & ASHRITH**:
> 1. `hackathon_core` is **FROZEN**. Neither teammate ever modifies `hackathon_core`.
> 2. **Akthar** works EXCLUSIVELY inside `custom_addons/hackathon_feature_a/`.
> 3. **Ashrith** works EXCLUSIVELY inside `custom_addons/hackathon_feature_b/`.
> 4. All model extensions must use Python `_inherit`.
> 5. All view extensions must use XML `<xpath expr="//notebook" position="inside">` with distinct `<page>` tabs.
> 6. Any new field, model, or method must be documented here before implementation.

---

## 1. Shared Base Models (Owned by `hackathon_core` - FROZEN)

| Technical Identifier | Description | Key Base Fields |
| :--- | :--- | :--- |
| `dealflow.quote` | Core Quotation / Order | `name`, `partner_name`, `partner_email`, `partner_tier`, `user_id`, `date_order`, `state`, `line_ids`, `amount_untaxed`, `amount_discount`, `amount_total`, `order_margin`, `order_margin_percent`, `notes` |
| `dealflow.quote.line` | Quotation Item Line | `quote_id`, `product_id`, `category_type`, `quantity`, `price_unit`, `cost_price`, `discount`, `price_subtotal`, `margin`, `margin_percent` |
| `dealflow.product` | Product Catalog | `name`, `category_type` (hardware/service/subscription), `list_price`, `standard_price`, `max_discount`, `active` |

---

## 2. Akthar's Scope & Ownership (`hackathon_feature_a`)

**Feature Focus**: Pricing Governance, Blended Discount Risk, Multi-Tier Approvals, Customer Negotiation Portal, Deal Health & Anomaly Alerts.

### Models Created by Akthar
| Technical Model | Table Name | Purpose |
| :--- | :--- | :--- |
| `dealflow.discount.tier` | `dealflow_discount_tier` | Configures max allowed discount ceilings per customer tier & category |
| `dealflow.approval.log` | `dealflow_approval_log` | Immutable audit trail for all approval requests, manager approvals, finance approvals, and rejections |
| `dealflow.deal.health` | `dealflow_deal_health` | System-wide deal health thresholds (days inactive, discount anomaly % vs rep average) |

### Fields Added to `dealflow.quote` by Akthar (`_inherit = 'dealflow.quote'`)
| Field Name | Type | Description |
| :--- | :--- | :--- |
| `blended_risk_score` | `Float` | Computed blended discount risk score across order lines |
| `risk_level` | `Selection` | `low` (No approval), `medium` (Manager only), `high` (Manager + Finance) |
| `requires_manager_approval` | `Boolean` | True if blended score or line discounts exceed manager threshold |
| `requires_finance_approval` | `Boolean` | True if discount or score exceeds finance threshold |
| `approval_log_ids` | `One2many` | Links to `dealflow.approval.log` records |
| `portal_token` | `Char` | Secure unique access token for customer negotiation portal |
| `portal_negotiation_active` | `Boolean` | True when quotation is shared with customer for negotiation |
| `portal_counter_discount` | `Float` | Counter discount requested by customer in portal |
| `portal_counter_notes` | `Text` | Customer remarks / requests submitted via portal |
| `is_stalled` | `Boolean` | Flagged if quote inactive for > configured threshold days |
| `days_inactive` | `Integer` | Computed days since last update |
| `discount_anomaly` | `Boolean` | Flagged if quote discount significantly exceeds rep's historical average |

### Methods Exposed by Akthar
| Method Signature | Context / Trigger | Description |
| :--- | :--- | :--- |
| `action_compute_blended_risk()` | On quote save or button click | Evaluates each line ceiling and computes aggregate blended risk score |
| `action_submit_approval()` | Rep submits quote for review | Checks risk level, updates `state` to `pending_manager` or `pending_finance`, creates audit log |
| `action_approve_manager()` | Sales Manager clicks Approve | Marks Manager step approved; advances to Finance if required, else marks `approved` |
| `action_approve_finance()` | Finance User clicks Approve | Marks Finance step approved; advances `state` to `approved` |
| `action_reject(reason)` | Reviewer clicks Reject | Reverts quote to `draft` or `rejected` with mandatory logged reason |
| `action_generate_portal_link()` | Rep clicks "Share with Customer" | Generates portal token and URL for customer access |
| `action_process_portal_counter(counter_discount, notes)` | Portal controller submission | Applies customer counter-offer; auto re-routes to approval if thresholds breached |
| `action_check_deal_health()` | Automated / Dashboard refresh | Evaluates stalled status and discount anomalies across open deals |

---

## 3. Ashrith's Scope & Ownership (`hackathon_feature_b`)

**Feature Focus**: Multi-Warehouse Fulfillment Splitting, Backorder Handling, Hybrid Billing & Subscription Proration, Live Upsell Intelligence.

### Models Created by Ashrith
| Technical Model | Table Name | Purpose |
| :--- | :--- | :--- |
| `dealflow.warehouse` | `dealflow_warehouse` | Warehouses with shipping cost weighting & location info |
| `dealflow.warehouse.stock` | `dealflow_warehouse_stock` | Live product stock quantity and replenishment rules per warehouse |
| `dealflow.fulfillment.split` | `dealflow_fulfillment_split` | Line-by-line warehouse allocation plan with shipment counts and costs |
| `dealflow.subscription.plan` | `dealflow_subscription_plan` | Recurring billing plans (monthly, quarterly, yearly) and proration policies |
| `dealflow.billing.schedule` | `dealflow_billing_schedule` | Reconciles one-time charges with recurring subscription dates & proration |
| `dealflow.upsell.rule` | `dealflow_upsell_rule` | Co-purchase rules, promoted flags, and margin threshold criteria |
| `dealflow.quote.upsell` | `dealflow_quote_upsell` | Live upsell / cross-sell suggestions generated for the current quotation |

### Fields Added to `dealflow.quote` by Ashrith (`_inherit = 'dealflow.quote'`)
| Field Name | Type | Description |
| :--- | :--- | :--- |
| `fulfillment_split_ids` | `One2many` | Links to `dealflow.fulfillment.split` records |
| `fulfillment_status` | `Selection` | `draft`, `split_suggested`, `partially_fulfilled`, `fulfilled` |
| `total_shipments_est` | `Integer` | Estimated total shipments required |
| `estimated_shipping_cost` | `Float` | Computed shipping cost across all split warehouses |
| `has_backorder` | `Boolean` | True if any line requires replenishment stock |
| `has_recurring_lines` | `Boolean` | True if quote contains any subscription product category lines |
| `billing_schedule_ids` | `One2many` | Links to `dealflow.billing.schedule` lines |
| `upsell_suggestion_ids` | `One2many` | Links to `dealflow.quote.upsell` suggestion cards |
| `live_margin_impact` | `Float` | Real-time margin delta preview for proposed upsell items |

### Methods Exposed by Ashrith
| Method Signature | Context / Trigger | Description |
| :--- | :--- | :--- |
| `action_suggest_warehouse_split()` | Header button / Auto on Approval | Evaluates live warehouse stock to generate optimal split plan |
| `action_accept_split()` | Ops user confirms recommended split | Locks in warehouse allocations |
| `action_consolidate_backorder()` | Stock arrival notification | Re-allocates backordered quantities when fresh stock arrives |
| `action_generate_billing_schedule()` | On quote confirmation | Splits one-time items from recurring lines and builds schedule |
| `action_apply_proration(new_qty, effective_date)` | Mid-cycle subscription change | Computes prorated charges / credit notes |
| `action_compute_upsells()` | On quote builder load/line change | Evaluates co-purchase rules and active promotions to surface suggestions |
| `action_add_upsell_to_cart(upsell_id)` | Upsell panel "Add to Quote" | Appends suggested product to `line_ids` and updates margin instantly |

---

## 4. UI / View Separation Contract

In `dealflow.quote` form view (`hackathon_core.view_dealflow_quote_form`):
```xml
<notebook>
    <page name="order_lines" string="Order Lines"> ... </page>
    <page name="notes_page" string="Terms &amp; Notes"> ... </page>
    <!-- AKTHAR adds pages via feature_a_views.xml: -->
    <!-- <page name="page_approvals" string="Approvals &amp; Risk Governance"/> -->
    <!-- <page name="page_deal_health" string="Deal Health &amp; Audit Trail"/> -->

    <!-- ASHRITH adds pages via feature_b_views.xml: -->
    <!-- <page name="page_fulfillment" string="Fulfillment &amp; Warehouses"/> -->
    <!-- <page name="page_subscriptions" string="Subscriptions &amp; Billing Schedules"/> -->
    <!-- <page name="page_upsell" string="Upsell &amp; Cross-Sell Recommendations"/> -->
</notebook>
```
**Strict View Rule**:
- Akthar only uses `<xpath expr="//notebook" position="inside">` with page names starting with `page_akthar_` or `page_approvals_`.
- Ashrith only uses `<xpath expr="//notebook" position="inside">` with page names starting with `page_ashrith_` or `page_fulfillment_`.
- Neither touches header buttons belonging to the other.
