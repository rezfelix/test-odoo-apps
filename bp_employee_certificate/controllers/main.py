from odoo import http
from odoo.http import request
from odoo.tools.translate import _


class DiscussController(http.Controller):
    @http.route('/certificate/<string:certificate_token>', type='http', auth='public')
    def public_employee_certificate(self, **kwargs):
        certificate_token = kwargs.get("certificate_token")
        certificate = (
            request.env["employee.certificate"]
            .sudo()
            .get_website_certificate(
                token=certificate_token,
            )
        )

        if not certificate_token or not certificate:
            return request.render(
                'http_routing.http_error',
                {
                    'status_code': _('Oops'),
                    'status_message': _(
                        """
                        The requested certificate is not valid, or doesn't exist anymore.
                        """
                    ),
                },
            )
        template_id = certificate.get_website_certificat_view()

        return request.render(
            template_id,
            {
                'docs': certificate,
            },
        )
