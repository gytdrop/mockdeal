from odoo import models, fields

class HackathonBaseItem(models.Model):
    _name = 'hackathon.item'
    _description = 'Core Hackathon Entity'

    name = fields.Char(string='Item Name', required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('done', 'Completed')
    ], default='draft', string='Status')
