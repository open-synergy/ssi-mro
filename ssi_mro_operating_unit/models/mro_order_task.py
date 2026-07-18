# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class MroOrderTask(models.Model):  # pylint: disable=too-few-public-methods
    _name = "mro_order_task"
    _inherit = [
        "mro_order_task",
        "mixin.single_operating_unit",
    ]
