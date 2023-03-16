
from odoo import conf, http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal


class TestProjectTaskPortal(CustomerPortal):

    @http.route(['/open/task/<int:task_id>'], type='http', auth="public")
    def open_task(self, task_id, **kwargs):
        task = request.env['project.task'].sudo().browse(task_id)
        return request.render(
            'test_project.task_sharing_portal',
            {'task_id': task.id},
        )
