# 🌐 VantageOps (Development Canvas: `mockdeal`)
**Engineered by gytdrop**  
*The autonomous B2B revenue and margin governance engine for Odoo.*

---

> [!CAUTION]
> ### 🛑 ABSOLUTE GUARDRAIL FOR ALL AGENTS (ANTIGRAVITY, CLAUDE, ETC.)
> 1. **DO NOT STAGE OR COMMIT IN `VantageOps`**: This current workspace (`mockdeal`) is our **active development canvas**. All coding, testing, debugging, and git commits MUST happen strictly inside `mockdeal`.
> 2. **`VantageOps` IS THE FINAL RELEASE DESTINATION**: Code is ONLY promoted and copied to `VantageOps` when a feature is 100% complete, fully working, and verified. No agent is ever permitted to run git stage or commit commands directly inside the `VantageOps` directory.
> 3. **MANDATORY LOGGING PROTOCOL**:
>    - **Antigravity** MUST log every commit and milestone into [`antigravity.log`](antigravity.log).
>    - **Claude** MUST log every commit and milestone into [`claude.log`](claude.log).
>    - **ALL AGENTS** MUST log every completed period/commit into [`workonmyperiod.log`](workonmyperiod.log).
>    - If the user says **"write log"**, the active agent must immediately append a detailed progress entry to its respective agent log and `workonmyperiod.log`.
> 4. **AFTAB RESTRICTION**: If working as or with **Aftab** (or Afteb), he is strictly restricted. Aftab is **NEVER permitted to work inside `VantageOps` or push to `VantageOps`**. All work must be conducted exclusively in `mockdeal`.

---

## Executive Summary
VantageOps provides enterprise sales teams with the strategic high ground—delivering **Total Panoramic Visibility** to eliminate margin bleed, automate complex multi-warehouse fulfillment, and govern B2B deal negotiation in real time without human bottlenecks.

## Core Capabilities
* **Executive Sales Cockpit:** Full-width Bootstrap 5 panoramic command center right from Odoo's 9-grid app launcher with real-time gross pipeline value, margin bleed alerts, approval queues, and live activity feed.
* **Dynamic Margin Governance:** Replaces static discount rules with a live Blended Risk Score. High-risk line items aggregate into an order-wide penalty, automatically halting confirmation and routing deals to the "Approvals" dashboard.
* **Agentic Portal Negotiation:** Replaces offline haggling with a governed Customer Portal and frictionless self-signup. Buyers propose counter-offers line-by-line; VantageOps intercepts, recalculates risk, and strictly limits negotiation rounds via automated circuit breakers.
* **Multi-Warehouse Execution:** Scans line items against regional warehouse stock. Automatically splits lines and generates secondary fulfillment pickings for backordered inventory, manageable directly from the "Fulfillment" module.
* **Hybrid Subscription Billing:** Natively supports both consumable hardware and recurring subscriptions on a single quotation canvas, routing properly to standard and subscription billing schedules.
* **Live Smart Upsell Engine:** Proactively pairs accessories and services to active cart lines, rendering real-time gross margin delta contribution with 1-click quote injection.

## Technical Architecture
Built as a native Odoo integration suite extending `sale_management`, `stock`, `sale_stock`, and `portal`. It leverages Odoo's native ORM and `mail.activity` chatter to ensure zero database bloat and instant deployment readiness.

## Module Structure (`custom_addons/`)
- `vantage_core`: Shared foundation extending `sale.order` and `sale.order.line` with blended risk scoring, hybrid contract detection, and the top-level 9-grid application menus.
- `vantage_governance`: Akthar's module for approval routing, chatter escalations, portal negotiation, two-tier governance, and the executive sales cockpit.
- `vantage_fulfillment`: Ashrith's module for multi-warehouse auto-splitting, milestone billing schedules, and live upsell margin contributions.

## Repositories & Resources
- **Active Canvas & Prototyping (`mockdeal`):** `https://github.com/gytdrop/mockdeal.git`
- **Final Release Destination (`VantageOps`):** `https://github.com/gytdrop/VantageOps.git` *(FROZEN TO AGENTS)*
- [System & Page Map Directory](SUMMARY.md)
- [Judge Technical Explainer & Recipe Book](EXPLAINER.md)
- [Execution Blueprint](EXECUTION_PLAN.md)
- [Data Schema & ERD Architecture](SCHEMA.md)
- [Vision & Architecture](VISION.md)
- [Interface Contract](CONTRACT.md)
- [Command Palette & Helper Keys](KEYS.md)
- [Agent Governance & Zero-Conflict Protocol](AGENTS.md)
- [Antigravity Activity Log](antigravity.log)
- [Claude Activity Log](claude.log)
- [Global Work Session Log](workonmyperiod.log)
