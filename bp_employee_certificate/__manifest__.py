# Part of bloopark systems. See LICENSE file for full copyright and licensing details.

{
    "name": "Employees Certificates",
    "version": "15.0.0.0.1",
    "category": "hr",
    "currency": "EUR",
    "price": "99",
    "summary": "Employees Certificates",
    'images': ['static/description/certificate-cover.svg'],
    "depends": [
        "http_routing",
        "hr",
    ],
    "author": "bloopark systems GmbH & Co. KG",
    "maintainer": "bloopark systems GmbH & Co. KG",
    "license": "OPL-1",
    "website": "https://www.bloopark.de",
    "data": [
        # Security files
        "security/ir.model.access.csv",
        "security/security.xml",
        # View files
        "views/employee_certificate_views.xml",
        "views/certificate_type_views.xml",
        "views/menuitems.xml",
        # Data files
        "data/mail_template_data.xml",
        # Reports files
        "reports/certificate_template.xml",
    ],
    "installable": True,
    "application": True,
}
