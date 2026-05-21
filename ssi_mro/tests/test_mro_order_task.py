# Copyright 2025 OpenSynergy Indonesia
# Copyright 2025 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestMroOrderTask(YamlTransactionCase):
    def test_mro_order_task(self):
        self.run_yaml_scenario("test_data_mro_order_task.yaml")
