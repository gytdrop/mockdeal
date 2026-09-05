# DealFlow360 (VantageOps) — Master Project Status & Architecture

> **Notice**: All previous siloed design blueprints and split-persona markdown files have been archived into [`hide/`](./hide). 
> This document represents the **single source of truth** for DealFlow360: what is built, current limitations, hardcoded parameters requiring versatility, and the precise roadmap for production readiness.

---

## 1. Executive Summary & Unified Architecture

**DealFlow360** is a self-governing Sales Operations platform built as an extension to native Odoo 17. The system eliminates manual deal reviews and fragmented operations by tying together pricing governance, live upsell intelligence, multi-warehouse fulfillment splitting, hybrid subscription billing, customer portal bargaining, and executive deal health monitoring.

The architecture comprises three native modular layers under `custom_addons/`:
1. **`vantage_core`**: Shared schema extensions on `sale.order` (`blended_risk_score`, `risk_approval_state`, `is_recurring_hybrid`), `sale.order.line` (`is_subscription_item`), and top-level root application menus.
2. **`vantage_governance`**: Two-tier discount approval engine (Manager & Finance Director), `action_confirm` block, `mail.activity` chatter escalations, customer portal counter-offer bargaining with circuit-breaker lock, and the Bootstrap 5 Executive Sales Cockpit (`vantage.sales.dashboard`).
3. **`vantage_fulfillment`**: Multi-warehouse stock deficit engine, logistics shipping cost weighting (`stock.warehouse`), autonomous auto-split & backorder forking (`action_split_fulfillments`), backorder consolidation (`action_consolidate_backorders`), hybrid billing installments (`vantage.billing.schedule`), and live smart upsell pairing (`vantage.upsell.rule`).

---

## 2. What We Have Built Till Now

| Pillar | Implemented Capability | Files / Models |
| :--- | :--- | :--- |
| **Quotation Builder & Margin** | Real-time calculation of net margin contribution (`margin_delta`) on order lines; visual indicator of profitability during quotation drafting. Pre-configured 1-click bundle template. | `custom_addons/vantage_fulfillment/models/sale_order.py`, `sale.order.template` |
| **Discount Governance** | Customer tier classification (`bronze`, `silver`, `gold`) on `res.partner` with editable badge dropdowns. Dynamic Blended Risk Score penalizing excess discount breaches beyond tier limits. | `custom_addons/vantage_governance/models/sale_order.py`, `governance_views.xml` |
| **Approval Routing & Blocking** | `action_confirm()` override: unapproved high-risk deals raise a `UserError` and automatically schedule high-priority `mail.activity` tasks. Two-tier sign-off: Manager ($\le 10$) and Finance Director ($> 10$). | `custom_addons/vantage_governance/models/sale_order.py` |
| **Live Smart Upsell Engine** | `vantage.upsell.rule` pairing complementary products with minimum margin thresholds. Live recommendation tab shows estimated profit delta with 1-click "Add to Quote". | `custom_addons/vantage_fulfillment/models/upsell_rule.py`, `fulfillment_views.xml` |
| **Multi-Warehouse Auto-Split** | Real-time available stock checking against primary warehouse. Autonomous line splitting truncating local fulfilled quantity and forking deficit to secondary depot. | `custom_addons/vantage_fulfillment/models/sale_order.py`, `fulfillment_views.xml` |
| **Shipping Cost Weighting** | Extended `stock.warehouse` with `shipping_cost_weight` (distance factor) and `base_shipping_cost`. System computes estimated shipment count and total freight costs across legs. | `custom_addons/vantage_fulfillment/models/sale_order.py` |
| **Backorder Consolidation** | `action_consolidate_backorders()`: Recombines child backorder split lines back into the primary shipment when stock arrives to minimize carrier costs. | `custom_addons/vantage_fulfillment/models/sale_order.py` |
| **Hybrid Billing Engine** | `vantage.billing.schedule`: Separates one-time hardware/delivery charges from 12 recurring monthly subscription installments, with milestone invoicing actions. | `custom_addons/vantage_fulfillment/models/billing_schedule.py` |
| **Customer Portal Negotiation** | Dedicated `/my/orders/<id>` portal interface. Customers can pitch line-level counter discounts. Protected by a 3-round circuit breaker; auto-reroutes to approval if counter exceeds limits. | `custom_addons/vantage_governance/controllers/portal.py`, `portal_templates.xml` |
| **Executive Sales Cockpit** | Full-width Bootstrap 5 dashboard (`vantage.sales.dashboard`) tracking total pipeline value, healthy/stalled deals, pending approvals, and quick-action drilldowns. | `custom_addons/vantage_governance/models/vantage_dashboard.py`, `dashboard_views.xml` |
| **1-Click Turnkey Seed Data** | Executive dashboard button (`⚡ Load Turnkey Seed Data`) instantly provisioning Bronze/Silver/Gold accounts, Main & East warehouses, stock quants, demo products, and upsell pairings. | `custom_addons/vantage_governance/models/vantage_dashboard.py` |

---

## 3. Current Limitations of Our Project

Despite strong end-to-end functionality, several operational boundaries currently exist:

1. **Two-Warehouse Split Topology**:
   - *Current State*: The auto-split engine evaluates stock between the quotation's primary warehouse and one selected secondary warehouse.
   - *Limitation*: If an order requires splitting across 3 or more regional depots (e.g., Main WH, East Depot, and West Hub), the algorithm currently only forks into a single child depot line.
