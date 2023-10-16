# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ReferenceDocument(models.Model):
    _name = "reference_document"
    _description = "Reference Document"
    _inherit = ["mixin.master_data"]
    _order = "category_id, sequence"

    sequence = fields.Integer(
        string="Sequence",
        default=10,
        required=True,
    )
    category_id = fields.Many2one(
        string="Category",
        comodel_name="reference_document_category",
        required=True,
    )
    url = fields.Char(
        string="URL",
        required=True,
    )
