# Part of bloopark systems. See LICENSE file for full copyright and licensing details.


from odoo import fields, models


class Project(models.Model):
    _inherit = 'project.project'

    project_sequence_id = fields.Many2one("ir.sequence", copy=False)
    sub_task_hierarchy_sequence = fields.Boolean(string="Hierarchy Sub-task Sequence")

    def action_reset_tasks_sequence(self):
        for project in self:
            parent_tasks = project.task_ids.filtered(lambda t: not t.parent_id)
            parent_tasks.write(
                {
                    "last_child_sequence": 0,
                }
            )
            parent_tasks.set_task_sequence()
