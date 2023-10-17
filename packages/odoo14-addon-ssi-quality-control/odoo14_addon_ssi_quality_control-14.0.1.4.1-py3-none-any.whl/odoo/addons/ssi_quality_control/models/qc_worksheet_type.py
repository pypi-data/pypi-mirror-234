# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class QCWorksheetType(models.Model):
    _name = "qc_worksheet_type"
    _inherit = ["mixin.master_data"]
    _description = "QC Worksheet Type"

    model_id = fields.Many2one(
        string="Model",
        comodel_name="ir.model",
        required=False,
        ondelete="set null",
    )
    question_ids = fields.One2many(
        string="Questions",
        comodel_name="qc_worksheet_type.question",
        inverse_name="type_id",
    )
