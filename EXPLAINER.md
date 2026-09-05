# 📘 VantageOps Technical Explainer & Native Odoo Gigs Architecture

> **The Definitive Blueprint of the Autonomous B2B Deal Governance & Fulfillment Engine for Odoo 18**

---

## 🧭 1. Executive Summary & The Problem

Enterprise B2B sales teams frequently suffer from three systemic margin leaks:
1. **Rogue Discounting & Margin Bleed**: Sales reps offer unapproved, aggressive discounts to close quarter-end deals without real-time oversight.
2. **Infinite Customer Haggling**: Unstructured offline email negotiations drag sales cycles out and erode deal value.
3. **Fulfillment Stalls & Backorder Bottlenecks**: High-value orders are delayed entirely because a single line item is out of stock in the primary warehouse.

**VantageOps** solves all three problems autonomously inside native Odoo 18.

---

## ⚡ 2. The Core Philosophy: "Native Odoo Gigs"

The primary failure mode in Odoo hackathons is building redundant custom engines. Odoo already possesses world-class messaging (`mail`), inventory routing (`stock`), and portal UI (`portal`).

Our strategy was **"Native Odoo Gigs"**—exploiting high-leverage Odoo framework hooks to deliver massive enterprise capabilities in **under 400 lines of clean Python**.

Here are the **6 core architectural gigs** powering VantageOps:

```
                  ┌──────────────────────────────────────────────────────────┐
                  │                 VANTAGEOPS ARCHITECTURE                  │
                  └──────────────────────────────────────────────────────────┘
                                               │
         ┌─────────────────────────────────────┼────────────────────────────────────┐
         ▼                                     ▼                                    ▼
┌──────────────────┐                 ┌────────────────────┐               ┌──────────────────┐
│   vantage_core   │                 │ vantage_governance │               │vantage_fulfillment│
├──────────────────┤                 ├────────────────────┤               ├──────────────────┤
│• Blended Risk    │                 │• action_confirm    │               │• Auto WH Split   │
│  Math Matrix     │◄────────────────┤  High-Risk Block   │               │• Line Forking    │
│• Approval State  │                 │• mail.activity     │               │• Margin Delta    │
│• Hybrid Contract │                 │  Chatter Tasks     │               │  Upsell Engine   │
│  Detection       │                 │• Portal Negotiate  │               │• Location FreeQty│
└──────────────────┘                 │• Circuit Breaker   │               └──────────────────┘
                                     └────────────────────┘
```

---

### 💡 Gig 1: The Chatter Task Escalation Gig (`mail.activity`)
* **The Traditional (Bad) Approach**: Build custom notification tables, approval queues, email notification crons, and custom inbox views.
* **The VantageOps Gig**: We hook directly into Odoo's native `mail.activity` model. When an order exceeds risk limits, VantageOps calls `self.activity_schedule()`. 
  - The Commercial Director immediately sees a native red/orange activity badge in the Odoo top navbar.
  - Chatter logs an actionable task: *"High-Risk Deal Approval Required"*.
  - When the manager clicks **"Director Approve"**, VantageOps calls `activities.action_feedback()`, automatically resolving the activity with audit trail feedback.

### 💡 Gig 2: The Confirmation Interceptor Gig (`action_confirm` Super-Hook)
* **The Traditional (Bad) Approach**: Completely override the Odoo sales confirmation workflow, breaking third-party addons, invoice generation, and delivery picking triggers.
* **The VantageOps Gig**: We cleanly inherit `sale.order` and wrap `action_confirm()`:
  ```python
  def action_confirm(self):
      for order in self:
          if order.blended_risk_score > 0 and order.risk_approval_state != 'approved':
              order._schedule_manager_approval_activity()
              raise UserError(_("⚠️ High-Risk Deal Blocked by VantageOps!"))
      return super().action_confirm()
  ```
  - If clean $\rightarrow$ `super().action_confirm()` executes natively, triggering stock pickings and invoices normally.
  - If high-risk and unapproved $\rightarrow$ `UserError` halts execution before database mutation, schedules chatter tasks, and alerts the user.

### 💡 Gig 3: The Tokenized Portal Negotiation Gig (QWeb XPath + Route)
* **The Traditional (Bad) Approach**: Build a standalone customer portal using React/Vue, manage separate JWT tokens, and build complex synchronization APIs.
* **The VantageOps Gig**: We extend Odoo's native Customer Portal (`sale.sale_order_portal_content`) with a surgical `<xpath>` template injection and a lightweight HTTP controller:
  - Customers access their quote via standard Odoo secure token URLs (`/my/orders/<id>?access_token=...`).
  - An interactive **Deal Negotiation Portal** card is injected directly above the quotation line items.
  - When a customer enters a counter-discount, the route `/my/orders/<id>/counter_offer` calls `order_sudo.action_customer_counter_offer()`.
  - Recalculates risk in real time, increments negotiation rounds, and writes an audit message to the deal's chatter.

### 💡 Gig 4: The Circuit-Breaker Anti-Haggling Gig
* **The Traditional (Bad) Approach**: Infinite back-and-forth email loops without algorithmic termination boundaries.
* **The VantageOps Gig**: Computed circuit-breaker:
  ```python
  is_negotiation_locked = fields.Boolean(compute='_compute_is_negotiation_locked', store=True)
  
  @api.depends('negotiation_rounds', 'max_negotiation_rounds')
  def _compute_is_negotiation_locked(self):
      for order in self:
          order.is_negotiation_locked = order.negotiation_rounds >= order.max_negotiation_rounds
  ```
  - When rounds hit the limit (default 3), the portal form vanishes and is replaced with a locked badge:
    `🔒 Negotiation Locked: Maximum permitted negotiation rounds (3) reached.`
  - Further counter-offers are rejected with a `UserError` lock.

