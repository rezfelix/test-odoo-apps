# Part of bloopark systems. See LICENSE file for full copyright and licensing details.

{
    "name": "Portal Timesheet Access",
    "sequence": 30,
    "description": """
    - This module give a portal user an access to add his timesheet on tasks.
    """,
    'images': ['static/description/cover.png'],
    'version': '15.0.0.0.1',
    "currency": "EUR",
    "price": "199",
    'category': 'Services/Project',
    "author": "Bloopark systems GmbH & Co. KG",
    "website": "http://www.bloopark.de",
    "license": "OPL-1",
    "depends": [
        "project",
        "hr_timesheet",
    ],
    "installable": True,
    "data": [
        # Security files
        "security/ir.model.access.csv",
        # View files
        "views/project_task_views.xml",
        "views/res_users_views.xml",
        "views/analytic_account_views.xml",
    ],
    "demo": [],
}
