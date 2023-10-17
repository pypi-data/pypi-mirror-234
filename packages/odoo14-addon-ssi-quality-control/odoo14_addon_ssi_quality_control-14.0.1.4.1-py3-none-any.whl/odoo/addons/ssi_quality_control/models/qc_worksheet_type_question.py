# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class QCWorksheetTypeQuestion(models.Model):
    _name = "qc_worksheet_type.question"
    _description = "QC Worksheet Type - Question"
    _order = "type_id, sequence"

    type_id = fields.Many2one(
        string="QC Worksheet Type",
        comodel_name="qc_worksheet_type",
        required=True,
        ondelete="cascade",
    )
    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=5,
    )
    name = fields.Char(
        string="Question",
        required=True,
    )
    type = fields.Selection(
        string="Type",
        selection=[
            ("qualitative", "Qualitative"),
            ("quantitative", "Quantitative"),
        ],
        required=True,
    )
    value_set_id = fields.Many2one(
        string="Value Set",
        comodel_name="qc_value_set",
    )
    min_value = fields.Float(
        string="Min. Value",
    )
    max_value = fields.Float(
        string="Max. Value",
    )
    uom_id = fields.Many2one(
        string="UoM",
        comodel_name="uom.uom",
    )
    notes = fields.Text(
        string="Notes",
    )

    def _create_worksheet_question(self, worksheet):
        self.ensure_one()
        self.env["qc_worksheet.question"].create(
            {
                "worksheet_id": worksheet.id,
                "sequence": self.sequence,
                "name": self.name,
                "type": self.type,
                "uom_id": self.uom_id and self.uom_id.id or False,
                "set_id": self.value_set_id and self.value_set_id.id or False,
            }
        )
