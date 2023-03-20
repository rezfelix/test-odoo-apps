# Part of bloopark systems. See LICENSE file for full copyright and licensing details.


from odoo import Command
from odoo.addons.mail.tests.common import mail_new_test_user
from odoo.tests.common import Form, TransactionCase


class TestProject(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        ir_sequence = cls.env['ir.sequence']
        project = cls.env['project.project']
        ctx = {
            'mail_create_nolog': True,
        }
        project_vals = {
            'name': 'Project with sequence',
            'privacy_visibility': 'portal',
            'alias_name': 'Project with sequence',
            'project_sequence_id': (
                ir_sequence.create(
                    {
                        'name': 'Project with sequence',
                        'padding': 5,
                    }
                )
            ).id,
        }
        cls.user_portal = mail_new_test_user(
            cls.env,
            login='user_portal',
            name='User Portal',
            groups='base.group_portal',
        )
        cls.partner_portal = cls.env['res.partner'].create(
            {
                'name': 'Chell Gladys',
                'email': 'chell@gladys.portal',
                'company_id': False,
                'user_ids': [
                    Command.link(cls.user_portal.id),
                ],
            }
        )
        cls.project_with_sequence = project.with_context(ctx).create(project_vals)
        cls.project_with_sequence.project_sequence_id.write(
            {
                "res_model": "project.project",
                "res_id": cls.project_with_sequence.id,
            }
        )

    def test_case001_task_sequence(self):
        """Task should take the next number of project sequence."""
        project_sequence = self.project_with_sequence.project_sequence_id
        number_next = project_sequence.number_next_actual
        next_sequence = project_sequence.get_next_char(number_next)
        with Form(
            self.env['project.task'].with_context(
                {
                    'tracking_disable': True,
                    'default_project_id': self.project_with_sequence.id,
                }
            )
        ) as task_form:
            task_form.task_name = 'Test Task 1'
        task = task_form.save()
        self.assertEqual(task.task_sequence, next_sequence)

    def test_case002_task_name(self):
        """Task name contain the next number of project sequence and task name."""
        with Form(
            self.env['project.task'].with_context(
                {
                    'tracking_disable': True,
                    'default_project_id': self.project_with_sequence.id,
                }
            )
        ) as task_form:
            task_form.task_name = 'Test Task name'
        task = task_form.save()
        self.assertEqual(task.name, f"[{task.task_sequence}] {task.task_name}")
