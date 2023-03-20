# Part of bloopark systems. See LICENSE file for full copyright and licensing details.

{
    "name": "Project Task/Sub-Task Sequence",
    "sequence": 30,
    "currency": "EUR",
    "price": "149",
    'images': ['static/description/image.png'],
    "summary": """
    Project Task/Sub-Task Sequence
    """,
    "description": """
        With this module, the project management module (Project) allows you to
        handle tasks and their sequences.

        The project module allows you to create tasks, assign them to team members,
        set deadlines, and track
        progress. The tasks can be organized using the Gantt view, which allows you
        to see the dependencies
        and
        sequences of the tasks. Additionally, you can also use the kanban view to see
         the tasks in columns
        based
        on their status (e.g. to do, in progress, done). The project module also allows
        you to create
        subtasks
        for a task and link them to the main task. It also allows you to manage the task
         workflow, set up
        reminders and notifications, and track time spent on tasks.

        In Odoo, the Project module allows you to handle task sequences, and it also
        provides a way to
        access it
        via the portal. The portal users can view and search on the tasks and task
        sequence that have access
        on them, track their progress, and update their status. Additionally,
        the portal users can also show
        all tasks in Kanban view of the project, which shows the task sequences,
        dependencies and progress of the
        project. They can also view the project milestones and deadlines,
        and add comments or attachments to
        the tasks. However, the portal users may not have the permission to create or
        modify tasks, they can only view their assigned tasks and update their status.

        It's important to note that the Project module needs to be installed and
         configured properly to use
        it
        via the portal. Additionally, the access rights of the portal users needs
         to be configured to allow
        them
        to access the project module and related information.
    """,
    'version': '15.0.0.0.1',
    'category': 'Services/Project',
    "author": "Bloopark systems GmbH & Co. KG",
    "website": "http://www.bloopark.de",
    "license": "OPL-1",
    "depends": [
        "project",
    ],
    "installable": True,
    "currency": "EUR",
    "auto_install": True,
    "application": True,
    'post_init_hook': '_post_init_hook',
    "data": [
        # View files
        "views/project_views.xml",
        "views/task_views.xml",
        "views/ir_sequence_views.xml",
    ],
    "demo": [],
}
