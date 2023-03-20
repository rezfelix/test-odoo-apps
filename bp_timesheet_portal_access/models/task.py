# Part of bloopark systems. See LICENSE file for full copyright and licensing details.


from odoo import _, fields, models
from odoo.exceptions import UserError

NEW_FIELDS = {
    "view_only_timesheet",
    "view_only_timesheet_ids",
}


class ProjectTask(models.Model):
    _inherit = 'project.task'

    view_only_timesheet = fields.Boolean(
        compute="_compute_view_only_timesheet",
    )
    view_only_timesheet_ids = fields.Many2many(
        "Timesheet Lines",
        "account.analytic.line",
        'task_timesheet_rel',
        'proj_task_id',
        'timesheet_line_id',
        compute="_compute_view_only_timesheet",
    )

    @property
    def SELF_READABLE_FIELDS(self):
        return super().SELF_READABLE_FIELDS | NEW_FIELDS

    @property
    def SELF_WRITABLE_FIELDS(self):
        return super().SELF_WRITABLE_FIELDS | NEW_FIELDS

    def _compute_view_only_timesheet(self):
        portal_user = self.env.user.has_group('base.group_portal')
        user_timesheet_only = self.env.user.user_timesheet_only
        view_only_condition = portal_user and user_timesheet_only

        self.view_only_timesheet = view_only_condition
        if not view_only_condition:
            self.view_only_timesheet_ids = False
            return

        for task in self:
            task.view_only_timesheet_ids = task.timesheet_ids.filtered(
                lambda t: t.employee_id.user_id.id == self.env.user.id
            )

    def action_portal_timesheet(self):
        self.ensure_one()
        project = self.project_id
        employee = self.env.user.employee_id or self.env["hr.employee"].sudo().search(
            [
                "|",
                ("address_home_id", "=", self.env.user.partner_id.id),
                ("user_id", "=", self.env.user.id),
            ],
            limit=1,
        )
        if not employee:
            raise UserError(_("Your account is not linked to any employee!"))

        return {
            'type': 'ir.actions.act_window',
            'name': self.display_name,
            'res_model': 'account.analytic.line',
            'view_mode': 'list,form',
            'context': {
                'default_project_id': project.id,
                'default_user_id': self.env.user.id,
                'default_task_id': self.id,
                'default_name': "/",
                'default_employee_id': employee.id,
            },
            'domain': [
                ('project_id', '=', project.id),
                ('employee_id', '=', employee.id),
                ('task_id', '=', self.id),
            ],
        }
