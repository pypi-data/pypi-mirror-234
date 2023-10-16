# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class DataRequirementPackageTypeDetail(models.Model):
    _name = "data_requirement_package_type.detail"
    _description = "Data Requirement Package Type - Detail"
    _order = "type_id, sequence"

    type_id = fields.Many2one(
        string="Data Requirement Package Type",
        comodel_name="data_requirement_package_type",
        required=True,
        ondelete="cascade",
    )
    sequence = fields.Integer(
        string="Sequence",
        default=10,
        required=True,
    )
    data_type_id = fields.Many2one(
        string="Data Requirement Type",
        comodel_name="data_requirement_type",
        required=True,
        ondelete="restrict",
    )

    def _create_package_detail(self, data_package):
        self.env["data_requirement_package.detail"].create(
            self._prepare_create_package_detail(data_package)
        )

    def _prepare_create_package_detail(self, data_package):
        self.ensure_one()
        return {
            "package_id": data_package.id,
            "type_id": self.data_type_id.id,
        }
