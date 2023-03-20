# Part of bloopark systems. See LICENSE file for full copyright and licensing details.


from odoo import fields, models


class EmployeeCertificateType(models.Model):
    _name = "employee.certificate.type"
    _description = "Employee Certificate Type"

    name = fields.Char(required=1)
    view_id = fields.Many2one(
        "ir.ui.view",
        domain="[('type','=','qweb'),('model','=',False)]",
    )
