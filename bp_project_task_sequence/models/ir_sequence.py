# Part of bloopark systems. See LICENSE file for full copyright and licensing details.


from odoo import fields, models


class IrSequence(models.Model):
    _inherit = 'ir.sequence'

    res_model = fields.Char(copy=False, string="Model Name")
    res_id = fields.Integer(copy=False, string="Related Record")
