# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "Data Requirement Mixin",
    "version": "14.0.2.6.1",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "application": True,
    "depends": [
        "base",
        "ssi_master_data_mixin",
        "ssi_transaction_open_mixin",
        "ssi_transaction_confirm_mixin",
        "ssi_transaction_done_mixin",
        "ssi_transaction_cancel_mixin",
        "ssi_localdict_mixin",
        "ssi_partner_mixin",
        "base_duration",
    ],
    "data": [
        "security/ir_module_category_data.xml",
        "security/res_group_data.xml",
        "security/ir.model.access.csv",
        "security/ir_rule_data.xml",
        "data/ir_sequence_data.xml",
        "data/sequence_template_data.xml",
        "data/approval_template_data.xml",
        "data/policy_template_data.xml",
        "menu.xml",
        "templates/mixin_data_requirement_templates.xml",
        "views/data_requirement_type_category_views.xml",
        "views/data_requirement_type_views.xml",
        "views/data_requirement_package_type_views.xml",
        "views/data_requirement_views.xml",
        "views/data_requirement_package_views.xml",
    ],
}
