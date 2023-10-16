# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class DataRequirementConfigurator(models.Model):
    _name = "data_requirement_configurator"
    _description = "Data Requirement Configurator"

    model_id = fields.Many2one(
        string="Document Type",
        comodel_name="ir.model",
        index=True,
        readonly=False,
        default=lambda self: self._default_model_id(),
    )
    model_name = fields.Char(
        related="model_id.model",
        index=True,
        store=True,
        readonly=False,
    )
    object_id = fields.Many2oneReference(
        string="Document ID",
        index=True,
        required=True,
        readonly=False,
        model_field="model_name",
    )
    type_id = fields.Many2one(
        string="Data Requirement Type",
        comodel_name="data_requirement_type",
        required=True,
    )
    title = fields.Char(
        string="Title",
    )

    @api.model
    def _default_model_id(self):
        model = False
        obj_ir_model = self.env["ir.model"]
        model_name = self.env.context.get("model", False)
        if model_name:
            criteria = [("model", "=", model_name)]
            model = obj_ir_model.search(criteria)
        return model
