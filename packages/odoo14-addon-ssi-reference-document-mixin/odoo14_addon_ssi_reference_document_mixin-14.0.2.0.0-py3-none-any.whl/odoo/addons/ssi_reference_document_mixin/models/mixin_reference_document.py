# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import api, fields, models

from odoo.addons.ssi_decorator import ssi_decorator


class MixinReferenceDocument(models.AbstractModel):
    _name = "mixin.reference_document"
    _inherit = [
        "mixin.decorator",
    ]
    _description = "Reference Document Mixin"
    _reference_document_create_page = False
    _reference_document_page_xpath = "//page[last()]"
    _configurator_field_name = "type_id"
    _reference_document_set_field_name = "reference_document_set_ids"

    reference_document_set_ids = fields.Many2many(
        string="Reference Document Sets",
        comodel_name="reference_document_set",
    )
    reference_document_ids = fields.Many2many(
        string="Reference Document",
        comodel_name="reference_document",
        compute="_compute_reference_document_ids",
        store=False,
        compute_sudo=True,
    )

    @api.depends(
        "reference_document_set_ids",
    )
    def _compute_reference_document_ids(self):
        for record in self.sudo():
            result = self.env["reference_document"]
            for document_set in record.reference_document_set_ids:
                result += document_set.reference_document_ids
            record.reference_document_ids = result

    @ssi_decorator.insert_on_form_view()
    def _reference_document_insert_form_element(self, view_arch):
        if self._reference_document_create_page:
            view_arch = self._add_view_element(
                view_arch=view_arch,
                qweb_template_xml_id="ssi_reference_document_mixin.reference_document",
                xpath=self._reference_document_page_xpath,
                position="after",
            )
        return view_arch
