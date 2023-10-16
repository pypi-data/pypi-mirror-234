# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ReferenceDocumentCategory(models.Model):
    _name = "reference_document_category"
    _description = "Reference Document Category"
    _inherit = ["mixin.master_data"]
    _order = "sequence"

    sequence = fields.Integer(
        string="Sequence",
        default=10,
        required=True,
    )
