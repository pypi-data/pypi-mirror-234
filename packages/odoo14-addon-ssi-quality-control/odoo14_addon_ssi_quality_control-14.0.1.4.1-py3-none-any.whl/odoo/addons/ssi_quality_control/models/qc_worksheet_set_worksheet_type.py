# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class QCWorksheetSetWorksheetType(models.Model):
    _name = "qc_worksheet_set.worksheet_type"
    _description = "QC Worksheet Set - Worksheet Type"

    set_id = fields.Many2one(
        string="Set",
        comodel_name="qc_worksheet_set",
        required=True,
        ondelete="cascade",
    )
    type_id = fields.Many2one(
        string="Worksheet Type",
        comodel_name="qc_worksheet_type",
        required=True,
        ondelete="restrict",
    )

    def _create_worksheet(self, qc_record):
        self.ensure_one()
        self.env["qc_worksheet"].create(self._prepare_create_worksheet(qc_record))

    def _prepare_create_worksheet(self, qc_record):
        self.ensure_one()
        criteria = [("model", "=", qc_record._name)]
        model = self.env["ir.model"].search(criteria)
        return {
            "model_id": model.id,
            "object_id": qc_record.id,
            "date": fields.Date.today(),
            "type_id": self.type_id.id,
        }
