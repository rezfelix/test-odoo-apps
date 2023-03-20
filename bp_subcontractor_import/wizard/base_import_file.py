# Part of bloopark systems. See LICENSE file for full copyright and licensing details.

import base64
import binascii
import io
import logging
import tempfile

import xlrd
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools import pycompat

_logger = logging.getLogger(__name__)


class BaseImportFile(models.TransientModel):
    _name = "base.import.file"
    _description = "Base Import File"
    _rec_name = "file_type"

    file = fields.Binary(required=True)
    file_type = fields.Selection(
        [
            ("xls", "XLS File"),
            ("csv", "CSV File"),
        ],
        string="Select",
        default="xls",
        required=1,
    )
    separator = fields.Char(
        default=";",
        string="Separator (CSV)",
        help="Select the separator for CSV files.",
    )

    search_product_by_field = fields.Selection(
        [("default_code", "Internal Reference"), ("name", "Name")],
        string="Search product by field",
        default="name",
        help='Select the field to match the existing products. '
        'Is possible to check for exact matches based on product name '
        'or product internal reference.',
    )

    @api.model
    def read_file_data(self, file_type, file):
        """Load data from Uploaded file.

        :param file_type: str [csv, xlsx]
        :param file: selected file content (binary data)
        :return: dict of final file cleaned data
         ([('component1', '111'), ('component2', '112'), ('Finish product', 123)])
        """
        values = []
        first_column = []
        try:
            if file_type == "csv":
                data = base64.b64decode(file)
                reader = pycompat.csv_reader(
                    io.BytesIO(data),
                    quotechar='"',
                    delimiter=self.separator or ",",
                )
                first_column = next(reader)
                values = list(reader)
            elif file_type == "xls":
                fp = tempfile.NamedTemporaryFile(suffix=".xlsx")
                fp.write(binascii.a2b_base64(file))
                fp.seek(0)
                workbook = xlrd.open_workbook(fp.name)
                sheet = workbook.sheet_by_index(0)
                if sheet._cell_values:
                    first_column = sheet._cell_values[0]
                    values = sheet._cell_values[1:]

        except Exception as e:
            _logger.error(e)
            raise ValidationError(_(f"Something went wrong: {e}!"))
        mapped_value = map(
            lambda value: list(
                tuple(
                    zip(
                        first_column,
                        value,
                    )
                )
            ),
            values,
        )

        return list(mapped_value)
