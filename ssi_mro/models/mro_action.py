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
    # Product Category
    product_category_selection_method = fields.Selection(
        default="domain",
        selection=[("manual", "Manual"), ("domain", "Domain"), ("code", "Python Code")],
        string="Product Category Selection Method",
        required=True,
    )
    product_category_ids = fields.Many2many(
        comodel_name="product.category",
        string="Product Categories",
        relation="rel_mro_action_2_product_category",
        column1="mro_action_id",
        column2="product_category_id",
    )
    product_category_domain = fields.Text(
        default="[]", string="Product Category Domain"
    )
    product_category_python_code = fields.Text(
        default="result = []", string="Product Category Python Code"
    )

    # Product
    product_selection_method = fields.Selection(
        default="domain",
        selection=[("manual", "Manual"), ("domain", "Domain"), ("code", "Python Code")],
        string="Product Selection Method",
        required=True,
    )
    product_ids = fields.Many2many(
        comodel_name="product.product",
        string="Products",
        relation="rel_mro_action_2_product_product",
        column1="mro_action_id",
        column2="product_product_id",
    )
    product_domain = fields.Text(default="[]", string="Product Domain")
    product_python_code = fields.Text(
        default="result = []", string="Product Python Code"
    )
