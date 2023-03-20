# Part of bloopark systems. See LICENSE file for full copyright and licensing details.

from . import models
from odoo import api, SUPERUSER_ID


def _post_init_hook(cr, registry):
    cr.execute("UPDATE project_task SET task_name=name")
