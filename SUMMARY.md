# 🗺️ VantageOps: System Map, Page Directory & Destined File Locations

> **Quick-reference handbook for Akthar: All UI page names, tabs, backend headers, portal routes, and exact file paths across `mockdeal` and `VantageOps`.**

---

## 📑 Table of Contents
1. [Backend Odoo UI: Tabs, Fields & File Locations](#1-backend-odoo-ui-tabs-fields--file-locations)
2. [Backend Odoo UI: Header Buttons, Alerts & Code Locations](#2-backend-odoo-ui-header-buttons-alerts--code-locations)
3. [Customer Portal: Pages, Views & Controller Locations](#3-customer-portal-pages-views--controller-locations)
4. [Destined File Mapping: Mockdeal Canvas ➔ VantageOps Destination](#4-destined-file-mapping-mockdeal-canvas--vantageops-destination)
5. [Confirmed Python & XML Source Code Inventory (All 18 Production Files)](#5-confirmed-python--xml-source-code-inventory-all-18-production-files)
6. [Repository Artifacts & Documentation Directory](#6-repository-artifacts--documentation-directory)
7. [Keywords & Living Update Instructions](#7-keywords--living-update-instructions)

---

## 🖥️ 1. Backend Odoo UI: Tabs, Fields & File Locations

When viewing a Quotation or Sales Order in Odoo ([`sale.view_order_form`](http://localhost:8069/web#id=26&model=sale.order&view_type=form)), the central `<notebook>` contains three primary tabs:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ [Order Lines]    [Risk & Approvals (Akthar)]    [Fulfillment (Ashrith)]     │
└─────────────────────────────────────────────────────────────────────────────┘
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
* **View Source File**: [`custom_addons/vantage_fulfillment/views/fulfillment_views.xml:L32-41`](file:///home/gytdrop/Documents/HACKATHONS/2026/odoo%20hackathon/odoo%20gujarat/custom_addons/vantage_fulfillment/views/fulfillment_views.xml#L32-L41)
* **Model Source File**: [`custom_addons/vantage_fulfillment/models/sale_order.py:L7-17`](file:///home/gytdrop/Documents/HACKATHONS/2026/odoo%20hackathon/odoo%20gujarat/custom_addons/vantage_fulfillment/models/sale_order.py#L7-L17)
* **Purpose**: Operational logistics and multi-warehouse routing.
* **Fields & Defining Locations**:
  - `has_split_requirement`: Deficit indicator. Defined in `vantage_fulfillment/models/sale_order.py:L7`.
  - `secondary_warehouse_id`: Backorder destination warehouse. Defined in `vantage_fulfillment/models/sale_order.py:L13`.

---

## 🔘 2. Backend Odoo UI: Header Buttons, Alerts & Code Locations

### Header Action Buttons (`<header>`)
| Button Name | Technical Identifier | View Definition Location | Python Logic Location | What It Does |
| :--- | :--- | :--- | :--- | :--- |
| **Confirm** | `action_confirm` | Native Odoo `sale.view_order_form` | [`vantage_governance/models/sale_order.py:L21`](file:///home/gytdrop/Documents/HACKATHONS/2026/odoo%20hackathon/odoo%20gujarat/custom_addons/vantage_governance/models/sale_order.py#L21) | Validates deal; intercepted to raise `UserError` and schedule Chatter task if risk score > 0 and unapproved. |
| **Director Approve** | `action_manager_approve` | [`vantage_governance/views/governance_views.xml:L10`](file:///home/gytdrop/Documents/HACKATHONS/2026/odoo%20hackathon/odoo%20gujarat/custom_addons/vantage_governance/views/governance_views.xml#L10) | [`vantage_governance/models/sale_order.py:L55`](file:///home/gytdrop/Documents/HACKATHONS/2026/odoo%20hackathon/odoo%20gujarat/custom_addons/vantage_governance/models/sale_order.py#L55) | Sets `risk_approval_state = 'approved'`, auto-resolves `mail.activity`, and unlocks confirmation. |
| **Reject Deal** | `action_manager_reject` | [`vantage_governance/views/governance_views.xml:L12`](file:///home/gytdrop/Documents/HACKATHONS/2026/odoo%20hackathon/odoo%20gujarat/custom_addons/vantage_governance/views/governance_views.xml#L12) | [`vantage_governance/models/sale_order.py:L67`](file:///home/gytdrop/Documents/HACKATHONS/2026/odoo%20hackathon/odoo%20gujarat/custom_addons/vantage_governance/models/sale_order.py#L67) | Sets `risk_approval_state = 'rejected'`, closes activity, and logs rejection in Chatter. |
| **Auto-Split Warehouses** | `action_split_fulfillments` | [`vantage_fulfillment/views/fulfillment_views.xml:L10`](file:///home/gytdrop/Documents/HACKATHONS/2026/odoo%20hackathon/odoo%20gujarat/custom_addons/vantage_fulfillment/views/fulfillment_views.xml#L10) | [`vantage_fulfillment/models/sale_order.py:L25`](file:///home/gytdrop/Documents/HACKATHONS/2026/odoo%20hackathon/odoo%20gujarat/custom_addons/vantage_fulfillment/models/sale_order.py#L25) | Truncates primary line and forks child line routed to secondary warehouse. |
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

## 🌐 3. Customer Portal: Pages, Views & Controller Locations

| URL / Route | Component | XML / Python File Location | Purpose & Experience |
| :--- | :--- | :--- | :--- |
| **`/my` & `/my/home`** | Portal Dashboard | Native Odoo `addons/portal/` | Overview of all customer transactions. |
| **`/my/quotes`** | Quotation List | Native Odoo `addons/sale/` | Summary of quotations awaiting review. |
| **`/my/orders/<id>`** | Order Portal Detail | Native `addons/sale/views/sale_portal_templates.xml` | Full customer quotation view. |
| *(Inside Portal)* | **Deal Negotiation Card** | [`custom_addons/vantage_governance/views/portal_templates.xml:L6-26`](file:///home/gytdrop/Documents/HACKATHONS/2026/odoo%20hackathon/odoo%20gujarat/custom_addons/vantage_governance/views/portal_templates.xml#L6-L26) | Injected card above line items allowing customer to submit counter-discount % and concession notes. |
| *(Inside Portal)* | **Circuit Breaker Alert** | [`custom_addons/vantage_governance/views/portal_templates.xml:L28-30`](file:///home/gytdrop/Documents/HACKATHONS/2026/odoo%20hackathon/odoo%20gujarat/custom_addons/vantage_governance/views/portal_templates.xml#L28-L30) | Banner informing customer that maximum rounds (3) have been reached and deal terms are locked. |
| **`POST /my/orders/<id>/counter_offer`** | Counter-Offer API | [`custom_addons/vantage_governance/controllers/portal.py:L7-24`](file:///home/gytdrop/Documents/HACKATHONS/2026/odoo%20hackathon/odoo%20gujarat/custom_addons/vantage_governance/controllers/portal.py#L7-L24) | Validates token, calls `action_customer_counter_offer()`, recalculates risk, and posts Chatter card. |

---

## 🚚 4. Destined File Mapping: Mockdeal Canvas ➔ VantageOps Destination

| Component / File | Location in `mockdeal` (Canvas) | Destined Location in `VantageOps` (Release) | Status / Rule |
| :--- | :--- | :--- | :--- |
| **Shared Core Addon** | `custom_addons/vantage_core/` | `VantageOps/custom_addons/vantage_core/` | ✅ **Mirrored & Pushed** |
| **Akthar Governance Addon** | `custom_addons/vantage_governance/` | `VantageOps/custom_addons/vantage_governance/` | ✅ **Mirrored & Pushed** |
| **Ashrith Fulfillment Addon** | `custom_addons/vantage_fulfillment/` | `VantageOps/custom_addons/vantage_fulfillment/` | ✅ **Mirrored & Pushed** |
| **Enterprise README** | `README.md` (Canvas version) | `VantageOps/README.md` (Enterprise clean version) | ✅ **Clean Enterprise Live** |
| **Git Exclusion Rules** | `.gitignore` | `VantageOps/.gitignore` | ✅ **Clean Enterprise Live** |
| **Judge Recipe Book** | [`EXPLAINER.md`](file:///home/gytdrop/Documents/HACKATHONS/2026/odoo%20hackathon/odoo%20gujarat/EXPLAINER.md) | *Canvas only (or optional promotion)* | 🏠 Kept in `mockdeal` |
| **System & Page Map** | [`SUMMARY.md`](file:///home/gytdrop/Documents/HACKATHONS/2026/odoo%20hackathon/odoo%20gujarat/SUMMARY.md) | *Canvas only (or optional promotion)* | 🏠 Kept in `mockdeal` |
| **Command Palette & Helpers** | [`KEYS.md`](file:///home/gytdrop/Documents/HACKATHONS/2026/odoo%20hackathon/odoo%20gujarat/KEYS.md), `./--keys`, `./keys` | *Excluded from VantageOps* | 🚫 Canvas only |
| **Team Governance Rules** | [`AGENTS.md`](file:///home/gytdrop/Documents/HACKATHONS/2026/odoo%20hackathon/odoo%20gujarat/AGENTS.md), [`CONTRACT.md`](file:///home/gytdrop/Documents/HACKATHONS/2026/odoo%20hackathon/odoo%20gujarat/CONTRACT.md), [`EXECUTION_PLAN.md`](file:///home/gytdrop/Documents/HACKATHONS/2026/odoo%20hackathon/odoo%20gujarat/EXECUTION_PLAN.md) | *Excluded from VantageOps* | 🚫 Canvas only |
| **Agent & Period Logs** | `antigravity.log`, `workonmyperiod.log` | *Excluded from VantageOps* | 🚫 Canvas only |

---

## 📜 5. Confirmed Python & XML Source Code Inventory (All 18 Production Files)

All 18 production files have been compiled, syntax-validated, and confirmed working on local Odoo (`vantage_db` on port 8069).

### 📦 Summary by File Type & Line Count
* **Total Confirmed Files**: 18
* **Python Files**: 14 files (379 lines of Python)
* **XML Files**: 4 files (149 lines of XML)
* **Total Production Lines**: **528 lines** *(Delivering full enterprise scope under 400 lines of Python!)*

---

### 1️⃣ Module: `vantage_core` (Base Foundation) — 5 Files / 143 Lines
| File Path | Type | Lines | Purpose & Key Classes / Records |
| :--- | :--- | :--- | :--- |
| [`custom_addons/vantage_core/__init__.py`](file:///home/gytdrop/Documents/HACKATHONS/2026/odoo%20hackathon/odoo%20gujarat/custom_addons/vantage_core/__init__.py) | Python Init | 1 | Imports `models` package. |
| [`custom_addons/vantage_core/__manifest__.py`](file:///home/gytdrop/Documents/HACKATHONS/2026/odoo%20hackathon/odoo%20gujarat/custom_addons/vantage_core/__manifest__.py) | Manifest | 13 | Module declaration, dependencies (`sale_management`, `mail`), view registration. |
| [`custom_addons/vantage_core/models/__init__.py`](file:///home/gytdrop/Documents/HACKATHONS/2026/odoo%20hackathon/odoo%20gujarat/custom_addons/vantage_core/models/__init__.py) | Python Init | 1 | Imports `sale_order`. |
| [`custom_addons/vantage_core/models/sale_order.py`](file:///home/gytdrop/Documents/HACKATHONS/2026/odoo%20hackathon/odoo%20gujarat/custom_addons/vantage_core/models/sale_order.py) | Python Model | 91 | Implements `_compute_vantage_risk` formula, `risk_approval_state` transitions, and `_compute_is_recurring_hybrid` contract detection. |
| [`custom_addons/vantage_core/views/vantage_core_views.xml`](file:///home/gytdrop/Documents/HACKATHONS/2026/odoo%20hackathon/odoo%20gujarat/custom_addons/vantage_core/views/vantage_core_views.xml) | Form XML | 37 | Injects red high-risk alert, blue hybrid banner, and sheet badges (`blended_risk_score`, `risk_approval_state`). |

---

### 2️⃣ Module: `vantage_governance` (Akthar: Commercial Control) — 8 Files / 214 Lines
| File Path | Type | Lines | Purpose & Key Classes / Records |
| :--- | :--- | :--- | :--- |
| [`custom_addons/vantage_governance/__init__.py`](file:///home/gytdrop/Documents/HACKATHONS/2026/odoo%20hackathon/odoo%20gujarat/custom_addons/vantage_governance/__init__.py) | Python Init | 2 | Imports `models` and `controllers`. |
| [`custom_addons/vantage_governance/__manifest__.py`](file:///home/gytdrop/Documents/HACKATHONS/2026/odoo%20hackathon/odoo%20gujarat/custom_addons/vantage_governance/__manifest__.py) | Manifest | 14 | Module metadata, dependencies (`vantage_core`, `portal`, `mail`), view loading. |
| [`custom_addons/vantage_governance/models/__init__.py`](file:///home/gytdrop/Documents/HACKATHONS/2026/odoo%20hackathon/odoo%20gujarat/custom_addons/vantage_governance/models/__init__.py) | Python Init | 1 | Imports `sale_order`. |
| [`custom_addons/vantage_governance/models/sale_order.py`](file:///home/gytdrop/Documents/HACKATHONS/2026/odoo%20hackathon/odoo%20gujarat/custom_addons/vantage_governance/models/sale_order.py) | Python Model | 105 | Implements `action_confirm` block, `_schedule_manager_approval_activity`, `action_manager_approve`, `action_manager_reject`, and `action_customer_counter_offer`. |
| [`custom_addons/vantage_governance/controllers/__init__.py`](file:///home/gytdrop/Documents/HACKATHONS/2026/odoo%20hackathon/odoo%20gujarat/custom_addons/vantage_governance/controllers/__init__.py) | Python Init | 1 | Imports `portal`. |
| [`custom_addons/vantage_governance/controllers/portal.py`](file:///home/gytdrop/Documents/HACKATHONS/2026/odoo%20hackathon/odoo%20gujarat/custom_addons/vantage_governance/controllers/portal.py) | Python Controller | 23 | Public HTTP endpoint `/my/orders/<id>/counter_offer` validating tokens and routing counter discounts. |
| [`custom_addons/vantage_governance/views/governance_views.xml`](file:///home/gytdrop/Documents/HACKATHONS/2026/odoo%20hackathon/odoo%20gujarat/custom_addons/vantage_governance/views/governance_views.xml) | Form XML | 35 | Injects `action_manager_approve` & `action_manager_reject` header buttons and the `Risk & Approvals` notebook tab. |
| [`custom_addons/vantage_governance/views/portal_templates.xml`](file:///home/gytdrop/Documents/HACKATHONS/2026/odoo%20hackathon/odoo%20gujarat/custom_addons/vantage_governance/views/portal_templates.xml) | QWeb Portal XML | 33 | XPath injection onto `sale.sale_order_portal_content`: renders the Deal Negotiation form card and the locked Circuit Breaker banner. |

---

### 3️⃣ Module: `vantage_fulfillment` (Ashrith: Operational Execution) — 5 Files / 174 Lines
| File Path | Type | Lines | Purpose & Key Classes / Records |
| :--- | :--- | :--- | :--- |
| [`custom_addons/vantage_fulfillment/__init__.py`](file:///home/gytdrop/Documents/HACKATHONS/2026/odoo%20hackathon/odoo%20gujarat/custom_addons/vantage_fulfillment/__init__.py) | Python Init | 1 | Imports `models`. |
| [`custom_addons/vantage_fulfillment/__manifest__.py`](file:///home/gytdrop/Documents/HACKATHONS/2026/odoo%20hackathon/odoo%20gujarat/custom_addons/vantage_fulfillment/__manifest__.py) | Manifest | 13 | Module declaration, dependencies (`vantage_core`, `stock`, `sale_stock`), view loading. |
| [`custom_addons/vantage_fulfillment/models/__init__.py`](file:///home/gytdrop/Documents/HACKATHONS/2026/odoo%20hackathon/odoo%20gujarat/custom_addons/vantage_fulfillment/models/__init__.py) | Python Init | 1 | Imports `sale_order`. |
| [`custom_addons/vantage_fulfillment/models/sale_order.py`](file:///home/gytdrop/Documents/HACKATHONS/2026/odoo%20hackathon/odoo%20gujarat/custom_addons/vantage_fulfillment/models/sale_order.py) | Python Model | 115 | Location-context inventory scanner (`_compute_free_qty_today`), auto-split line forking (`action_split_fulfillments`), and `margin_delta`. |
| [`custom_addons/vantage_fulfillment/views/fulfillment_views.xml`](file:///home/gytdrop/Documents/HACKATHONS/2026/odoo%20hackathon/odoo%20gujarat/custom_addons/vantage_fulfillment/views/fulfillment_views.xml) | Form XML | 44 | Injects `Auto-Split Warehouses` header button, yellow inventory deficit warning, line tree margin columns, and `Fulfillment & Warehouses` tab. |

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