### 💡 Gig 5: The Multi-Warehouse Stock-Split Forking Gig
* **The Traditional (Bad) Approach**: Manually create multiple quotations or write complex delivery picking algorithms.
* **The VantageOps Gig**: Line-level inventory forking:
  1. Checks real-time free stock at the quotation's specific warehouse location:
     `product.with_context(location=wh.lot_stock_id.id).free_qty`
  2. Flags deficit lines (`requires_split = True`).
  3. Clicking **Split Warehouse Fulfillments**:
     - Truncates the primary line to currently available stock (`product_uom_qty = avail_qty`).
     - Forks a new child line with the deficit quantity, tagged as `is_split_child = True`, assigned to the secondary regional warehouse.
  4. Native Odoo `sale_stock` automatically generates separate `stock.picking` delivery orders per warehouse upon confirmation!

### 💡 Gig 6: The Algorithmic Blended Risk Matrix Gig
* **The Traditional (Bad) Approach**: Fixed single-threshold percentage discounts that ignore deal volume and line-level deviations.
* **The VantageOps Gig**: A weighted multi-factor penalty formula calculated in `< 30` lines:
  - **Worst Line Breach (60% weight)**: Measures the maximum single discount breach beyond the 15% safety ceiling.
  - **Overall Margin Loss (40% weight)**: Total dollar discount given divided by total gross dollar volume.
  - Formula:
    $$\text{Blended Risk Score} = \text{round}((\text{Worst Breach} \times 0.6) + (\text{Margin Loss \%} \times 0.4), 2)$$
  - Immediately drives the approval state machine (`draft` $\rightarrow$ `pending_approval` $\rightarrow$ `approved` / `rejected`).

---

## 🏛️ 3. Repository Architecture & Team Governance

To guarantee zero code regressions and pristine enterprise delivery, the project uses a **Two-Tier Repository Architecture**:

| Repository Tier | Path | Remote URL | Role |
| :--- | :--- | :--- | :--- |
| **Active Canvas** | `/home/gytdrop/.../odoo gujarat` | `https://github.com/gytdrop/mockdeal.git` | Active workspace where all code, testing, logs, and experimental branches live. |
| **Enterprise Release** | `mockdeal/VantageOps` (git-ignored) | `https://github.com/gytdrop/VantageOps.git` | Frozen enterprise destination. Contains ONLY clean modules (`custom_addons`), enterprise README, and zero agent/instruction artifacts. |

### Persona Isolation Rules
* **Akthar (Commercial Control)**: Works strictly inside `custom_addons/vantage_governance/`.
* **Ashrith (Operational Execution)**: Works strictly inside `custom_addons/vantage_fulfillment/`.
* **vantage_core**: Frozen base layer. Zero modifications after baseline.
* **Afteb**: Strictly restricted from touching or pushing to `VantageOps`. All work confined to `mockdeal`.

---

## 📂 4. File-by-File Implementation Index

```
custom_addons/
├── vantage_core/
│   ├── models/sale_order.py        # Core Risk Scoring formula & Hybrid contract detection
│   └── views/vantage_core_views.xml# Base Sales metrics UI
│
├── vantage_governance/             # AKTHAR'S MODULE
│   ├── models/sale_order.py        # action_confirm block, mail.activity scheduling, approval actions
│   ├── views/governance_views.xml  # Header buttons (Approve/Reject) & Risk & Approvals tab
│   ├── views/portal_templates.xml  # QWeb portal counter-offer card & circuit breaker alert
│   └── controllers/portal.py       # Secure HTTP portal counter-offer route
│
└── vantage_fulfillment/            # ASHRITH'S MODULE
    ├── models/sale_order.py        # Warehouse free_qty compute, action_split_fulfillments, margin_delta
    └── views/fulfillment_views.xml # Fulfillment & Warehouses notebook tab & margin contributions
```

---

## 🧪 5. Live Demo Scenarios on Local Odoo (`vantage_db`)

The local environment (running on `http://localhost:8069`) contains 4 seeded demo scenarios:

| Record | Scenario | Risk Score | Approval State | Key Demonstration |
| :--- | :--- | :--- | :--- | :--- |
| **`S00025`** | Clean Deal | `0.0` | `draft` | 0% discount; confirms instantly with zero popup. |
| **`S00026`** | High-Risk Margin Bleed | `25.7` | `pending_approval` | 35% discount; `action_confirm` triggers modal halt & schedules `mail.activity`. Header has **Director Approve**. |
| **`S00027`** | Portal Negotiation | `13.0` | `pending_approval` | Interactive customer portal card allows submitting live counter-discount with chatter log. |
| **`S00028`** | Circuit Breaker Lock | `16.0` | `pending_approval` | 3 rounds completed; form is locked with circuit-breaker warning. |

---

## 🔄 6. Living Explainer Maintenance

To synchronize and update this explainer document at any time:
1. Run `./--keys` or `./keys` in your terminal.
2. Trigger the keyword **`update explainer`**.
3. Antigravity will automatically inspect recent commits, code updates, and log entries to append newly developed capabilities into `EXPLAINER.md`.
