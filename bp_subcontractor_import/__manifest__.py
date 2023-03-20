# Part of bloopark systems. See LICENSE file for full copyright and licensing details.

{
    "name": "Subcontractor Serial Numbers Import",
    "sequence": 20,
    "currency": "EUR",
    "price": "149",
    'images': ['static/description/cover.png'],
    "description": """
    - This module extends the functionality of stock module to allow import serial
    numbers for Subcontractors from an excel or CSV file.
    """,
    "version": "15.1",
    "category": "Inventory/Inventory",
    "author": "bloopark systems GmbH & Co. KG",
    "website": "http://www.bloopark.de",
    "license": "OPL-1",
    "depends": [
        "mrp_subcontracting_dropshipping",
        "mrp_subcontracting_purchase",
    ],
    "external_dependencies": {"python": ["xlrd"]},
    "installable": True,
    "auto_install": False,
    "application": False,
    "data": [
        # Security files
        "security/ir.model.access.csv",
        # Wizard files
        "wizard/wh_in_import_view.xml",
        # View files
        "views/stock_picking_views.xml",
    ],
    "demo": [],
}
