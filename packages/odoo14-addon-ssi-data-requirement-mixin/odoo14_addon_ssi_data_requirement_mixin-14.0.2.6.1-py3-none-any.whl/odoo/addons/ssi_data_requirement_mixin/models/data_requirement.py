# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class DataRequirement(models.Model):
    _name = "data_requirement"
    _inherit = [
        "mixin.transaction_open",
        "mixin.transaction_confirm",
        "mixin.transaction_done",
        "mixin.transaction_cancel",
        "mixin.localdict",
        "mixin.partner",
    ]
    _description = "Data Requirement"

    # Multiple Approval Attribute
    _approval_from_state = "open"
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

    _statusbar_visible_label = "draft,open,confirm,done"
    _policy_field_order = [
        "open_ok",
        "confirm_ok",
        "approve_ok",
        "reject_ok",
        "restart_approval_ok",
        "cancel_ok",
        "restart_ok",
        "manual_number_ok",
    ]
    _header_button_order = [
        "action_open",
        "action_confirm",
        "action_approve_approval",
        "action_reject_approval",
        "%(ssi_transaction_cancel_mixin.base_select_cancel_reason_action)d",
        "action_restart",
    ]

    # Attributes related to add element on search view automatically
    _state_filter_order = [
        "dom_draft",
        "dom_open",
        "dom_confirm",
        "dom_reject",
        "dom_done",
        "dom_cancel",
    ]

    # Sequence attribute
    _create_sequence_state = "open"

    package_id = fields.Many2one(
        string="# Data Requirement Package",
        comodel_name="data_requirement_package",
        readonly=True,
        ondelete="restrict",
    )
    date = fields.Date(
        string="Date",
        required=True,
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
    date_submit = fields.Date(
        string="Submit Date",
        required=False,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    type_id = fields.Many2one(
        string="Type",
        comodel_name="data_requirement_type",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    title = fields.Char(
        string="Title",
        default="-",
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    category_id = fields.Many2one(
        string="Category",
        related="type_id.category_id",
        store=True,
    )
    mode = fields.Selection(
        string="Mode",
        selection=[
            ("url", "URL"),
            ("attachment", "Attachment"),
        ],
        required=True,
        readonly=True,
        default="url",
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    url = fields.Char(
        string="URL",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    attachment_id = fields.Many2one(
        string="Attachment",
        comodel_name="ir.attachment",
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
            ("open", "In Progress"),
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
        res = super(DataRequirement, self)._get_policy_field()
        policy_field = [
            "open_ok",
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
