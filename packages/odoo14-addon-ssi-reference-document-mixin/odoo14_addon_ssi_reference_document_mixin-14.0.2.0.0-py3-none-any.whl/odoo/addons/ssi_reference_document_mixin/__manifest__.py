# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "Reference Document Mixin",
    "version": "14.0.2.0.0",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "ssi_master_data_mixin",
        "ssi_decorator",
    ],
    "data": [
        "security/ir.model.access.csv",
        "menu.xml",
        "templates/mixin_reference_document_templates.xml",
        "views/reference_document_category_views.xml",
        "views/reference_document_set_views.xml",
        "views/reference_document_views.xml",
    ],
    "demo": [
        "demo/reference_document_category_demos.xml",
        "demo/reference_document_demos.xml",
    ],
}
