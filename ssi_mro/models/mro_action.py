# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class MroAction(models.Model):
    _name = "mro_action"
    _description = "MRO Action"
    _inherit = [
        "mixin.master_data",
    ]

    kind = fields.Selection(
        selection=[
            ("maintenance", "Maintenance"),
            ("repair", "Repair"),
            ("overhaul", "Overhaul"),
        ],
        string="Kind",
        required=True,
        default="maintenance",
    )
