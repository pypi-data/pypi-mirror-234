# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class DataRequirementPackageDetail(models.Model):
    _name = "data_requirement_package.detail"
    _description = "Data Requirement Package Detail"
    _order = "package_id, sequence"

    package_id = fields.Many2one(
        string="# Package",
        comodel_name="data_requirement_package",
        required=True,
        ondelete="cascade",
    )
    sequence = fields.Integer(
        string="Sequence",
        default=10,
        required=True,
    )
    type_id = fields.Many2one(
        string="Data Requirement Type",
        comodel_name="data_requirement_type",
        required=True,
        ondelete="restrict",
    )
    data_id = fields.Many2one(
        string="# Data",
        comodel_name="data_requirement",
        readonly=True,
        ondelete="cascade",
    )

    def _create_data_requirement(self):
        self.ensure_one()
        data = self.env["data_requirement"].create(
            self._prepare_create_data_requirement()
        )
        self.write(
            {
                "data_id": data.id,
            }
        )

    def _prepare_create_data_requirement(self):
        self.ensure_one()
        package = self.package_id
        return {
            "package_id": package.id,
            "partner_id": package.partner_id.id,
            "contact_partner_id": package.contact_partner_id.id,
            "type_id": self.type_id.id,
            "mode": self.type_id.mode,
            "date": package.date,
            "duration_id": package.duration_id and package.duration_id.id or False,
            "date_commitment": package.date_commitment,
        }

    def _cleanup_data_requirement(self):
        self.ensure_one()
        data = self.data_id
        self.write(
            {
                "data_id": False,
            }
        )
        data.unlink()
