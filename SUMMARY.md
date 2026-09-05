# 🗺️ VantageOps: System Map, Page Directory & Destined File Locations

> **Quick-reference handbook for Akthar: All UI page names, tabs, backend headers, portal routes, and exact file paths across `mockdeal` and `VantageOps`.**

---

## 📑 Table of Contents
1. [VantageOps Standalone Root App & Header Navigation](#1-vantageops-standalone-root-app--header-navigation)
2. [Executive Sales Cockpit (Dashboard)](#2-executive-sales-cockpit-dashboard)
3. [Backend Odoo UI: Quotation Tabs, Fields & File Locations](#3-backend-odoo-ui-quotation-tabs-fields--file-locations)
4. [Backend Odoo UI: Header Buttons, Alerts & Code Locations](#4-backend-odoo-ui-header-buttons-alerts--code-locations)
5. [Customer Portal & Public Access: Pages, Views & Controller Locations](#5-customer-portal--public-access-pages-views--controller-locations)
6. [Destined File Mapping: Mockdeal Canvas ➔ VantageOps Destination](#6-destined-file-mapping-mockdeal-canvas--vantageops-destination)
7. [Confirmed Python, XML & Security Source Code Inventory (All 26 Production Files)](#7-confirmed-python-xml--security-source-code-inventory-all-26-production-files)
8. [Repository Artifacts & Documentation Directory](#8-repository-artifacts--documentation-directory)
9. [Keywords & Living Update Instructions](#9-keywords--living-update-instructions)

---

## 🚀 1. VantageOps Standalone Root App & Header Navigation

VantageOps is deployed as an independent top-level application in Odoo's 9-grid app switcher (`menus.xml`), giving leadership and sales operations an uncluttered panoramic workspace with 9 integrated header tabs:

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│ 🌐 VantageOps  │ Dashboard │ Quotations │ Approvals │ Fulfillment │ Subscriptions │ Invoices ... │
└──────────────────────────────────────────────────────────────────────────────────────────────────┘
```

* **Menu Definition File**: [`custom_addons/vantage_core/views/menus.xml`](file:///home/gytdrop/Documents/HACKATHONS/2026/odoo%20hackathon/odoo%20gujarat/custom_addons/vantage_core/views/menus.xml)
* **Root Application**: `menu_vantage_root` (Icon: custom brand icon in 9-grid)
* **Navbar Categories**:
  1. `Dashboard`: Opens the Executive Sales Cockpit (`action_vantage_sales_dashboard`).
  2. `Quotations`: Direct list/kanban of all active commercial quotes (`sale.action_quotations_with_onboarding`).
  3. `Approvals`: Filtered action displaying deals requiring Manager or Finance sign-off.
  4. `Fulfillment`: Logistics routing views and delivery orders (`stock.action_picking_tree_all`).
  5. `Subscriptions`: Hybrid contracts and milestone billing installment schedules.
  6. `Invoices`: Direct access to customer account move records.
  7. `Deal Health`: Pipeline inspection filtered by stalled deals and margin bleed.
  8. `Reports`: Sales analysis and performance pivot reports.
  9. `Products`: Master catalog with direct link to Smart Upsell Rules (`menu_vantage_upsell_rules`).

---

## 📊 2. Executive Sales Cockpit (Dashboard)

A full-width, Bootstrap 5-powered command dashboard ([`vantage.sales.dashboard`](file:///home/gytdrop/Documents/HACKATHONS/2026/odoo%20hackathon/odoo%20gujarat/custom_addons/vantage_governance/models/vantage_dashboard.py)) designed for Sales VPs, Commercial Directors, and Operations Leads:

* **View Source File**: [`custom_addons/vantage_governance/views/dashboard_views.xml`](file:///home/gytdrop/Documents/HACKATHONS/2026/odoo%20hackathon/odoo%20gujarat/custom_addons/vantage_governance/views/dashboard_views.xml)
* **Model Source File**: [`custom_addons/vantage_governance/models/vantage_dashboard.py`](file:///home/gytdrop/Documents/HACKATHONS/2026/odoo%20hackathon/odoo%20gujarat/custom_addons/vantage_governance/models/vantage_dashboard.py)
* **Layout Highlights**:
  - **Full-Width Viewport**: Employs `.p-4 .w-100` and disables fixed-width `<sheet>` centering. Native `.o_control_panel` breadcrumbs are cleanly suppressed for a sleek header.
  - **Metric Cards**: Thick 5px accent borders (`border-primary`, `border-success`, `border-warning`, `border-danger`, `border-info`).
  - **Live Counters**: Pipeline Gross Value, Average Deal Size, Critical Margin Bleed, Pending Manager/Finance Approvals, and MRR Pipeline.
  - **Live Chatter Activity Feed**: Inlines real-time message stream with colored status pill badges directly from `mail.message`.
  - **One-Click Quick Action Bar**: Instant triggers for "New Quotation", "Review Approvals", "Generate Billing", and "Upsell Catalog".

---

## 🖥️ 3. Backend Odoo UI: Quotation Tabs, Fields & File Locations

When viewing a Quotation or Sales Order in Odoo ([`sale.view_order_form`](http://localhost:8069/web#id=26&model=sale.order&view_type=form)), the central `<notebook>` contains five specialized tabs:

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│ [Order Lines] [Risk & Approvals] [Fulfillment] [Hybrid Billing Schedule] [Smart Upsells]         │
└──────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### 1️⃣ Tab: `Order Lines` (`name="order_lines"`)
* **Belongs to**: Native Odoo + `vantage_fulfillment` extension
* **View Source File**: [`custom_addons/vantage_fulfillment/views/fulfillment_views.xml:L24-29`](file:///home/gytdrop/Documents/HACKATHONS/2026/odoo%20hackathon/odoo%20gujarat/custom_addons/vantage_fulfillment/views/fulfillment_views.xml#L24-L29)
* **Model Source File**: [`custom_addons/vantage_fulfillment/models/sale_order.py:L70-91`](file:///home/gytdrop/Documents/HACKATHONS/2026/odoo%20hackathon/odoo%20gujarat/custom_addons/vantage_fulfillment/models/sale_order.py#L70-L91)
* **Purpose**: Primary quotation workspace where line items are priced and discounted.
* **Injected Columns & Locations**:
  - `Margin ($)` (`margin_delta`): Real-time dollar profit contribution per line (`price_subtotal - standard_cost`). Defined in `vantage_fulfillment/models/sale_order.py:L86`.
  - `Free Stock` (`free_qty_today`): Available stock in the primary warehouse. Defined in `vantage_fulfillment/models/sale_order.py:L72`.
  - `Fulfillment Warehouse` (`fulfillment_warehouse_id`): Assigned depot for the line. Defined in `vantage_fulfillment/models/sale_order.py:L84`.

---

### 2️⃣ Tab: `Risk & Approvals` (`name="page_akthar_approvals"`)
* **Belongs to**: **Akthar** (`custom_addons/vantage_governance`)
* **View Source File**: [`custom_addons/vantage_governance/views/governance_views.xml:L17-32`](file:///home/gytdrop/Documents/HACKATHONS/2026/odoo%20hackathon/odoo%20gujarat/custom_addons/vantage_governance/views/governance_views.xml#L17-L32)
* **Model Source File**: [`custom_addons/vantage_governance/models/sale_order.py:L7-20`](file:///home/gytdrop/Documents/HACKATHONS/2026/odoo%20hackathon/odoo%20gujarat/custom_addons/vantage_governance/models/sale_order.py#L7-L20) & [`vantage_core/models/sale_order.py:L6-18`](file:///home/gytdrop/Documents/HACKATHONS/2026/odoo%20hackathon/odoo%20gujarat/custom_addons/vantage_core/models/sale_order.py#L6-L18)
* **Purpose**: Commercial governance cockpit. Centralizes profitability metrics, approval state, and customer negotiation logs.
* **Fields & Defining Locations**:
  - `blended_risk_score`: Computed risk metric. Defined in `vantage_core/models/sale_order.py:L6`.
  - `risk_approval_state`: Selection status (`draft`, `pending_approval`, `approved`, `rejected`). Defined in `vantage_core/models/sale_order.py:L13`.
  - `negotiation_rounds`: Integer count of counter-offers. Defined in `vantage_governance/models/sale_order.py:L7`.
  - `max_negotiation_rounds`: Circuit breaker threshold (default: 3). Defined in `vantage_governance/models/sale_order.py:L8`.
  - `is_negotiation_locked`: Boolean circuit breaker status. Defined in `vantage_governance/models/sale_order.py:L9`.
  - `last_counter_offer`: Latest customer counter-offer text. Defined in `vantage_governance/models/sale_order.py:L14`.

---

### 3️⃣ Tab: `Fulfillment & Warehouses` (`name="page_ashrith_fulfillment"`)
* **Belongs to**: **Ashrith** (`custom_addons/vantage_fulfillment`)
* **View Source File**: [`custom_addons/vantage_fulfillment/views/fulfillment_views.xml`](file:///home/gytdrop/Documents/HACKATHONS/2026/odoo%20hackathon/odoo%20gujarat/custom_addons/vantage_fulfillment/views/fulfillment_views.xml)
* **Model Source File**: [`custom_addons/vantage_fulfillment/models/sale_order.py`](file:///home/gytdrop/Documents/HACKATHONS/2026/odoo%20hackathon/odoo%20gujarat/custom_addons/vantage_fulfillment/models/sale_order.py)
* **Purpose**: Operational logistics and multi-warehouse routing.
* **Fields & Defining Locations**:
  - `has_split_requirement`: Deficit indicator. Defined in `vantage_fulfillment/models/sale_order.py`.
  - `secondary_warehouse_id`: Backorder destination warehouse. Defined in `vantage_fulfillment/models/sale_order.py`.

---

### 4️⃣ Tab: `Hybrid Billing Schedule` (`name="page_billing_schedule"`)
* **Belongs to**: **Ashrith** (`custom_addons/vantage_fulfillment`)
* **View Source File**: [`custom_addons/vantage_fulfillment/views/fulfillment_views.xml`](file:///home/gytdrop/Documents/HACKATHONS/2026/odoo%20hackathon/odoo%20gujarat/custom_addons/vantage_fulfillment/views/fulfillment_views.xml)
* **Model Source File**: [`custom_addons/vantage_fulfillment/models/billing_schedule.py`](file:///home/gytdrop/Documents/HACKATHONS/2026/odoo%20hackathon/odoo%20gujarat/custom_addons/vantage_fulfillment/models/billing_schedule.py)
* **Purpose**: Milestone and installment schedule for mixed hardware + subscription contracts.
* **Fields & Defining Locations**:
  - `billing_schedule_ids`: Relation to `vantage.billing.schedule`.
  - `billing_type`: One-time Hardware vs Recurring SaaS.
  - `billing_date`: Milestone billing schedule date.
  - `amount`: Scheduled amount per installment period.
  - `state`: Status badge (`scheduled`, `invoiced`, `cancelled`) with 1-click `action_mark_invoiced`.

---

### 5️⃣ Tab: `Smart Upsells` (`name="page_smart_upsell"`)
* **Belongs to**: **Ashrith** (`custom_addons/vantage_fulfillment`)
* **View Source File**: [`custom_addons/vantage_fulfillment/views/fulfillment_views.xml`](file:///home/gytdrop/Documents/HACKATHONS/2026/odoo%20hackathon/odoo%20gujarat/custom_addons/vantage_fulfillment/views/fulfillment_views.xml)
* **Model Source File**: [`custom_addons/vantage_fulfillment/models/upsell_rule.py`](file:///home/gytdrop/Documents/HACKATHONS/2026/odoo%20hackathon/odoo%20gujarat/custom_addons/vantage_fulfillment/models/upsell_rule.py)
* **Purpose**: Real-time margin expansion recommendations based on active cart products.
* **Fields & Actions**:
  - `available_upsell_ids`: Dynamic pairings matched to active quote items.
  - `margin_contribution`: Net profit impact (`list_price - cost`).
  - `action_apply_upsell`: Single-click button injecting the recommended accessory directly into the quotation.

---

## 🔘 2. Backend Odoo UI: Header Buttons, Alerts & Code Locations

### Header Action Buttons (`<header>`)
| Button Name | Technical Identifier | View Definition Location | Python Logic Location | What It Does |
| :--- | :--- | :--- | :--- | :--- |
| **Confirm** | `action_confirm` | Native Odoo `sale.view_order_form` | [`vantage_governance/models/sale_order.py`](file:///home/gytdrop/Documents/HACKATHONS/2026/odoo%20hackathon/odoo%20gujarat/custom_addons/vantage_governance/models/sale_order.py) | Validates deal; intercepted to raise `UserError` and schedule Chatter task if risk score > 0 and unapproved. |
| **Manager Approve** | `action_manager_approve` | [`vantage_governance/views/governance_views.xml`](file:///home/gytdrop/Documents/HACKATHONS/2026/odoo%20hackathon/odoo%20gujarat/custom_addons/vantage_governance/views/governance_views.xml) | [`vantage_governance/models/sale_order.py`](file:///home/gytdrop/Documents/HACKATHONS/2026/odoo%20hackathon/odoo%20gujarat/custom_addons/vantage_governance/models/sale_order.py) | Tier-1 sign-off. If risk $\le 10$, approves. If risk $> 10$, auto-escalates to Finance Director! |
| **Finance Approve** | `action_finance_approve` | [`vantage_governance/views/governance_views.xml`](file:///home/gytdrop/Documents/HACKATHONS/2026/odoo%20hackathon/odoo%20gujarat/custom_addons/vantage_governance/views/governance_views.xml) | [`vantage_governance/models/sale_order.py`](file:///home/gytdrop/Documents/HACKATHONS/2026/odoo%20hackathon/odoo%20gujarat/custom_addons/vantage_governance/models/sale_order.py) | Tier-2 final sign-off for severe margin violations ($> 10.0$ score). |
| **Reject Deal** | `action_manager_reject` | [`vantage_governance/views/governance_views.xml`](file:///home/gytdrop/Documents/HACKATHONS/2026/odoo%20hackathon/odoo%20gujarat/custom_addons/vantage_governance/views/governance_views.xml) | [`vantage_governance/models/sale_order.py`](file:///home/gytdrop/Documents/HACKATHONS/2026/odoo%20hackathon/odoo%20gujarat/custom_addons/vantage_governance/models/sale_order.py) | Sets `risk_approval_state = 'rejected'`, closes activities, and logs rejection in Chatter. |
| **Nudge Rep** | `action_nudge_rep` | [`vantage_governance/views/governance_views.xml`](file:///home/gytdrop/Documents/HACKATHONS/2026/odoo%20hackathon/odoo%20gujarat/custom_addons/vantage_governance/views/governance_views.xml) | [`vantage_governance/models/sale_order.py`](file:///home/gytdrop/Documents/HACKATHONS/2026/odoo%20hackathon/odoo%20gujarat/custom_addons/vantage_governance/models/sale_order.py) | Dispatches reminder task to sales rep for quotes stalled $>3$ days or having discount anomalies. |
| **Generate Billing Schedule** | `action_generate_billing_schedule` | [`vantage_fulfillment/views/fulfillment_views.xml`](file:///home/gytdrop/Documents/HACKATHONS/2026/odoo%20hackathon/odoo%20gujarat/custom_addons/vantage_fulfillment/views/fulfillment_views.xml) | [`vantage_fulfillment/models/sale_order.py`](file:///home/gytdrop/Documents/HACKATHONS/2026/odoo%20hackathon/odoo%20gujarat/custom_addons/vantage_fulfillment/models/sale_order.py) | Autonomously creates 1-time hardware invoice + 12 monthly subscription billing milestones. |
| **Auto-Split Warehouses** | `action_split_fulfillments` | [`vantage_fulfillment/views/fulfillment_views.xml`](file:///home/gytdrop/Documents/HACKATHONS/2026/odoo%20hackathon/odoo%20gujarat/custom_addons/vantage_fulfillment/views/fulfillment_views.xml) | [`vantage_fulfillment/models/sale_order.py`](file:///home/gytdrop/Documents/HACKATHONS/2026/odoo%20hackathon/odoo%20gujarat/custom_addons/vantage_fulfillment/models/sale_order.py) | Truncates primary line and forks child line routed to secondary warehouse. |
| **Customer Preview** | `action_preview_sale_order` | Native Odoo `sale.view_order_form` | Native `addons/sale/models/sale_order.py` | Opens authentic customer portal view in current browser. |

---

### Dynamic Sheet Banners (Above Form Sheet)
* 🔴 **Red Alert (`alert-danger`)**:
  - *Location*: [`custom_addons/vantage_core/views/vantage_core_views.xml:L10-15`](file:///home/gytdrop/Documents/HACKATHONS/2026/odoo%20hackathon/odoo%20gujarat/custom_addons/vantage_core/views/vantage_core_views.xml#L10-L15)
  - *Message*: `⚠️ High-Risk Deal Detected: Blended Risk Score is [X]. Commercial approval required before confirmation.`
* 🔵 **Blue Alert (`alert-info`)**:
  - *Location*: [`custom_addons/vantage_core/views/vantage_core_views.xml:L16-19`](file:///home/gytdrop/Documents/HACKATHONS/2026/odoo%20hackathon/odoo%20gujarat/custom_addons/vantage_core/views/vantage_core_views.xml#L16-L19)
  - *Message*: `🔄 Hybrid Deal: Contains both one-time products and recurring subscription contracts.`
* 🟡 **Yellow Alert (`alert-warning`)**:
  - *Location*: [`custom_addons/vantage_fulfillment/views/fulfillment_views.xml:L15-21`](file:///home/gytdrop/Documents/HACKATHONS/2026/odoo%20hackathon/odoo%20gujarat/custom_addons/vantage_fulfillment/views/fulfillment_views.xml#L15-L21)
  - *Message*: `📦 Inventory Deficit Detected: Primary warehouse stock is insufficient. Click "Auto-Split Warehouses"...`

---

## 🌐 5. Customer Portal & Public Access: Pages, Views & Controller Locations

| URL / Route | Component | XML / Python File Location | Purpose & Experience |
| :--- | :--- | :--- | :--- |
| **`/web/login`** | Sign In & Onboarding | Native Odoo + `website.auth_signup_uninvited='b2c'` | Login portal equipped with direct **Sign Up** button for instant customer registration. |
| **`/web/signup`** | Customer Registration | Native Odoo `auth_signup` | Frictionless self-service customer portal onboarding. |
| **`/my` & `/my/home`** | Portal Dashboard | Native Odoo `addons/portal/` | Panoramic overview of customer quotes, orders, and invoices. |
| **`/my/quotes`** | Quotation List | Native Odoo `addons/sale/` | Summary of quotations awaiting customer review. |
| **`/my/orders/<id>`** | Order Portal Detail | Native `addons/sale/views/sale_portal_templates.xml` | Full interactive customer quotation canvas. |
| *(Inside Portal)* | **Deal Negotiation Card** | [`custom_addons/vantage_governance/views/portal_templates.xml:L6-26`](file:///home/gytdrop/Documents/HACKATHONS/2026/odoo%20hackathon/odoo%20gujarat/custom_addons/vantage_governance/views/portal_templates.xml#L6-L26) | Injected card allowing customer to submit counter-discount % and concession remarks. |
| *(Inside Portal)* | **Circuit Breaker Alert** | [`custom_addons/vantage_governance/views/portal_templates.xml:L28-30`](file:///home/gytdrop/Documents/HACKATHONS/2026/odoo%20hackathon/odoo%20gujarat/custom_addons/vantage_governance/views/portal_templates.xml#L28-L30) | Banner informing customer that maximum rounds (3) have been reached and deal terms are locked. |
| **`POST /my/orders/<id>/counter_offer`** | Counter-Offer API | [`custom_addons/vantage_governance/controllers/portal.py:L7-24`](file:///home/gytdrop/Documents/HACKATHONS/2026/odoo%20hackathon/odoo%20gujarat/custom_addons/vantage_governance/controllers/portal.py#L7-L24) | Validates token, calls `action_customer_counter_offer()`, recalculates risk, and posts Chatter card. |

---

## 🚚 6. Destined File Mapping: Mockdeal Canvas ➔ VantageOps Destination

| Component / File | Location in `mockdeal` (Canvas) | Destined Location in `VantageOps` (Release) | Status / Rule |
| :--- | :--- | :--- | :--- |
| **Shared Core Addon** | `custom_addons/vantage_core/` | `VantageOps/custom_addons/vantage_core/` | ✅ **Mirrored & Clean** |
| **Akthar Governance Addon** | `custom_addons/vantage_governance/` | `VantageOps/custom_addons/vantage_governance/` | ✅ **Mirrored & Clean** |
| **Ashrith Fulfillment Addon** | `custom_addons/vantage_fulfillment/` | `VantageOps/custom_addons/vantage_fulfillment/` | ✅ **Mirrored & Clean** |
| **Enterprise README** | `README.md` (Canvas version) | `VantageOps/README.md` (Enterprise clean version) | ✅ **Clean Enterprise Live** |
| **Git Exclusion Rules** | `.gitignore` | `VantageOps/.gitignore` | ✅ **Clean Enterprise Live** |
| **Judge Recipe Book** | [`EXPLAINER.md`](file:///home/gytdrop/Documents/HACKATHONS/2026/odoo%20hackathon/odoo%20gujarat/EXPLAINER.md) | *Canvas only (or optional promotion)* | 🏠 Kept in `mockdeal` |
| **System & Page Map** | [`SUMMARY.md`](file:///home/gytdrop/Documents/HACKATHONS/2026/odoo%20hackathon/odoo%20gujarat/SUMMARY.md) | *Canvas only (or optional promotion)* | 🏠 Kept in `mockdeal` |
| **Command Palette & Helpers** | [`KEYS.md`](file:///home/gytdrop/Documents/HACKATHONS/2026/odoo%20hackathon/odoo%20gujarat/KEYS.md), `./--keys`, `./keys` | *Excluded from VantageOps* | 🚫 Canvas only |
| **Team Governance Rules** | [`AGENTS.md`](file:///home/gytdrop/Documents/HACKATHONS/2026/odoo%20hackathon/odoo%20gujarat/AGENTS.md), [`CONTRACT.md`](file:///home/gytdrop/Documents/HACKATHONS/2026/odoo%20hackathon/odoo%20gujarat/CONTRACT.md), [`EXECUTION_PLAN.md`](file:///home/gytdrop/Documents/HACKATHONS/2026/odoo%20hackathon/odoo%20gujarat/EXECUTION_PLAN.md) | *Excluded from VantageOps* | 🚫 Canvas only |
| **Agent & Period Logs** | `antigravity.log`, `workonmyperiod.log` | *Excluded from VantageOps* | 🚫 Canvas only |

---

## 📜 7. Confirmed Python, XML & Security Source Code Inventory (All 26 Production Files)

All 26 production files have been compiled, syntax-validated, and confirmed working on local Odoo (`vantage_db` on port 8069).

### 📦 Summary by File Type & Line Count
* **Total Confirmed Files**: 26
* **Python Files**: 17 files
* **XML Files**: 7 files
* **Security CSV**: 2 files
* **Total Custom Addon Lines**: ~1,530 lines *(Delivering full enterprise DealFlow360 scope!)*

---

### 1️⃣ Module: `vantage_core` (Base Foundation) — 6 Files
| File Path | Type | Lines | Purpose & Key Classes / Records |
| :--- | :--- | :--- | :--- |
| [`custom_addons/vantage_core/__init__.py`](file:///home/gytdrop/Documents/HACKATHONS/2026/odoo%20hackathon/odoo%20gujarat/custom_addons/vantage_core/__init__.py) | Python Init | 1 | Imports `models` package. |
| [`custom_addons/vantage_core/__manifest__.py`](file:///home/gytdrop/Documents/HACKATHONS/2026/odoo%20hackathon/odoo%20gujarat/custom_addons/vantage_core/__manifest__.py) | Manifest | 17 | Module declaration, dependencies (`sale_management`, `mail`), view & menu registration. |
| [`custom_addons/vantage_core/models/__init__.py`](file:///home/gytdrop/Documents/HACKATHONS/2026/odoo%20hackathon/odoo%20gujarat/custom_addons/vantage_core/models/__init__.py) | Python Init | 1 | Imports `sale_order`. |
| [`custom_addons/vantage_core/models/sale_order.py`](file:///home/gytdrop/Documents/HACKATHONS/2026/odoo%20hackathon/odoo%20gujarat/custom_addons/vantage_core/models/sale_order.py) | Python Model | 92 | Implements base `_compute_vantage_risk` formula, `risk_approval_state` transitions, and `_compute_is_recurring_hybrid` contract detection. |
| [`custom_addons/vantage_core/views/menus.xml`](file:///home/gytdrop/Documents/HACKATHONS/2026/odoo%20hackathon/odoo%20gujarat/custom_addons/vantage_core/views/menus.xml) | Menu XML | 68 | Defines top-level VantageOps Root Application in 9-grid menu with navbar tabs (Dashboard, Quotations, Approvals, Fulfillment, Subscriptions, Invoices, Deal Health, Reports, Products). |
| [`custom_addons/vantage_core/views/vantage_core_views.xml`](file:///home/gytdrop/Documents/HACKATHONS/2026/odoo%20hackathon/odoo%20gujarat/custom_addons/vantage_core/views/vantage_core_views.xml) | Form XML | 37 | Injects red high-risk alert, blue hybrid banner, and sheet badges (`blended_risk_score`, `risk_approval_state`). |

---

### 2️⃣ Module: `vantage_governance` (Akthar: Commercial Control) — 12 Files
| File Path | Type | Lines | Purpose & Key Classes / Records |
| :--- | :--- | :--- | :--- |
| [`custom_addons/vantage_governance/__init__.py`](file:///home/gytdrop/Documents/HACKATHONS/2026/odoo%20hackathon/odoo%20gujarat/custom_addons/vantage_governance/__init__.py) | Python Init | 2 | Imports `models` and `controllers`. |
| [`custom_addons/vantage_governance/__manifest__.py`](file:///home/gytdrop/Documents/HACKATHONS/2026/odoo%20hackathon/odoo%20gujarat/custom_addons/vantage_governance/__manifest__.py) | Manifest | 22 | Module metadata, dependencies (`vantage_core`, `portal`, `mail`), security, data & view loading. |
| [`custom_addons/vantage_governance/models/__init__.py`](file:///home/gytdrop/Documents/HACKATHONS/2026/odoo%20hackathon/odoo%20gujarat/custom_addons/vantage_governance/models/__init__.py) | Python Init | 2 | Imports `sale_order` and `vantage_dashboard`. |
| [`custom_addons/vantage_governance/models/sale_order.py`](file:///home/gytdrop/Documents/HACKATHONS/2026/odoo%20hackathon/odoo%20gujarat/custom_addons/vantage_governance/models/sale_order.py) | Python Model | 249 | Customer Tiers (`res.partner.customer_tier`), Two-Tier Approval (`action_manager_approve`, `action_finance_approve`), Deal Health & Anomaly (`_compute_deal_health`), Rep Nudge (`action_nudge_rep`), and Portal counter-offers. |
| [`custom_addons/vantage_governance/models/vantage_dashboard.py`](file:///home/gytdrop/Documents/HACKATHONS/2026/odoo%20hackathon/odoo%20gujarat/custom_addons/vantage_governance/models/vantage_dashboard.py) | Python Model | 227 | `vantage.sales.dashboard`: Computes real-time executive KPIs (pipeline volume, healthy/stalled/bleed counts, approval queues, subscription MRR, fulfillment split alerts, and HTML live activity feed). |
| [`custom_addons/vantage_governance/controllers/__init__.py`](file:///home/gytdrop/Documents/HACKATHONS/2026/odoo%20hackathon/odoo%20gujarat/custom_addons/vantage_governance/controllers/__init__.py) | Python Init | 1 | Imports `portal`. |
| [`custom_addons/vantage_governance/controllers/portal.py`](file:///home/gytdrop/Documents/HACKATHONS/2026/odoo%20hackathon/odoo%20gujarat/custom_addons/vantage_governance/controllers/portal.py) | Python Controller | 23 | Public HTTP endpoint `/my/orders/<id>/counter_offer` validating tokens and routing counter discounts. |
| [`custom_addons/vantage_governance/views/governance_views.xml`](file:///home/gytdrop/Documents/HACKATHONS/2026/odoo%20hackathon/odoo%20gujarat/custom_addons/vantage_governance/views/governance_views.xml) | Form & Tree XML | 100 | Injects Manager & Finance Approve buttons, customer tier on partners, quotation tree health badges, and custom search filters. |
| [`custom_addons/vantage_governance/views/portal_templates.xml`](file:///home/gytdrop/Documents/HACKATHONS/2026/odoo%20hackathon/odoo%20gujarat/custom_addons/vantage_governance/views/portal_templates.xml) | QWeb Portal XML | 33 | XPath injection onto `sale.sale_order_portal_content`: renders Deal Negotiation form card and locked Circuit Breaker banner. |
| [`custom_addons/vantage_governance/views/dashboard_views.xml`](file:///home/gytdrop/Documents/HACKATHONS/2026/odoo%20hackathon/odoo%20gujarat/custom_addons/vantage_governance/views/dashboard_views.xml) | Form XML | 185 | Full-width Bootstrap 5 responsive executive dashboard with border-accented KPI cards, quick-action launchpad, and live chatter activity feed. |
| [`custom_addons/vantage_governance/security/ir.model.access.csv`](file:///home/gytdrop/Documents/HACKATHONS/2026/odoo%20hackathon/odoo%20gujarat/custom_addons/vantage_governance/security/ir.model.access.csv) | Security ACL | 2 | Access control rights granting sales users and managers full view and refresh rights on `vantage.sales.dashboard`. |
| [`custom_addons/vantage_governance/demo/demo_data.xml`](file:///home/gytdrop/Documents/HACKATHONS/2026/odoo%20hackathon/odoo%20gujarat/custom_addons/vantage_governance/demo/demo_data.xml) | Data XML | 15 | Default initialization record for the executive dashboard singleton. |

---

### 3️⃣ Module: `vantage_fulfillment` (Ashrith: Operational Execution) — 8 Files
| File Path | Type | Lines | Purpose & Key Classes / Records |
| :--- | :--- | :--- | :--- |
| [`custom_addons/vantage_fulfillment/__init__.py`](file:///home/gytdrop/Documents/HACKATHONS/2026/odoo%20hackathon/odoo%20gujarat/custom_addons/vantage_fulfillment/__init__.py) | Python Init | 1 | Imports `models`. |
| [`custom_addons/vantage_fulfillment/__manifest__.py`](file:///home/gytdrop/Documents/HACKATHONS/2026/odoo%20hackathon/odoo%20gujarat/custom_addons/vantage_fulfillment/__manifest__.py) | Manifest | 15 | Module declaration, dependencies (`vantage_core`, `sale_stock`), security & view loading. |
| [`custom_addons/vantage_fulfillment/models/__init__.py`](file:///home/gytdrop/Documents/HACKATHONS/2026/odoo%20hackathon/odoo%20gujarat/custom_addons/vantage_fulfillment/models/__init__.py) | Python Init | 3 | Imports `sale_order`, `billing_schedule`, and `upsell_rule`. |
| [`custom_addons/vantage_fulfillment/models/sale_order.py`](file:///home/gytdrop/Documents/HACKATHONS/2026/odoo%20hackathon/odoo%20gujarat/custom_addons/vantage_fulfillment/models/sale_order.py) | Python Model | 211 | Warehouse auto-split (`action_split_fulfillments`), billing schedule generator (`action_generate_billing_schedule`), and smart upsell matcher. |
| [`custom_addons/vantage_fulfillment/models/billing_schedule.py`](file:///home/gytdrop/Documents/HACKATHONS/2026/odoo%20hackathon/odoo%20gujarat/custom_addons/vantage_fulfillment/models/billing_schedule.py) | Python Model | 28 | `vantage.billing.schedule`: Tracks milestone invoices (one-time vs 12-month subscription installments) and `action_mark_invoiced`. |
| [`custom_addons/vantage_fulfillment/models/upsell_rule.py`](file:///home/gytdrop/Documents/HACKATHONS/2026/odoo%20hackathon/odoo%20gujarat/custom_addons/vantage_fulfillment/models/upsell_rule.py) | Python Model | 44 | `vantage.upsell.rule`: Pairing rules, dynamic profit contribution calculation, and 1-click cart insertion (`action_apply_upsell`). |
| [`custom_addons/vantage_fulfillment/security/ir.model.access.csv`](file:///home/gytdrop/Documents/HACKATHONS/2026/odoo%20hackathon/odoo%20gujarat/custom_addons/vantage_fulfillment/security/ir.model.access.csv) | Security ACL | 3 | Full CRUD access rights on `vantage.billing.schedule` and `vantage.upsell.rule` for internal sales users. |
| [`custom_addons/vantage_fulfillment/views/fulfillment_views.xml`](file:///home/gytdrop/Documents/HACKATHONS/2026/odoo%20hackathon/odoo%20gujarat/custom_addons/vantage_fulfillment/views/fulfillment_views.xml) | Form & Menu XML | 104 | Injects `Generate Billing Schedule` header button, `Hybrid Billing Schedule` tab, `Smart Upsells` tab, and Sales -> Products -> Upsell Rules menu. |

---

## 📁 6. Repository Artifacts & Documentation Directory

* **`mockdeal` (Active Workspace)**: `/home/gytdrop/Documents/HACKATHONS/2026/odoo hackathon/odoo gujarat`
  - Remote: [`https://github.com/gytdrop/mockdeal.git`](https://github.com/gytdrop/mockdeal.git)
* **`VantageOps` (Destination Directory)**: `/home/gytdrop/Documents/HACKATHONS/2026/odoo hackathon/odoo gujarat/VantageOps`
  - Remote: [`https://github.com/gytdrop/VantageOps.git`](https://github.com/gytdrop/VantageOps.git)

---

## 🔄 7. Keywords & Living Update Instructions

Run `./--keys` or `./keys` in your terminal to see all triggers:

| Keyword Trigger | What It Updates |
| :--- | :--- |
| **`update summary`** | Scans recent UI additions, tabs, models, and file inventories to synchronize **`SUMMARY.md`**. |
| **`update explainer`** | Scans recent code chunks and logic to append new recipes into **`EXPLAINER.md`**. |
| **`promote to vantageops`** | Mirrors validated custom addons into `VantageOps` after confirmation. |
| **`write log`** | Records current work session immediately into `antigravity.log` and `workonmyperiod.log`. |
