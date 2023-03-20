# Part of bloopark systems. See LICENSE file for full copyright and licensing details.


from odoo import api, fields, models

NEW_FIELDS = {
    'task_name',
    'task_sequence',
    'last_child_sequence',
}


class ProjectTask(models.Model):
    _inherit = 'project.task'

    task_name = fields.Char(tracking=1)
    name = fields.Char(
        required=False,
        readonly=True,
        compute="_compute_name",
        store=True,
    )
    task_sequence = fields.Char(
        tracking=True,
        readonly=True,
        copy=False,
        default=False,
    )
    last_child_sequence = fields.Integer(copy=False)

    @property
    def SELF_READABLE_FIELDS(self):
        return super().SELF_READABLE_FIELDS | NEW_FIELDS

    @property
    def SELF_WRITABLE_FIELDS(self):
        return super().SELF_WRITABLE_FIELDS | NEW_FIELDS

    @api.depends("task_name", "task_sequence", "project_id")
    def _compute_name(self):
        for task in self.sudo():
            name = task.task_name or "New"
            if task.task_sequence:
                name = f"[{task.task_sequence}] {task.task_name}"
            task.name = name

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            name = vals.get('name') or vals.get("task_name") or False
            vals['task_name'] = vals.get('task_name') or name or False
        res = super().create(vals_list)
        res.set_task_sequence()
        return res

    def write(self, vals):
        res = super().write(vals)
        if 'project_id' in vals.keys() or vals.get("parent_id"):
            self.set_task_sequence()
        return res

    def get_task_sequence(self, project, parent_task=None):
        if not project.project_sequence_id:
            return False

        elif parent_task and project.sub_task_hierarchy_sequence:
            parent_task.last_child_sequence = parent_task.last_child_sequence + 1
            return self.generate_child_hierarchy_sequence(
                parent_task=parent_task,
            )
        return project.project_sequence_id.next_by_id()

    def set_task_sequence(self):
        for task in self:
            sequence = task.get_task_sequence(
                project=task.project_id,
                parent_task=task.parent_id,
            )
            task.task_sequence = sequence or ''
            task.child_ids.set_task_sequence()

    @api.model
    def generate_child_hierarchy_sequence(self, parent_task):
        padding = 2
        last_sequence = parent_task.last_child_sequence
        return f'{parent_task.task_sequence}-{str(last_sequence).zfill(padding)}'
