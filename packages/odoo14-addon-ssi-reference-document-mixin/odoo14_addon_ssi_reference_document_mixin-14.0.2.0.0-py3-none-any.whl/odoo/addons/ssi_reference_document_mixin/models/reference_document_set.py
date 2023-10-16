# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ReferenceDocumentSet(models.Model):
    _name = "reference_document_set"
    _description = "Reference Document Set"
    _inherit = ["mixin.master_data"]

    reference_document_ids = fields.Many2many(
        string="Reference Documents",
        comodel_name="reference_document",
        relation="rel_reference_document_set_2_document",
        column1="set_id",
        column2="document_id",
    )
