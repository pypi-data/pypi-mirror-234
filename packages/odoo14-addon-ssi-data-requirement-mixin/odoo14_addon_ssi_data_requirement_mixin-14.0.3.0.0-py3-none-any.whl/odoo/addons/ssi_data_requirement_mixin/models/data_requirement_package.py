# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class DataRequirementPackage(models.Model):
    _name = "data_requirement_package"
    _inherit = [
        "mixin.transaction_confirm",
        "mixin.transaction_done",
        "mixin.transaction_cancel",
        "mixin.partner",
    ]
    _description = "Data Requirement Package"

    # Multiple Approval Attribute
    _approval_from_state = "draft"
    _approval_to_state = "done"
    _approval_state = "confirm"
    _after_approved_method = "action_done"

    # Attributes related to add element on view automatically
    _automatically_insert_view_element = True

    # Attributes related to add element on form view automatically
    _automatically_insert_multiple_approval_page = True
    _automatically_insert_done_policy_fields = False
    _automatically_insert_done_button = False

    # mixin.partner configuration
    _mixin_partner_insert_form = True
    _mixin_partner_insert_tree = True
    _mixin_partner_insert_search = True
    _mixin_partner_contact_id_required = True

    _statusbar_visible_label = "draft,confirm,done"
    _policy_field_order = [
        "confirm_ok",
        "approve_ok",
        "reject_ok",
        "restart_approval_ok",
        "cancel_ok",
        "restart_ok",
        "manual_number_ok",
    ]
    _header_button_order = [
        "action_confirm",
        "action_approve_approval",
        "action_reject_approval",
        "%(ssi_transaction_cancel_mixin.base_select_cancel_reason_action)d",
        "action_restart",
    ]

    # Attributes related to add element on search view automatically
    _state_filter_order = [
        "dom_draft",
        "dom_confirm",
        "dom_reject",
        "dom_done",
        "dom_cancel",
    ]

    # Sequence attribute
    _create_sequence_state = "done"

    type_id = fields.Many2one(
        string="Type",
        comodel_name="data_requirement_package_type",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    date = fields.Date(
        string="Date",
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    title = fields.Char(
        string="Title",
        default="-",
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    upload_url = fields.Char(
        string="Upload URL",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    duration_id = fields.Many2one(
        string="Duration",
        comodel_name="base.duration",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    date_commitment = fields.Date(
        string="Commitment Date",
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    data_requirement_ids = fields.One2many(
        string="Data Requirements",
        comodel_name="data_requirement",
        inverse_name="package_id",
    )
    data_requirement_status = fields.Selection(
        string="Data Requirement Status",
        selection=[
            ("not_needed", "Not Needed"),
            ("open", "In Progress"),
            ("done", "Done"),
        ],
        compute="_compute_data_requirement_status",
        store=True,
    )
    detail_ids = fields.One2many(
        string="Detail",
        comodel_name="data_requirement_package.detail",
        inverse_name="package_id",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Draft"),
            ("confirm", "Waiting for Approval"),
            ("done", "Done"),
            ("cancel", "Cancelled"),
            ("reject", "Rejected"),
        ],
        default="draft",
        copy=False,
    )

    @api.model
    def _get_policy_field(self):
        res = super(DataRequirementPackage, self)._get_policy_field()
        policy_field = [
            "confirm_ok",
            "approve_ok",
            "cancel_ok",
            "reject_ok",
            "restart_ok",
            "restart_approval_ok",
            "manual_number_ok",
        ]
        res += policy_field
        return res

    @api.depends(
        "data_requirement_ids",
        "data_requirement_ids.state",
    )
    def _compute_data_requirement_status(self):
        for record in self:
            result = "not_needed"
            num_of_data_requirement = len(record.data_requirement_ids)
            num_of_done_data_requirement = len(
                record.data_requirement_ids.filtered(lambda r: r.state == "done")
            )

            if (
                num_of_data_requirement != 0
                and num_of_data_requirement != num_of_done_data_requirement
            ):
                result = "open"
            elif (
                num_of_data_requirement != 0
                and num_of_data_requirement == num_of_done_data_requirement
            ):
                result = "done"

            record.data_requirement_status = result

    @api.onchange(
        "duration_id",
        "date",
    )
    def onchange_date_commitment(self):
        self.date_commitment = False
        if self.duration_id:
            self.date_commitment = self.duration_id.get_duration(self.date)

    @api.onchange(
        "type_id",
    )
    def onchange_title(self):
        self.title = False
        if self.type_id:
            self.title = self.type_id.name

    def action_reload_detail(self):
        for record in self.sudo():
            record._reload_detail()

    def action_create_data_requirement(self):
        for record in self.sudo():
            record._create_data_requirement()

    def _reload_detail(self):
        self.ensure_one()
        self._cleanup_data_requirement()
        self.detail_ids.unlink()

        if not self.type_id.detail_ids:
            return True

        for detail in self.type_id.detail_ids:
            detail._create_package_detail(self)

    def _create_data_requirement(self):
        self.ensure_one()
        for detail in self.detail_ids.filtered(lambda r: not r.data_id):
            detail._create_data_requirement()

    def _cleanup_data_requirement(self):
        self.ensure_one()
        for detail in self.detail_ids:
            detail._cleanup_data_requirement()
