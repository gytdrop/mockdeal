from odoo import models, fields

class HackathonItemFeatureA(models.Model):
    _inherit = 'hackathon.item'  # Extends existing model without file conflicts

    feature_a_score = fields.Float(string='Feature A Score')
