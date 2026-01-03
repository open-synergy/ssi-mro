# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class StockProductionLot(models.Model):
    _name = "stock.production.lot"
    _inherit = [
        "stock.production.lot",
    ]

    mro_action_ids = fields.One2many(
        comodel_name="mro_order.detail",
        string="MRO Actions",
        inverse_name="lot_id",
    )

    def action_open_mro_action(self):
        for record in self.sudo():
            result = record._open_mro_action()
        return result

    def _open_mro_action(self):
        self.ensure_one()
        return {
            "name": "MRO Actions",
            "type": "ir.actions.act_window",
            "res_model": "mro_order.detail",
            "view_mode": "tree,form",
            "domain": [("lot_id", "=", self.id)],
        }
