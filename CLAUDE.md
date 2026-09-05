# CLAUDE INSTRUCTION & CONTEXT HANDOFF — DEALFLOW360 (VANTAGEOPS)

> **FOR CLAUDE**: This document gives you full context of the project, what has been built, how to run and upgrade the environment, existing limitations, and what needs to be made versatile.
> Full detailed documentation is in [`README.md`](./README.md). Archived design blueprints are in [`hide/`](./hide).

---

## 1. Quick Environment & Commands
- **Working Directory**: `/home/gytdrop/Documents/HACKATHONS/2026/odoo hackathon/odoo gujarat`
- **Database**: `vantage_db`
- **Odoo Path**: `/home/gytdrop/odoo/odoo-bin`
- **Addons Path**: `/home/gytdrop/odoo/addons,custom_addons`
- **Upgrade All Modules Command**:
  ```bash
  python3 /home/gytdrop/odoo/odoo-bin -d vantage_db -r odoo --addons-path=/home/gytdrop/odoo/addons,custom_addons -u vantage_core,vantage_governance,vantage_fulfillment --stop-after-init
  ```
- **Run Odoo Dev Server**:
  ```bash
  python3 /home/gytdrop/odoo/odoo-bin -d vantage_db -r odoo --addons-path=/home/gytdrop/odoo/addons,custom_addons --dev=reload
  ```
- **Logging Rule**: Whenever you make a commit or complete a task, append an entry to `claude.log` and `workonmyperiod.log`.

---

## 2. Architecture & Ownership
- **No More Persona Silos**: The work division between Akthar, Ashrith, and Aftab is dissolved. You are working directly on the full unified codebase.
- **Active Modules in `custom_addons/`**:
  1. `vantage_core`: Base model extensions on `sale.order` (`blended_risk_score`, `risk_approval_state`, `is_recurring_hybrid`) and top navigation menus.
  2. `vantage_governance`: Customer tiers (`res.partner.customer_tier`), Blended Risk calculation, Two-Tier Approval routing (Manager $\le 10$, Finance $> 10$), `action_confirm` blocking, Customer Portal negotiation with 3-round circuit breaker, and Executive Sales Cockpit (`vantage.sales.dashboard`).
  3. `vantage_fulfillment`: Multi-warehouse cost weighting (`shipping_cost_weight` & `base_shipping_cost` on `stock.warehouse`), stock deficit auto-split (`action_split_fulfillments`), backorder consolidation (`action_consolidate_backorders`), hybrid billing installments (`vantage.billing.schedule`), and live smart upsells (`vantage.upsell.rule`).

---

## 3. What Has Been Completed & Verified
1. **Quotation Builder with Live Margin Delta**: Line-level profit margin (`margin_delta`) updates live as products, quantities, and discounts change.
2. **Turnkey Seed Data & Bundle**:
   - Clicking `⚡ Load Turnkey Seed Data` on the dashboard provisions Bronze, Silver, Gold customers, Main & East warehouses, demo products, and upsells.
   - Quotation Template `DealFlow360 Enterprise Hybrid Bundle` pre-populates 10 Servers, 1 Setup Service, and 1 SaaS Subscription in 1 click.
3. **Discount Governance & Blended Risk**: Excess discount breaches beyond tier ceilings (Bronze 5%, Silver 10%, Gold 15%) trigger positive risk scores.
4. **Approval Routing & Blocking**: Quotes with risk $> 0$ block confirmation and schedule activities. Manager approves up to score 10; score $> 10$ auto-escalates to Finance Director.
5. **Live Smart Upsell Intelligence**: Complementary pairings (e.g. Server $\to$ 24/7 SLA Warranty with +$350 margin) can be added to the cart with 1 click.
6. **Multi-Warehouse Auto-Split & Shipping Cost Weighting**: Deficits split lines between Main Warehouse ($25 base $\times$ 1.0) and East Depot ($60 base $\times$ 2.5) with real-time freight estimation ($175.00).
7. **Backorder Consolidation**: Merges split backorder lines back into a single shipment when inventory arrives.
8. **Hybrid Billing Engine**: Separates one-time hardware delivery charges from 12 monthly subscription billing milestones.
9. **Customer Portal Negotiation**: Interactive customer screen at `/my/orders/<id>` with counter-discount proposals, circuit breaker limit, and auto-approval re-routing.
10. **Executive Sales Cockpit**: Central dashboard tracking pipeline health, stalled deals, margin bleed, and quick-action filters.

---

## 4. Current Limitations (What the System Cannot Do Yet)
1. **2-Warehouse Limit**: Auto-split handles 1 primary warehouse + 1 secondary depot. It cannot do N-way combinatorial bin-packing across 3+ warehouses simultaneously.
2. **Static Subscription Installments**: Generates 12 monthly slots; does not calculate fractional calendar-day proration for mid-cycle seat additions or cancellations.
3. **Heuristic Delivery Slippage**: Stalled status is based on inactivity days, not live picking delivery scheduled dates.
4. **Draft-Stage Stock Reservation**: Stock is read dynamically via `free_qty_today`, but hard stock reservations only occur upon order confirmation.
5. **Payment Gateway**: Portal negotiation confirms orders, but real-time online credit card capture is not hooked to live payment acquirers (uses offline invoice reconciliation).

---

## 5. What We Hardcoded That Needs to Be Versatile
1. **Tier Ceilings**: Currently hardcoded in Python (`sale_order.py`: Bronze=5%, Silver=10%, Gold=15%). Needs a dynamic configuration model or settings view with category-specific ceilings (e.g. Hardware vs Services).
2. **Escalation Thresholds**: Static cutoff at 10.0 points. Needs configurable settings for Manager vs Finance boundaries.
3. **Circuit Breaker Limits**: Static 3 rounds. Needs configurable limits per tier/team.
4. **Subscription Frequency**: Static 12-month division. Needs flexible frequencies (monthly, quarterly, annual) and exact proration math.
5. **Freight Matrix**: Static flat fees and weights. Needs tiered weight tables or carrier grid integration.
