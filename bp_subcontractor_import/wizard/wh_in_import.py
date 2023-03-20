# Part of bloopark systems. See LICENSE file for full copyright and licensing details.

import base64
import logging

import xlrd
from odoo import _, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class WHInImport(models.TransientModel):
    _name = "wh.in.import"
    _inherit = "base.import.file"
    _description = "WH Import File"

    def action_confirm_wizard(self):
        """Perform actions based on the selected file:

        - Confirm the purchase order for the drop shipping
        - Create stock moves lines for the drop shipping but only for components.
        - Create stock moves lines for the finish products.
        - Assign the serial numbers from the files to the components and finish products.
        """
        values = self.read_file_data(
            file_type=self.file_type,
            file=self.file,
        )

        xl_workbook = xlrd.open_workbook(file_contents=base64.b64decode(self.file))
        xl_sheet = xl_workbook.sheet_by_index(0)
        ctx = self.env.context
        active_model = ctx.get("active_model")
        active_id = ctx.get("active_id")
        stock_move = self.env[active_model].browse(active_id)
        picking = stock_move.picking_id
        record_component_action = picking.action_record_components()
        mrp_id = record_component_action.get("res_id")
        production_comp = self.env["mrp.production"].browse(mrp_id)
        header_list = [i[0] for i in values[0]]

        finished_product = stock_move.product_id

        products = self.env["product.product"].search(
            [(self.search_product_by_field, "in", header_list)]
        )
        if finished_product not in products:
            raise UserError(
                _(f"Product ({finished_product.name}) was not found in the file")
            )

        if stock_move.product_uom_qty != len(values):
            raise UserError(
                _(
                    f"You're trying to import "
                    f"({len(values)}) lines, but only"
                    f" {stock_move.product_uom_qty} units should be imported."
                )
            )

        procurement_group = production_comp.procurement_group_id
        po_line = procurement_group.stock_move_ids.mapped("created_purchase_line_id")
        purchase_order_ids = (
            po_line.order_id
            | procurement_group.stock_move_ids.move_orig_ids.purchase_line_id.order_id
        ).ids
        for order in purchase_order_ids:
            purchase_order = self.env["purchase.order"].browse(order)

            if purchase_order.state == "draft":
                purchase_order.button_confirm()

        picking_ids = purchase_order.picking_ids
        if picking_ids:
            for picking in picking_ids:
                picking.mapped("move_line_ids").unlink()

                self._import_serial_number(xl_sheet, picking, finished_product)
                picking.button_validate()

        self.action_record_components(
            stock_move=stock_move,
            production_comp=production_comp,
            values=values,
        )

    def _import_serial_number(self, xl_sheet, picking, finished_product):
        """import serial numbers only for the components."""
        product_file_set = set()
        serial_list = []

        for col_idx in range(0, xl_sheet.ncols):
            product = str(xl_sheet.cell(0, col_idx).value)
            product_file_set.add(product)
            for row_idx in range(1, xl_sheet.nrows):
                serial = str(xl_sheet.cell(row_idx, col_idx).value)
                serial_list.append((product, serial))

        products = self.env["product.product"].search(
            [(self.search_product_by_field, "in", list(product_file_set))]
        )
        stock_move_values = []
        for item in serial_list:
            product = products.filtered(
                lambda p: p[self.search_product_by_field] == item[0]
            )

            if product and finished_product != product and item[1]:
                stock_move_values.append(
                    {
                        "picking_id": picking.id,
                        "location_id": picking.location_id.id,
                        "location_dest_id": picking.location_dest_id.id,
                        "product_id": product.id,
                        "product_uom_id": product.uom_id.id,
                        "lot_name": item[1],
                        "product_uom_qty": 0.0,
                        "qty_done": 1.0,
                    }
                )
        if stock_move_values:
            self.env['stock.move.line'].create(stock_move_values)

    def action_record_components(self, stock_move, production_comp, values):
        mrp = self.env["mrp.production"]
        lot = self.env["stock.production.lot"]
        stock_move.date_deadline = stock_move.picking_id.date_deadline
        production_comp.qty_producing = 1
        production_comp._set_qty_producing()
        if self.search_product_by_field == "name":
            finished_product = stock_move.product_id.name
        elif self.search_product_by_field == "default_code":
            finished_product = stock_move.product_id.default_code

        for row in values:
            production_comp.move_line_raw_ids.unlink()
            finished_lots = [y[1] for y in row if y[0] == finished_product]
            row_component_lots = [y[1] for y in row if y[0] != finished_product]
            comp_lots = lot.search([("name", "in", row_component_lots)])
            move_line_raw_ids_list = [
                (
                    0,
                    0,
                    {
                        "product_id": comp_lot.product_id.id,
                        "lot_id": comp_lot.id,
                        "company_id": production_comp.company_id.id,
                        "product_uom_id": production_comp.product_uom_id.id,
                        "location_id": production_comp.location_src_id.id,
                        "location_dest_id": production_comp.location_dest_id.id,
                        "qty_done": 1,
                    },
                )
                for comp_lot in comp_lots
            ]
            production_comp.move_line_raw_ids = move_line_raw_ids_list
            if isinstance(finished_lots[0], float):
                lo_name = int(finished_lots[0])
            else:
                lo_name = str(finished_lots[0])
            production_comp.lot_producing_id = lot.create(
                {
                    "name": lo_name,
                    "product_id": stock_move.product_id.id,
                    "company_id": stock_move.company_id.id,
                    "product_uom_id": stock_move.product_uom.id,
                }
            )
            act_record = production_comp.subcontracting_record_component()
            if new_mrp_action_id := act_record.get("res_id"):
                production_comp = mrp.browse(new_mrp_action_id)
