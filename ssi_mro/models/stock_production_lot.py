# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class StockProductionLot(models.Model):
    _name = "stock.production.lot"
    _inherit = [
        "stock.production.lot",
    ]

    mro_order_task_ids = fields.One2many(
        comodel_name="mro_order_task",
        string="MRO Order Task",
        inverse_name="lot_id",
    )

    def action_open_mro_task(self):
        for record in self.sudo():
            result = record._open_mro_task()
        return result

    def _open_mro_task(self):
        self.ensure_one()
        return {
            "name": "MRO Order Tasks",
            "type": "ir.actions.act_window",
            "res_model": "mro_order_task",
            "view_mode": "tree,form",
            "domain": [("lot_id", "=", self.id)],
        }