2. **Static Subscription Installment Cadence**:
   - *Current State*: The billing schedule engine assumes an annual contract divided into 12 equal monthly milestones.
   - *Limitation*: It does not natively support non-monthly cycles (quarterly, semi-annual, biennial) or mid-cycle seat change proration math (e.g. adding 5 licenses halfway through month 3).
3. **Delivery Promise Slippage Is Heuristic**:
   - *Current State*: Deal Health flags deals as `stalled` based on `days_inactive > 3`.
   - *Limitation*: It does not directly compare `commitment_date` against real-time `stock.picking` scheduled dates to detect operational logistics delays.
4. **Draft-Stage Stock Awareness**:
   - *Current State*: Stock availability is read in real-time via `free_qty_today`.
   - *Limitation*: It does not reserve inventory at quotation drafting; formal stock reservation only occurs once the sales order is confirmed into state `sale`.
5. **Simulated Portal Payment**:
   - *Current State*: The customer portal allows counter-proposals and final acceptance.
   - *Limitation*: Online payment capture requires configuring a payment acquirer/provider (Stripe/PayPal test credentials) rather than native offline invoice reconciliation.

---

## 4. What We Hardcoded That Needs to Be Versatile

To achieve full commercial versatility, the following hardcoded elements must be externalized into configurable models and settings:

### 1. Customer Tier Discount Ceilings
* **What is hardcoded**: In `custom_addons/vantage_governance/models/sale_order.py`, discount ceilings are hardcoded inside `_compute_vantage_risk()`:
  - Bronze: fixed at 5.0%
  - Silver: fixed at 10.0%
  - Gold: fixed at 15.0%
* **What it needs to do**: 
  - Create a dedicated model `dealflow.discount.tier` (or Odoo ResConfigSettings) allowing administrators to add arbitrary tiers (e.g. Platinum, Distributor, Government) and define discount ceiling percentages per tier.
  - Support category-specific discount ceilings (e.g., Gold customer gets 15% on Hardware, but only 10% on thin-margin Services).

### 2. Risk Score Escalation Thresholds
* **What is hardcoded**: 
  - Score $\le 0$: Approved / Draft (Clean)
  - $0 < \text{Score} \le 10$: Frontline Sales Manager
  - $\text{Score} > 10$: Auto-escalates to Finance Director
* **What it needs to do**:
  - Make approval threshold numbers configurable via Sales Settings so companies with higher risk tolerance can adjust the Manager/Finance boundary (e.g. up to 15 points for Manager).

### 3. Circuit-Breaker Negotiation Limits
* **What is hardcoded**: 
  - Max counter-offer rounds is hardcoded to 3 (or 5) on `sale.order`.
* **What it needs to do**:
  - Allow negotiation limits to be defined per customer tier or sales team (e.g. VIP Gold deals permit 5 rounds, while standard inbound deals permit only 2 rounds).

### 4. Subscription Plan Billing Cycles & Proration
* **What is hardcoded**:
  - In `action_generate_billing_schedule()`, billing generates strictly 12 monthly periods dividing recurring amounts by 12.
* **What it needs to do**:
  - Add recurring frequency to products (`monthly`, `quarterly`, `annual`).
  - Calculate exact calendar-day proration when recurring subscription lines are modified mid-billing cycle.

### 5. Warehouse Shipping Matrix
* **What is hardcoded**:
  - Flat base freight costs ($25 / $60) and static weights (1.0x / 2.5x).
* **What it needs to do**:
  - Support tiered weight brackets based on total order weight (kg) or integrate with standard Odoo delivery carrier grids.

---

## 5. Verification Checklist & Demo Guide

### Turnkey Verification Steps:
1. Open **VantageOps > Dashboard** $\to$ Click **`⚡ Load Turnkey Seed Data`**.
2. Go to **Quotations** $\to$ Create new quote for **Acme Corp (Bronze Tier)**.
3. Select Quotation Template: **`DealFlow360 Enterprise Hybrid Bundle`** (loads 10 Servers, 1 Setup Service, 1 SaaS License).
4. Review **Fulfillment & Warehouses** tab:
   - Primary stock: 5 units available. Deficit: 5 units.
   - Live shipping calculation shows: **2 shipments / $175.00** (`Main: $25` + `East: $150`).
5. Click **"Auto-Split Warehouses"**:
   - Order line splits: 5 units Main Warehouse, 5 units backorder East Depot.
6. Pitch **18% Discount**:
   - Risk score jumps to `13.0` (exceeds Bronze 5% limit by 13 points).
   - Approval state transitions to `pending_manager`. Confirmation is blocked.
7. Switch to **Smart Upsells** tab:
   - Click **"Add to Quote"** on `24/7 SLA Warranty` $\to$ instant +$350 margin increase.
8. Switch to **Hybrid Billing Schedule** tab:
   - Click **"Generate Billing Schedule"** $\to$ separates immediate hardware charges from 12 monthly subscription installments.
9. Executive Sign-Off:
   - Click **Manager Approve** $\to$ auto-escalates to `pending_finance` (since score > 10).
   - Click **Finance Approve** $\to$ state becomes `approved`.
   - Click **Confirm** $\to$ Order confirms successfully!
