# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "MRO",
    "version": "14.0.1.0.0",
    "website": "https://github.com/open-synergy/ssi-mro",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "application": False,
    "depends": [
        "ssi_master_data_mixin",
        "ssi_transaction_mixin",
        "ssi_stock",
    ],
    "data": [
        "security/ir_module_category/mro_order_module_category.xml",
        "security/res_groups/mro_type.xml",
        "security/res_groups/mro_action.xml",
        "security/res_groups/mro_order.xml",
        "security/ir_model_access/mro_type.xml",
        "security/ir_model_access/mro_action.xml",
        "security/ir_model_access/mro_order.xml",
        "security/ir_rule/mro_order.xml",
        "ir_sequence/mro_order.xml",
        "sequence_template/mro_order.xml",
        "approval_template/mro_order.xml",
        "policy_template/mro_order.xml",
        "views/mro_type.xml",
        "views/mro_action.xml",
        "views/mro_order_views.xml",
        "views/mro_order_detail_views.xml",
        "views/stock_production_lot.xml",
    ],
    "demo": [
        "demo/mro_type.xml",
        "demo/mro_action.xml",
    ],
}
