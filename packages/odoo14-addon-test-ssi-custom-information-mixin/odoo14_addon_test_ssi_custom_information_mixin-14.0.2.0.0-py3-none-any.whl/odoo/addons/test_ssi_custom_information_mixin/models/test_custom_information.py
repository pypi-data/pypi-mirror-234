# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class TestCustomInformation(models.Model):
    _name = "test.custom_information"
    _description = "Test Custom Information"
    _inherit = [
        "mixin.custom_info",
    ]

    _custom_info_create_page = True

    name = fields.Char(
        string="# Document",
        default="/",
        required=True,
    )
    partner_id = fields.Many2one(
        string="Partner",
        comodel_name="res.partner",
    )
    date = fields.Date(
        string="Date",
        default=fields.Date.context_today,
    )
    notes = fields.Text(
        string="Notes",
    )
