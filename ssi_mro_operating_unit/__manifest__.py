# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "MRO + Operating Unit",
    "version": "14.0.1.0.0",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "contributors": [
        "Andhitia Rama <andhitia.r@gmail.com>",
    ],
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "ssi_mro",
        "ssi_operating_unit_mixin",
    ],
    "data": [
        "security/res_group/mro_order.xml",
        "security/res_group/mro_order_task.xml",
        "security/ir_rule/mro_order.xml",
        "security/ir_rule/mro_order_task.xml",
        "view/mro_order.xml",
        "view/mro_order_task.xml",
    ],
}
