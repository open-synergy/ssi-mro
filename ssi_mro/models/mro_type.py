# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class MroType(models.Model):
    _name = "mro_type"
    _description = "MRO Type"
    _inherit = [
        "mixin.master_data",
    ]
