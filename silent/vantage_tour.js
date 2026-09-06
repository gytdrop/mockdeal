/** @odoo-module **/
import { registry } from "@web/core/registry";

registry.category("web_tour.tours").add("vantageops_admin_tour", {
    url: "/web",
    sequence: 10,
    checkDelay: 100,
    steps: () => [
        // 1. Active Deal Console Header & Tour Launcher
        {
            trigger: 'button[name="action_launch_onboarding_tour"], .o_form_statusbar',
            content: "<b>Active Deal Console</b><br/>" +
                     "<b>What:</b> The primary execution record unifying commercial negotiation, margin guardrails, and physical fulfillment.<br/>" +
                     "<b>Why:</b> Gives sales reps and executive leadership complete real-time governance directly within the quotation workflow.",
            tooltipPosition: "bottom",
        },

        // 2. Margin Risk Score
        {
            trigger: '.o_field_widget[name="blended_risk_score"], div[name="blended_risk_score"], div[name="risk_approval_state"]',
            content: "<b>Autonomous Margin Risk Engine</b><br/>" +
                     "<b>What:</b> Dynamic scoring algorithm factoring client credit tier, product line margins, and discount variance.<br/>" +
                     "<b>Why:</b> Intercepts silent margin bleed by automatically locking deals when discounts violate policy rules.",
            tooltipPosition: "bottom",
        },

        // 3. Multi-Depot Auto-Split
        {
            trigger: 'button[name="action_split_fulfillments"]',
            content: "<b>Deficit Line-Forking Engine</b><br/>" +
                     "<b>What:</b> Real-time regional warehouse inventory allocator.<br/>" +
                     "<b>Why:</b> If the primary depot lacks stock, it forks lines into discrete regional pickings to eliminate delivery backorder stalls without manual intervention.",
            tooltipPosition: "bottom",
        },

        // 4. Pitch Counter-Offer
        {
            trigger: 'button[name="action_open_bargain_wizard"]',
            content: "<b>Commercial Concession Window</b><br/>" +
                     "<b>What:</b> Wizard that defines acceptable concession floors and initiates structured bargaining.<br/>" +
                     "<b>Why:</b> Prevents sales reps from giving ad-hoc discounts by binding negotiations to policy parameters.",
            tooltipPosition: "bottom",
        },

        // 5. Simulated Inbound Negotiation
        {
            trigger: 'button[name="action_simulate_customer_counter"]',
            content: "<b>Inbound Negotiation Response</b><br/>" +
                     "<b>What:</b> Simulates incoming customer terms (8% volume concession) handled by the portal controller.<br/>" +
                     "<b>Why:</b> Demonstrates the round-trip feedback loop directly on one screen without fragile cross-browser session tab switching.",
            tooltipPosition: "bottom",
        },

        // 6. Circuit Breaker Telemetry
        {
            trigger: '.o-mail-Chatter, .o_MessageList, .o_Chatter, .o-mail-Form-chatter',
            content: "<b>3-Round Circuit Breaker &amp; Audit Trail</b><br/>" +
                     "<b>What:</b> Strict round limiter and immutable Chatter audit log.<br/>" +
                     "<b>Why:</b> Prevents endless bargaining deadlocks; after 3 rounds, terms lock permanently to protect profit margins.",
            tooltipPosition: "top",
        },

        // 7. Milestone Hybrid Billing
        {
            trigger: 'button[name="action_generate_billing_schedule"]',
            content: "<b>Hybrid Milestone Billing Engine</b><br/>" +
                     "<b>What:</b> Automated revenue recognition generator that bifurcates physical fulfillment from recurring services into structured periods.<br/>" +
                     "<b>Why:</b> Solves contract billing mismatches by generating clean invoicing schedules directly from the sale order.",
            tooltipPosition: "bottom",
        },

        // 8. Two-Tier Approval Cascade
        {
            trigger: 'button[name="action_manager_approve"], button[name="action_finance_approve"], .o_statusbar_buttons',
            content: "<b>Two-Tier Governance Escalation</b><br/>" +
                     "<b>What:</b> Role-based authorization gate (Manager sign-off for minor variance; Finance Director for risk scores &gt; 10.0).<br/>" +
                     "<b>Why:</b> Ensures senior leadership visibility into high-exposure commitments while allowing routine deals to move quickly.",
            tooltipPosition: "bottom",
        },

        // 9. Final ORM Interception Gate
        {
            trigger: 'button[name="action_confirm"]',
            content: "<b>ORM Confirmation Guard</b><br/>" +
                     "<b>What:</b> Interception gate hooked directly into the core `action_confirm` method.<br/>" +
                     "<b>Why:</b> Guarantees unapproved, high-risk deals can never generate pickings or commit inventory, even if attempted via external API or bulk scripts.",
            tooltipPosition: "bottom",
        },
    ],
});

// Client action bridge to launch tour from Python XML button
registry.category("actions").add("vantageops.start_tour", function (env, action) {
    const tourService = env.services && (env.services.tour_service || env.services.tour);
    if (tourService && tourService.startTour) {
        tourService.startTour("vantageops_admin_tour", { mode: "manual", redirect: false });
    } else if (window.odoo && window.odoo.startTour) {
        window.odoo.startTour("vantageops_admin_tour", { mode: "manual", redirect: false });
    }
});
