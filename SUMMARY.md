# 🗺️ VantageOps: System Map, Page Directory & Section Guide

> **Quick-reference handbook for Akthar: All UI page names, tabs, backend headers, portal routes, and repository files.**

---

## 📑 Table of Contents
1. [Backend Odoo UI: Tabs & Page Directory](#1-backend-odoo-ui-tabs--page-directory)
2. [Backend Odoo UI: Header Buttons & Dynamic Banners](#2-backend-odoo-ui-header-buttons--dynamic-banners)
3. [Customer Portal: Pages & Routes](#3-customer-portal-pages--routes)
4. [Repository Sections & Documentation Files](#4-repository-sections--documentation-files)
5. [Keywords & Living Update Instructions](#5-keywords--living-update-instructions)

---

## 🖥️ 1. Backend Odoo UI: Tabs & Page Directory

When viewing a Quotation or Sales Order in Odoo (`sale.view_order_form`), the central `<notebook>` contains three primary tabs:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ [Order Lines]    [Risk & Approvals (Akthar)]    [Fulfillment (Ashrith)]     │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 1️⃣ Tab: `Order Lines` (`name="order_lines"`)
* **Belongs to**: Native Odoo + `vantage_fulfillment` extension
* **Purpose**: Primary quotation workspace where line items are priced and discounted.
* **VantageOps Custom Columns Injected into Tree**:
  - `Margin ($)` (`margin_delta`): Shows real-time dollar profit contribution per line (`price_subtotal - cost`).
  - `Free Stock` (`free_qty_today`): Shows currently available free stock in the quotation's primary warehouse.
  - `Fulfillment Warehouse` (`fulfillment_warehouse_id`): Shows which specific regional warehouse fulfills this line (set automatically upon split).

---

### 2️⃣ Tab: `Risk & Approvals` (`name="page_akthar_approvals"`)
* **Belongs to**: **Akthar** (`custom_addons/vantage_governance`)
* **Purpose**: Commercial governance cockpit. Centralizes deal profitability metrics, approval state machine, and customer negotiation logs.
* **Fields Inside**:
  - **Blended Risk Score** (`blended_risk_score`): Order-wide penalty based on worst discount breach (>15%) and aggregate dollar margin loss.
  - **Risk Approval State** (`risk_approval_state`): Current governance state (`draft` $\rightarrow$ `pending_approval` $\rightarrow$ `approved` / `rejected`).
  - **Negotiation Rounds** (`negotiation_rounds`): Number of counter-offers submitted by the customer (e.g., `1 / 3`).
  - **Max Negotiation Rounds** (`max_negotiation_rounds`): Ceiling for anti-haggling circuit breaker (default: `3`).
  - **Negotiation Locked (Circuit Breaker)** (`is_negotiation_locked`): Boolean flag; turns `True` when maximum rounds are reached, disabling further portal negotiations.
  - **Last Counter-Offer Details** (`last_counter_offer`): Audit summary of the latest customer counter-proposal.

---

### 3️⃣ Tab: `Fulfillment & Warehouses` (`name="page_ashrith_fulfillment"`)
* **Belongs to**: **Ashrith** (`custom_addons/vantage_fulfillment`)
* **Purpose**: Operational logistics and multi-warehouse routing.
* **Fields Inside**:
  - **Requires Fulfillment Split** (`has_split_requirement`): Auto-computed flag that triggers when any line item's requested quantity exceeds primary warehouse available free stock.
  - **Secondary Warehouse (Backorder)** (`secondary_warehouse_id`): Destination warehouse used to fulfill stock deficits.

---

## 🔘 2. Backend Odoo UI: Header Buttons & Dynamic Banners

### Header Action Buttons (`<header>`)
| Button Name | Technical Identifier | Visibility Condition | What It Does |
| :--- | :--- | :--- | :--- |
| **Confirm** | `action_confirm` | Native Odoo | Validates deal. Intercepted by VantageOps: raises `UserError` and schedules Chatter task if risk score > 0 and unapproved. |
| **Director Approve** | `action_manager_approve` | Visible when `risk_approval_state == 'pending_approval'` | Commercial Director approves deal, transitions state to `'approved'`, auto-resolves `mail.activity`, and unlocks confirmation. |
| **Reject Deal** | `action_manager_reject` | Visible when `risk_approval_state == 'pending_approval'` | Director rejects deal, transitions state to `'rejected'`, closes activity, and logs refusal in Chatter. |
| **Auto-Split Warehouses** | `action_split_fulfillments` | Visible when `has_split_requirement == True` and state in draft/sent | Autonomously truncates primary line to available stock and forks a child line routed to secondary warehouse. |
| **Customer Preview** | `action_preview_sale_order` | Always in draft/sent | Switches current browser view into the authentic customer portal view for that order. |

---

### Dynamic Sheet Banners (Above Form Sheet)
* 🔴 **Red Alert (`alert-danger`)**:
  - *Condition*: `blended_risk_score > 0 and risk_approval_state != 'approved'`
  - *Message*: `⚠️ High-Risk Deal Detected: Blended Risk Score is [X]. Commercial approval required before confirmation.`
* 🔵 **Blue Alert (`alert-info`)**:
  - *Condition*: `is_recurring_hybrid == True`
  - *Message*: `🔄 Hybrid Deal: Contains both one-time products and recurring subscription contracts.`
* 🟡 **Yellow Alert (`alert-warning`)**:
  - *Condition*: `has_split_requirement == True`
  - *Message*: `📦 Inventory Deficit Detected: Primary warehouse stock is insufficient. Click "Auto-Split Warehouses" to allocate across regional depots.`

---

## 🌐 3. Customer Portal: Pages & Routes

External customers access their quotes via secure, tokenized URLs without requiring backend login credentials.

| URL / Endpoint | Page / View Name | Purpose & User Experience |
| :--- | :--- | :--- |
| **`http://localhost:8069/my`** | **Customer Portal Home** | Overview of all customer documents (Quotations, Orders, Invoices). |
| **`http://localhost:8069/my/quotes`** | **Quotation List** | Table of open quotations awaiting client review, acceptance, or negotiation. |
| **`http://localhost:8069/my/orders/<id>?access_token=...`** | **Order Portal Detail** | Full quotation review page. Injects VantageOps negotiation components: |
| *(Inside Order Portal)* | **Deal Negotiation Card** | *(Visible during Rounds 1-3)* Yellow card above line items allowing the customer to enter counter-discount % and concession notes. |
| *(Inside Order Portal)* | **Circuit Breaker Banner** | *(Visible when Locked)* Grey locked alert stating maximum rounds have been reached and terms are frozen. |
| **`POST /my/orders/<id>/counter_offer`** | **Counter-Offer Route** | Backend HTTP controller receiving customer input, updating discounts, recalculating risk, and posting to Chatter. |

---

## 📁 4. Repository Sections & Documentation Files

| File / Folder | Section Role | What It Contains |
| :--- | :--- | :--- |
| **`SUMMARY.md`** | **System & Page Map** | *(This file)* Comprehensive inventory of all UI pages, tabs, buttons, routes, and files. |
| **`EXPLAINER.md`** | **Judge Recipe Book** | Deep technical defense guide: Tech stack table, 8 key technical terms, 6 step-by-step Q&A recipes with exact code lines and verbal talking points for judges. |
| **`KEYS.md` / `./--keys`** | **Command Palette** | Cheat sheet of all workflow triggers (`I am Akthar`, `update explainer`, `update summary`, etc.). |
| **`CONTRACT.md`** | **Interface Boundaries** | Data model field contracts and zero-conflict rules between Akthar and Ashrith. |
| **`EXECUTION_PLAN.md`** | **Strategy Blueprint** | The original "Native Odoo Gigs" blueprint delivering features in < 400 lines of Python. |
| **`custom_addons/vantage_core/`** | **Base Models** | Shared risk formula (`blended_risk_score`), approval state machine, and hybrid contract tagging. |
| **`custom_addons/vantage_governance/`** | **Akthar's Module** | Confirmation block, Chatter activities, portal counter-offer UI, and circuit-breaker engine. |
| **`custom_addons/vantage_fulfillment/`** | **Ashrith's Module** | Warehouse free stock scanner, auto-split fulfillment logic, and live margin delta upsell. |
| **`antigravity.log` / `workonmyperiod.log`** | **Audit Trail** | Mandatory chronological logs of every milestone and commit. |

---

## 🔄 5. Keywords & Living Update Instructions

Whenever you update views, add new tabs, or create new models, use these exact keywords in your prompts or terminal:

| Keyword Trigger | What It Updates |
| :--- | :--- |
| **`./--keys`** or **`./keys`** | Displays the full technical command palette in your terminal anytime. |
| **`update summary`** | Automatically scans recent UI changes, tabs, and models to synchronize **`SUMMARY.md`**. |
| **`update explainer`** | Automatically scans recent code chunks and logic to append new recipes into **`EXPLAINER.md`**. |
| **`write log`** | Immediately records the current work session into `antigravity.log` and `workonmyperiod.log`. |
