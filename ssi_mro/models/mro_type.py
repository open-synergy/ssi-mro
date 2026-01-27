# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class MroType(models.Model):
    _name = "mro_type"
    _description = "MRO Type"
    _inherit = [
        "mixin.master_data",
    ]

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
        relation="rel_mro_type_2_product_category",
        column1="mro_type_id",
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
        relation="rel_mro_type_2_product_product",
        column1="mro_type_id",
        column2="product_product_id",
    )
    product_domain = fields.Text(default="[]", string="Product Domain")
    product_python_code = fields.Text(
        default="result = []", string="Product Python Code"
    )

    # Action
    action_selection_method = fields.Selection(
        default="domain",
        selection=[("manual", "Manual"), ("domain", "Domain"), ("code", "Python Code")],
        string="Action Selection Method",
        required=True,
    )
    action_ids = fields.Many2many(
        comodel_name="mro_action",
        string="Actions",
        relation="rel_mro_type_2_mro_action",
        column1="mro_type_id",
        column2="mro_action_id",
    )
    action_domain = fields.Text(default="[]", string="Action Domain")
    action_python_code = fields.Text(default="result = []", string="Action Python Code")
