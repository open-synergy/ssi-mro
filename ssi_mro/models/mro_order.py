# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import date

from odoo import api, fields, models

from odoo.addons.ssi_decorator import ssi_decorator


class MroOrder(models.Model):
    _name = "mro_order"
    _description = "MRO Order"
    _inherit = [
        "mixin.transaction_cancel",
        "mixin.transaction_done",
        "mixin.transaction_open",
        "mixin.transaction_confirm",
        "mixin.many2one_configurator",
    ]

    # mixin.multiple_approval attributes
    _approval_from_state = "draft"
    _approval_to_state = "open"
    _approval_state = "confirm"
    _after_approved_method = "action_open"

    # Attributes related to add element on view automatically
    _automatically_insert_view_element = True
    _automatically_insert_open_button = False
    _automatically_insert_open_policy_fields = False

    # Attributes related to add element on form view automatically
    _statusbar_visible_label = "draft,confirm,open"
    _policy_field_order = [
        "confirm_ok",
        "approve_ok",
        "reject_ok",
        "restart_approval_ok",
        "done_ok",
        "cancel_ok",
        "restart_ok",
        "manual_number_ok",
    ]
    _header_button_order = [
        "action_confirm",
        "action_approve",
        "action_reject",
        "action_done",
        "%(ssi_transaction_cancel_mixin.base_select_cancel_reason_action)d",
        "action_restart",
        "action_recompute_all_fields",
    ]

    # Attributes related to add element on search view automatically
    _state_filter_order = [
        "dom_draft",
        "dom_confirm",
        "dom_open",
        "dom_done",
        "dom_cancel",
        "dom_terminate",
        "dom_reject",
    ]

    # Sequence attribute
    _create_sequence_state = "open"

    date = fields.Date(
        string="Date",
        required=True,
        readonly=True,
        states={
            "draft": [("readonly", False)],
        },
        default=lambda self: date.today(),
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
    type_id = fields.Many2one(
        comodel_name="mro_type",
        string="Type",
        required=True,
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
    customer_id = fields.Many2one(
        comodel_name="res.partner",
        string="Customer",
        readonly=True,
        states={
            "draft": [("readonly", False)],
        },
    )
    vendor_id = fields.Many2one(
        comodel_name="res.partner",
        string="Vendor",
        readonly=True,
        states={
            "draft": [("readonly", False)],
        },
    )
    task_ids = fields.One2many(
        comodel_name="mro_order_task",
        inverse_name="order_id",
        string="MRO Order Tasks",
        readonly=False,
        states={
            "draft": [("readonly", False)],
        },
        copy=False,
    )
    allowed_mro_task_ids = fields.Many2many(
        comodel_name="mro_order_task",
        string="Allowed MRO Tasks",
        compute="_compute_allowed_mro_task_ids",
        compute_sudo=True,
        store=False,
    )
    num_of_tasks = fields.Integer(
        string="Σ Tasks",
        compute="_compute_num_of_tasks",
        compute_sudo=True,
        store=True,
    )
    num_of_open_tasks = fields.Integer(
        string="Σ Open Tasks",
        compute="_compute_num_of_tasks",
        compute_sudo=True,
        store=True,
    )
    num_of_done_tasks = fields.Integer(
        string="Σ Done Tasks",
        compute="_compute_num_of_tasks",
        compute_sudo=True,
        store=True,
    )
    num_of_canceled_tasks = fields.Integer(
        string="Σ Canceled Tasks",
        compute="_compute_num_of_tasks",
        compute_sudo=True,
        store=True,
    )
    num_of_terminated_tasks = fields.Integer(
        string="Σ Terminated Tasks",
        compute="_compute_num_of_tasks",
        compute_sudo=True,
        store=True,
    )
    task_is_finished = fields.Boolean(
        string="Task is Finished",
        compute="_compute_num_of_tasks",
        compute_sudo=True,
        store=True,
    )

    @api.depends(
        "task_ids",
        "task_ids.state",
    )
    def _compute_num_of_tasks(self):
        for record in self:
            record.num_of_tasks = len(record.task_ids)
            record.num_of_open_tasks = len(
                record.task_ids.filtered(
                    lambda r: r.state in ["draft", "confirm", "ready", "open"]
                )
            )
            record.num_of_done_tasks = len(
                record.task_ids.filtered(lambda r: r.state == "done")
            )
            record.num_of_canceled_tasks = len(
                record.task_ids.filtered(lambda r: r.state == "cancel")
            )
            record.num_of_terminated_tasks = len(
                record.task_ids.filtered(lambda r: r.state == "terminate")
            )
            if record.num_of_tasks == (
                record.num_of_done_tasks
                + record.num_of_canceled_tasks
                + record.num_of_terminated_tasks
            ):
                record.task_is_finished = True
            else:
                record.task_is_finished = False

    @api.depends("type_id")
    def _compute_allowed_product_ids(self):
        for record in self:
            result = False
            if record.type_id:
                result = record._m2o_configurator_get_filter(
                    object_name="product.product",
                    method_selection=record.type_id.product_selection_method,
                    manual_recordset=record.type_id.product_ids,
                    domain=record.type_id.product_domain,
                    python_code=record.type_id.product_python_code,
                )
            record.allowed_product_ids = result

    @api.depends("type_id")
    def _compute_allowed_product_category_ids(self):
        for record in self:
            result = False
            if record.type_id:
                result = record._m2o_configurator_get_filter(
                    object_name="product.category",
                    method_selection=record.type_id.product_category_selection_method,
                    manual_recordset=record.type_id.product_category_ids,
                    domain=record.type_id.product_category_domain,
                    python_code=record.type_id.product_category_python_code,
                )
            record.allowed_product_category_ids = result

    @api.depends(
        "type_id",
    )
    def _compute_allowed_mro_task_ids(self):
        for record in self:
            domain = []
            if record.type_id:
                domain = [
                    "|",
                    ("product_id", "in", record.allowed_product_ids.ids),
                    (
                        "product_id.categ_id",
                        "in",
                        record.allowed_product_category_ids.ids,
                    ),
                    ("order_id", "=", False),
                    ("state", "=", "ready"),
                    "|",
                    "|",
                    "&",
                    ("earliest_date", "=", False),
                    ("latest_date", "=", False),
                    ("earliest_date", "<=", record.date),
                    ("latest_date", ">=", record.date),
                ]
            record.allowed_mro_task_ids = self.env["mro_order_task"].search(domain)

    def action_load_task(self):
        for record in self.sudo():
            record._load_task()

    def _load_task(self):
        self.ensure_one()
        self.task_ids.write({"order_id": False})
        for task in self.allowed_mro_task_ids:
            task.write({"order_id": self.id})

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
            "open_ok",
            "restart_ok",
            "reject_ok",
            "manual_number_ok",
            "restart_approval_ok",
        ]
        res += policy_field
        return res
