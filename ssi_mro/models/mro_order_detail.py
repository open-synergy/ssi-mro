# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class MroOrderDetail(models.Model):
    _name = "mro_order.detail"
    _description = "MRO Order Detail"
    _order = "order_id, sequence"

    order_id = fields.Many2one(
        comodel_name="mro_order",
        string="MRO Order",
        required=True,
        ondelete="cascade",
    )
    sequence = fields.Integer(
        string="Sequence",
        default=10,
        required=True,
    )
    lot_id = fields.Many2one(
        comodel_name="stock.production.lot",
        string="Lot",
        related="order_id.lot_id",
        store=True,
        readonly=True,
    )
    action_id = fields.Many2one(
        comodel_name="mro_action",
        string="Action",
        required=True,
        ondelete="restrict",
    )
    next_mro_date = fields.Date(
        string="Next Date",
    )
    notes = fields.Text(
        string="Notes",
    )
