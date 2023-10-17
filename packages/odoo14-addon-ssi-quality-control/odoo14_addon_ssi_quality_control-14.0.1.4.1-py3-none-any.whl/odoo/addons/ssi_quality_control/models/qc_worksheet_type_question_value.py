# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class QCWorksheetTypeQuestionValue(models.Model):
    _name = "qc_worksheet_type.question.value"
    _description = "QC Worksheet Type - Question - Value"
    _order = "question_id, sequence"

    question_id = fields.Many2one(
        string="QC Worksheet Type - Question",
        comodel_name="qc_worksheet_type.question",
        required=True,
        ondelete="cascade",
    )
    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=5,
    )
    name = fields.Char(
        string="Value",
        required=True,
    )
    active = fields.Boolean(
        string="Active",
        default=True,
    )
    ok = fields.Boolean(
        string="Correct Answer",
    )
    description = fields.Text(
        string="Description",
    )
