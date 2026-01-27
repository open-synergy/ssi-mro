# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import date

from odoo import api, fields, models

from odoo.addons.ssi_decorator import ssi_decorator


class MroOrderTask(models.Model):
    _name = "mro_order_task"
    _description = "MRO Order Task"

    _inherit = [
        "mixin.transaction_terminate",
        "mixin.transaction_cancel",
        "mixin.transaction_done",
        "mixin.transaction_open",
        "mixin.transaction_ready",
        "mixin.transaction_confirm",
        "mixin.many2one_configurator",
    ]

    # mixin.multiple_approval attributes
    _approval_from_state = "draft"
    _approval_to_state = "ready"
    _approval_state = "confirm"
    _after_approved_method = "action_ready"

    # Attributes related to add element on view automatically
    _automatically_insert_view_element = True
    _automatically_insert_ready_button = False
    _automatically_insert_ready_policy_fields = False

    # Attributes related to add element on form view automatically
    _statusbar_visible_label = "draft,confirm,ready,open"
    _policy_field_order = [
        "confirm_ok",
        "approve_ok",
        "reject_ok",
        "restart_approval_ok",
        "ready_ok",
        "open_ok",
        "done_ok",
        "cancel_ok",
        "terminate_ok",
        "restart_ok",
        "manual_number_ok",
    ]
    _header_button_order = [
        "action_confirm",
        "action_approve",
        "actiion_open",
        "action_done",
        "action_reject",
        "%(ssi_transaction_cancel_mixin.base_select_cancel_reason_action)d",
        "%(ssi_transaction_terminate_mixin.base_select_terminate_reason_action)d",
        "action_restart",
        "action_recompute_all_fields",
    ]

    # Attributes related to add element on search view automatically
    _state_filter_order = [
        "dom_draft",
        "dom_confirm",
        "dom_ready",
        "dom_open",
        "dom_done",
        "dom_cancel",
        "dom_terminate",
        "dom_reject",
    ]

    # Sequence attribute
    _create_sequence_state = "ready"

    order_id = fields.Many2one(
        comodel_name="mro_order",
        string="MRO Order",
        required=False,
        ondelete="restrict",
        readonly=True,
        copy=False,
    )
    date = fields.Date(
        string="Date",
        required=True,
        readonly=True,
        states={
            "draft": [("readonly", False)],
        },
        default=lambda self: date.today(),
    )
    action_id = fields.Many2one(
        comodel_name="mro_action",
        string="Action",
        required=True,
        ondelete="restrict",
        readonly=True,
        states={
            "draft": [("readonly", False)],
        },
    )
    allowed_product_ids = fields.Many2many(
        comodel_name="product.product",
        string="Allowed Products",
        compute="_compute_allowed_product_ids",
        store=False,
        compute_sudo=True,
    )
    allowed_product_category_ids = fields.Many2many(
        comodel_name="product.category",
        string="Allowed Product Category",
        compute="_compute_allowed_product_category_ids",
        store=False,
        compute_sudo=True,
    )
    earliest_date = fields.Date(
        string="Earliest Date",
        required=False,
        readonly=True,
        states={
            "draft": [("readonly", False)],
        },
    )
    latest_date = fields.Date(
        string="Latest Date",
        required=False,
        readonly=True,
        states={
            "draft": [("readonly", False)],
        },
    )
    actual_finish_date = fields.Date(
        string="Actual Finish Date",
        required=False,
        readonly=True,
        states={
            "open": [
                ("readonly", False),
                ("required", True),
            ],
        },
    )
    product_id = fields.Many2one(
        comodel_name="product.product",
        string="Product",
        required=True,
        readonly=True,
        states={
            "draft": [("readonly", False)],
        },
    )
    lot_id = fields.Many2one(
        comodel_name="stock.production.lot",
        string="Serial Number",
        required=True,
        readonly=True,
        states={
            "draft": [("readonly", False)],
        },
    )

    @api.depends("action_id")
    def _compute_allowed_product_ids(self):
        for record in self:
            result = False
            if record.action_id:
                result = record._m2o_configurator_get_filter(
                    object_name="product.product",
                    method_selection=record.action_id.product_selection_method,
                    manual_recordset=record.action_id.product_ids,
                    domain=record.action_id.product_domain,
                    python_code=record.action_id.product_python_code,
                )
            record.allowed_product_ids = result

    @api.depends("action_id")
    def _compute_allowed_product_category_ids(self):
        for record in self:
            result = False
            if record.action_id:
                result = record._m2o_configurator_get_filter(
                    object_name="product.category",
                    method_selection=record.action_id.product_category_selection_method,
                    manual_recordset=record.action_id.product_category_ids,
                    domain=record.action_id.product_category_domain,
                    python_code=record.action_id.product_category_python_code,
                )
            record.allowed_product_category_ids = result

    @api.onchange("product_id")
    def onchange_lot_id(self):
        self.lot_id = False

    @ssi_decorator.insert_on_form_view()
    def _insert_form_element(self, view_arch):
        if self._automatically_insert_view_element:
            view_arch = self._reconfigure_statusbar_visible(view_arch)
        return view_arch

    @api.model
    def _get_policy_field(self):
        res = super()._get_policy_field()
        policy_field = [
            "confirm_ok",
            "approve_ok",
            "reject_ok",
            "done_ok",
            "cancel_ok",
            "terminate_ok",
            "open_ok",
            "restart_ok",
            "reject_ok",
            "manual_number_ok",
            "restart_approval_ok",
        ]
        res += policy_field
        return res
