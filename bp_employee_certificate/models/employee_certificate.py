# Part of bloopark systems. See LICENSE file for full copyright and licensing details.


import base64
import logging
import secrets
import string
from io import BytesIO

import qrcode
from num2words import num2words
from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class EmployeeCertificate(models.Model):
    _name = "employee.certificate"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Employee Certificate"

    name = fields.Char(required=1, string="Description", tracking=True)
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("confirm", "Confirmed/Published"),
            ("cancel", "Cancelled"),
        ],
        default="draft",
        tracking=True,
        readonly=True,
    )
    active = fields.Boolean(
        default=True,
        tracking=True,
        readonly=True,
    )
    date = fields.Date(
        required=1,
        tracking=True,
        readonly=True,
    )
    employee_id = fields.Many2one(
        "hr.employee",
        required=True,
        tracking=True,
        readonly=True,
    )
    company_id = fields.Many2one(
        "res.company",
        required=True,
        tracking=True,
        readonly=True,
    )
    certificate_type_id = fields.Many2one(
        "employee.certificate.type",
        tracking=True,
        readonly=True,
    )
    view_id = fields.Many2one(
        "ir.ui.view",
        domain="[('type','=','qweb'),('model','=',False)]",
        tracking=True,
        readonly=True,
    )
    qr_code = fields.Binary(
        'QRcode',
        compute="_compute_generate_qr",
        readonly=True,
    )
    token = fields.Char(
        default=False,
        copy=False,
        readonly=True,
    )
    certificate_url = fields.Char(
        string="url",
        compute="_compute_certificate_url",
    )
    certificate_years = fields.Integer(string="Years Of Certificate")
    ceo_signature = fields.Binary()
    hr_signature = fields.Binary()
    ceo_employee_id = fields.Many2one("hr.employee")
    hr_employee_id = fields.Many2one("hr.employee")

    def _compute_certificate_url(self):
        url = self.get_base_url()
        for record in self:
            record.certificate_url = (
                f"{url}/certificate/{record.token}" if record.token else ""
            )

    def _compute_generate_qr(self):
        opaque_pixel = (0, 0, 0, 255)
        transparent_pixel = (255, 255, 255, 0)
        for rec in self:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=3,
                border=4,
            )
            qr.add_data(rec.certificate_url)
            qr.make(fit=True)
            img = qr.make_image()

            # To make it qr image transparent
            img = img.convert("RGBA")
            img_data = img.getdata()
            new_pixels = [
                transparent_pixel if all(i == 255 for i in item) else opaque_pixel
                for item in img_data
            ]
            img.putdata(new_pixels)
            temp = BytesIO()

            img.save(temp, format="PNG")
            qr_image = base64.b64encode(temp.getvalue())
            rec.qr_code = qr_image or False

    @api.onchange("certificate_type_id")
    def _onchange_certificate_type(self):
        self.view_id = self.certificate_type_id.view_id

    @api.onchange("employee_id")
    def _onchange_employee(self):
        self.company_id = self.employee_id.company_id.id

    def action_generate_token(self):
        for record in self.filtered(lambda l: not l.token):
            token = f"""{record.id}{''.join(
                secrets.choice(string.ascii_uppercase + string.digits) for _ in range(32))
            }"""
            record.token = token or ""

    def action_send_mail_certificate(self):
        invite_template = self.env.ref(
            'bp_employee_certificate.mail_template_send_employee_certificate'
        )
        for record in self:
            email = record.employee_id.work_email or record.employee_id.user_id.login
            invite_template.send_mail(
                record.id,
                force_send=True,
                email_values={'email_to': email},
            )

    def action_draft(self):
        return self.write(
            {
                "state": "draft",
            }
        )

    def action_confirm(self):
        self.action_generate_token()
        self.action_send_mail_certificate()
        return self.write(
            {
                "state": "confirm",
            }
        )

    def action_cancel(self):
        return self.write(
            {
                "state": "cancel",
            }
        )

    @api.model
    def concert_num2words(self, number):
        return num2words(number, lang='en').title()

    @api.model
    def get_website_certificate(self, token):
        return self.search(
            [
                ("token", "=", token or ""),
                ("state", "=", "confirm"),
            ],
            limit=1,
        )

    def get_website_certificat_view(self):
        self.ensure_one()
        return self.view_id.id or "bp_employee_certificate.certificate_template"
