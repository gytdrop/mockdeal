# DealFlow360 - Intelligent, Self-Governing Sales Operations Platform

DealFlow360 is an intelligent B2B deal engine and sales operations platform built on Odoo. It enforces pricing discipline with multi-tiered discount governance and a blended risk score, reacts to multi-warehouse inventory realities in real time, reconciles hybrid subscriptions and one-time sales on a single order, provides live upsell margin suggestions, and enables customer portal negotiations.

---

## 📚 Key Documentation

- [Problem Statement & Full Specification](docs/PROBLEM_STATEMENT.md)
- [Original Problem PDF](docs/DealFlow360.pdf)
- [Data & Model Interface Contract (CONTRACT.md)](CONTRACT.md)
- [Development Guidelines & Agent Context (AGENTS.md)](AGENTS.md)
- [UI / UX Excalidraw Mockup](https://app.excalidraw.com/l/65VNwvy7c4X/7Fb5SR3WKu2)

---

## 👥 Two-Member Team Division

The codebase is split modularly under `custom_addons/` to ensure zero git merge conflicts:

```
custom_addons/
├── hackathon_core/          # Core Sales/Quotation models, Base Views, Shared Access Rules
├── hackathon_feature_a/     # Teammate A: Pricing Governance, Approvals & Portal Negotiation
└── hackathon_feature_b/     # Teammate B: Multi-Warehouse Fulfillment, Hybrid Billing & Upsell Engine
```

### Member 1: Feature A (`hackathon_feature_a`)
- **Discount Governance & Blended Risk Score**:
  - Customer tier ceilings (Bronze, Silver, Gold) & category ceilings.
  - Blended Discount Risk computation engine.
  - Multi-tiered approval workflow (Sales Manager & Finance routing).
- **Customer Negotiation Portal**:
  - Restricted external portal view for quotation negotiation.
  - Line-level comments and counter-offers.
  - Automatic re-entry into approval workflow on threshold breaches.
- **Deal Health & Anomaly Dashboard**:
  - Detection of stalled deals, rep discount anomalies, and slippage indicators.

### Member 2: Feature B (`hackathon_feature_b`)
- **Multi-Warehouse Fulfillment & Stock Splitting**:
  - Live stock-aware order line splitting across warehouses.
  - Split recommendation interface with manual overrides.
  - "Consolidate Remaining Backorder" trigger.
- **Hybrid Billing & Recurring Subscriptions**:
  - Mixing one-time hardware/services with recurring subscription contracts.
  - Billing schedules, invoice generation, and mid-cycle proration engine.
- **Live Upsell & Cross-Sell Intelligence**:
  - Contextual product pairings & promoted suggestions.
  - Real-time margin delta computation and live quote updates.

---

## 🛡️ Modular Development Rules
1. **Never modify `hackathon_core` directly** for feature-specific logic.
2. **Use Python inheritance (`_inherit`)** in feature modules to add fields and business logic.
3. **Use View inheritance (`inherit_id` + `<xpath>`)** to extend UI elements.
4. **Consult & update [CONTRACT.md](CONTRACT.md)** before adding fields, models, or methods to prevent naming collisions.
