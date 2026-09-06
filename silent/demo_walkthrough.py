# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class VantageDemoWalkthrough(models.TransientModel):
    _name = 'vantage.demo.walkthrough'
    _description = 'VantageOps Interactive Live Tour & Architectural Guide'

    name = fields.Char(default='VantageOps Interactive Demonstration')

    def action_open_high_risk_deal(self):
        """Jump to S00019 or the highest risk deal to demonstrate Margin Guard & ORM block."""
        order = self.env['sale.order'].search([('blended_risk_score', '>', 10.0)], limit=1)
        if not order:
            order = self.env['sale.order'].search([('name', '=', 'S00019')], limit=1)
        if not order:
            order = self.env['sale.order'].search([], order='id desc', limit=1)
        
        return {
            'name': _('High-Risk Deal Console (Governance Interception)'),
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order',
            'res_id': order.id if order else False,
            'view_mode': 'form',
            'target': 'current',
        }

    def action_open_split_deal(self):
        """Jump to S00039 or an order with split requirements to demonstrate Multi-Depot allocation."""
        order = self.env['sale.order'].search([('has_split_requirement', '=', True)], limit=1)
        if not order:
            order = self.env['sale.order'].search([('name', '=', 'S00039')], limit=1)
        if not order:
            order = self.env['sale.order'].search([], order='id desc', limit=1)
        
        return {
            'name': _('Multi-Depot Split Delivery Console'),
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order',
            'res_id': order.id if order else False,
            'view_mode': 'form',
            'target': 'current',
        }

    def action_open_negotiation_demo(self):
        """Jump to a quotation to demonstrate the Bargaining Wizard and Customer Counter simulation."""
        order = self.env['sale.order'].search([('state', 'in', ['draft', 'sent'])], limit=1)
        if not order:
            order = self.env['sale.order'].search([], order='id desc', limit=1)
        
        return {
            'name': _('Negotiation & Circuit Breaker Console'),
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order',
            'res_id': order.id if order else False,
            'view_mode': 'form',
            'target': 'current',
        }

    def action_open_approvals(self):
        """Jump to Pending Approvals Queue."""
        return {
            'name': _('Deals Awaiting Commercial Sign-off'),
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order',
            'view_mode': 'tree,kanban,form',
            'domain': [('risk_approval_state', 'in', ['pending_approval', 'pending_manager', 'pending_finance'])],
            'target': 'current',
        }

    def action_open_billing(self):
        """Jump to Hybrid Billing Schedules."""
        return {
            'name': _('Hybrid Milestone Billing Schedules'),
            'type': 'ir.actions.act_window',
            'res_model': 'vantage.billing.schedule',
            'view_mode': 'tree,form',
            'target': 'current',
        }

    def action_reseed_turnkey_data(self):
        """Re-seed turnkey demo data."""
        dashboard = self.env['vantage.sales.dashboard'].search([], limit=1)
        if dashboard and hasattr(dashboard, 'action_seed_turnkey_demo_data'):
            return dashboard.action_seed_turnkey_demo_data()
        return True

    def action_start_ui_tour(self):
        """Opens deal S00019 to launch the interactive live tour."""
        order = self.env['sale.order'].search([('name', '=', 'S00019')], limit=1)
        if not order:
            order = self.env['sale.order'].search([('blended_risk_score', '>', 10.0)], limit=1)
        if not order:
            order = self.env['sale.order'].search([], order='id desc', limit=1)
        return {
            'name': _('Active Deal Console (Tour Target)'),
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order',
            'res_id': order.id if order else False,
            'view_mode': 'form',
            'target': 'current',
        }
