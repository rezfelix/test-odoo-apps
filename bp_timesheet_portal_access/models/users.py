# Part of bloopark systems. See LICENSE file for full copyright and licensing details.


from odoo import fields, models


class ResUsers(models.Model):
    _inherit = "res.users"

    user_timesheet_only = fields.Boolean(
        string="Create/View Own Timesheet Only",
        copy=False,
        default=False,
    )
