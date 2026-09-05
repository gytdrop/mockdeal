from odoo import models, fields, api, _

class VantageSalesDashboard(models.Model):
    _name = 'vantage.sales.dashboard'
    _description = 'VantageOps Executive Sales Dashboard'

    name = fields.Char(string='Dashboard Title', default='VantageOps Executive Sales Cockpit')
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)

    # --- 1. DEAL METRICS ---
    total_deal_count = fields.Integer(string='Total Deals', compute='_compute_metrics')
    total_pipeline_val = fields.Monetary(string='Total Pipeline Value', currency_field='currency_id', compute='_compute_metrics')
    avg_deal_val = fields.Monetary(string='Avg Deal Value', currency_field='currency_id', compute='_compute_metrics')
    high_risk_deal_count = fields.Integer(string='High-Risk Deals', compute='_compute_metrics')

    # --- 2. HEALTH METRICS ---
    healthy_deal_count = fields.Integer(string='Healthy Deals', compute='_compute_metrics')
    stalled_deal_count = fields.Integer(string='Stalled Deals (>3 Days)', compute='_compute_metrics')
    margin_bleed_count = fields.Integer(string='Critical Margin Bleed', compute='_compute_metrics')

    # --- 3. APPROVALS METRICS ---
    pending_manager_count = fields.Integer(string='Pending Manager Approval', compute='_compute_metrics')
    pending_finance_count = fields.Integer(string='Pending Finance Approval', compute='_compute_metrics')
    total_pending_approvals = fields.Integer(string='Total Pending Approvals', compute='_compute_metrics')
    approved_deal_count = fields.Integer(string='Approved Deals', compute='_compute_metrics')
    rejected_deal_count = fields.Integer(string='Rejected Deals', compute='_compute_metrics')

    # --- 4. QUOTATIONS METRICS ---
    draft_quotes_count = fields.Integer(string='Draft Quotations', compute='_compute_metrics')
    sent_quotes_count = fields.Integer(string='Sent Quotations', compute='_compute_metrics')
    confirmed_orders_count = fields.Integer(string='Confirmed Sales Orders', compute='_compute_metrics')

    # --- 5. SUBSCRIPTION & HYBRID METRICS ---
    hybrid_deal_count = fields.Integer(string='Hybrid Contracts', compute='_compute_metrics')
    total_billing_schedules = fields.Integer(string='Billing Milestones', compute='_compute_metrics')
    scheduled_recurring_val = fields.Monetary(string='Scheduled MRR Pipeline', currency_field='currency_id', compute='_compute_metrics')
    invoiced_recurring_val = fields.Monetary(string='Realized Revenue', currency_field='currency_id', compute='_compute_metrics')

    # --- 6. FULFILLMENT & LOGISTICS METRICS ---
    split_deficit_count = fields.Integer(string='Orders with Stock Deficit', compute='_compute_metrics')
    forked_backorders_count = fields.Integer(string='Forked Regional Backorders', compute='_compute_metrics')

    # --- RECENT ACTIVITY ---
    recent_activity_html = fields.Html(string='Recent Activity', compute='_compute_metrics')

    def _compute_metrics(self):
        order_obj = self.env['sale.order']
        line_obj = self.env['sale.order.line']
        sched_obj = self.env['vantage.billing.schedule'] if 'vantage.billing.schedule' in self.env else None
        msg_obj = self.env['mail.message']

        for rec in self:
            all_orders = order_obj.search([])
            rec.total_deal_count = len(all_orders)
            rec.total_pipeline_val = sum(all_orders.mapped('amount_total'))
            rec.avg_deal_val = round(rec.total_pipeline_val / rec.total_deal_count, 2) if rec.total_deal_count else 0.0
            rec.high_risk_deal_count = len(all_orders.filtered(lambda o: o.blended_risk_score > 0))

            # Health
            rec.healthy_deal_count = len(all_orders.filtered(lambda o: o.deal_health == 'healthy'))
            rec.stalled_deal_count = len(all_orders.filtered(lambda o: o.deal_health == 'stalled'))
            rec.margin_bleed_count = len(all_orders.filtered(lambda o: o.deal_health == 'margin_bleed'))

            # Approvals
            rec.pending_manager_count = len(all_orders.filtered(lambda o: o.risk_approval_state in ('pending_approval', 'pending_manager')))
            rec.pending_finance_count = len(all_orders.filtered(lambda o: o.risk_approval_state == 'pending_finance'))
            rec.total_pending_approvals = rec.pending_manager_count + rec.pending_finance_count
            rec.approved_deal_count = len(all_orders.filtered(lambda o: o.risk_approval_state == 'approved'))
            rec.rejected_deal_count = len(all_orders.filtered(lambda o: o.risk_approval_state == 'rejected'))

            # Quotations
            rec.draft_quotes_count = len(all_orders.filtered(lambda o: o.state == 'draft'))
            rec.sent_quotes_count = len(all_orders.filtered(lambda o: o.state == 'sent'))
            rec.confirmed_orders_count = len(all_orders.filtered(lambda o: o.state == 'sale'))

            # Subscriptions / Hybrid
            rec.hybrid_deal_count = len(all_orders.filtered(lambda o: o.is_recurring_hybrid))
            if sched_obj:
                all_schedules = sched_obj.search([])
                rec.total_billing_schedules = len(all_schedules)
                rec.scheduled_recurring_val = sum(all_schedules.filtered(lambda s: s.state == 'scheduled').mapped('amount'))
                rec.invoiced_recurring_val = sum(all_schedules.filtered(lambda s: s.state == 'invoiced').mapped('amount'))
            else:
                rec.total_billing_schedules = 0
                rec.scheduled_recurring_val = 0.0
                rec.invoiced_recurring_val = 0.0

            # Fulfillment
            rec.split_deficit_count = len(all_orders.filtered(lambda o: o.has_split_requirement))
            rec.forked_backorders_count = line_obj.search_count([('is_split_child', '=', True)])

            # Recent Activity HTML
            recent_msgs = msg_obj.search([('model', '=', 'sale.order'), ('message_type', '!=', 'user_notification')], limit=5, order='id desc')
            
            html = '<ul style="list-style-type: none; padding-left: 0; margin: 0;">'
            for m in recent_msgs:
                order = order_obj.browse(m.res_id)
                # Strip HTML tags from message body
                import re
                clean_body = re.sub(r'<[^>]+>', '', m.body or '')
                text = f"{order.name} - {clean_body}"
                if len(text) > 80:
                    text = text[:77] + '...'
                html += f'<li style="margin-bottom: 8px;">- {text}</li>'
            
            if not recent_msgs:
                html += '<li>- No recent activity found</li>'
                
            html += '</ul>'
            rec.recent_activity_html = html

    def action_refresh(self):
        """Recompute metrics"""
        self.ensure_one()
        self._compute_metrics()
        return True

    def action_new_quotation(self):
        return {
            'name': _('New Quotation'),
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order',
            'view_mode': 'form',
            'target': 'current',
        }

    def action_view_approvals(self):
        return self.action_view_pending_approvals()

    def action_view_all_deals(self):
        return {
            'name': _('Deal Pipeline'),
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order',
            'view_mode': 'tree,kanban,form',
            'target': 'current',
        }

    def action_view_margin_bleed(self):
        return {
            'name': _('Critical Margin Bleed Deals'),
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order',
            'view_mode': 'tree,kanban,form',
            'domain': [('deal_health', '=', 'margin_bleed')],
            'target': 'current',
        }

    def action_view_stalled(self):
        return {
            'name': _('Stalled Quotes (>3 Days Inactive)'),
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order',
            'view_mode': 'tree,kanban,form',
            'domain': [('deal_health', '=', 'stalled')],
            'target': 'current',
        }

    def action_view_pending_approvals(self):
        return {
            'name': _('Deals Awaiting Commercial Sign-off'),
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order',
            'view_mode': 'tree,kanban,form',
            'domain': [('risk_approval_state', 'in', ['pending_approval', 'pending_manager', 'pending_finance'])],
            'target': 'current',
        }

    def action_view_quotations(self):
        return {
            'name': _('Active Quotations (Draft & Sent)'),
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order',
            'view_mode': 'tree,kanban,form',
            'domain': [('state', 'in', ['draft', 'sent'])],
            'target': 'current',
        }

    def action_view_confirmed_orders(self):
        return {
            'name': _('Confirmed Sales Orders'),
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order',
            'view_mode': 'tree,kanban,form',
            'domain': [('state', '=', 'sale')],
            'target': 'current',
        }

    def action_view_subscriptions(self):
        return {
            'name': _('Hybrid Subscription Deals'),
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order',
            'view_mode': 'tree,kanban,form',
            'domain': [('is_recurring_hybrid', '=', True)],
            'target': 'current',
        }

    def action_view_billing_schedules(self):
        return {
            'name': _('Hybrid Billing Installments'),
            'type': 'ir.actions.act_window',
            'res_model': 'vantage.billing.schedule',
            'view_mode': 'tree,form',
            'target': 'current',
        }

    def action_view_fulfillment_deficits(self):
        return {
            'name': _('Orders with Inventory Deficit'),
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order',
            'view_mode': 'tree,kanban,form',
            'domain': [('has_split_requirement', '=', True)],
            'target': 'current',
        }

    def action_view_forked_backorders(self):
        return {
            'name': _('Forked Regional Backorder Lines'),
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order.line',
            'view_mode': 'tree,form',
            'domain': [('is_split_child', '=', True)],
            'target': 'current',
        }
