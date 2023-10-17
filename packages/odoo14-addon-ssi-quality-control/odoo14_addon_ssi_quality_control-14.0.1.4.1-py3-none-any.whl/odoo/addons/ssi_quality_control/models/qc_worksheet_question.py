# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class QCWorksheetQuestion(models.Model):
    _name = "qc_worksheet.question"
    _description = "QC Worksheet - Question"
    _order = "worksheet_id, sequence"

    worksheet_id = fields.Many2one(
        string="QC Worksheet",
        comodel_name="qc_worksheet",
        required=True,
        ondelete="cascade",
    )
    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=5,
        readonly=True,
    )
    name = fields.Char(
        string="Question",
        required=True,
        readonly=True,
    )
    type = fields.Selection(
        string="Type",
        selection=[
            ("qualitative", "Qualitative"),
            ("quantitative", "Quantitative"),
        ],
        required=True,
    )
    set_id = fields.Many2one(
        string="Value Set",
        comodel_name="qc_value_set",
        readonly=True,
    )
    allowed_qc_value_ids = fields.Many2many(
        string="Allowed QC Value",
        comodel_name="qc_value_item",
        compute="_compute_allowed_qc_value_ids",
        store=False,
    )
    qualitative_value_id = fields.Many2one(
        string="Qualitative Value",
        comodel_name="qc_value_item",
    )
    quantitative_value = fields.Float(
        string="Quantitative Value",
    )
    min_value = fields.Float(
        string="Min. Value",
    )
    max_value = fields.Float(
        string="Max. Value",
    )
    uom_id = fields.Many2one(
        string="UoM",
        comodel_name="product.uom",
        readonly=True,
    )
    valid_values = fields.Char(
        string="Valid Values",
        compute="_compute_valid_values",
        store=True,
    )
    success = fields.Boolean(
        string="Success?",
        compute="_compute_result",
        store=True,
    )

    @api.depends(
        "set_id",
    )
    def _compute_allowed_qc_value_ids(self):
        for record in self:
            result = self.env["qc_value_item"]
            if record.set_id:
                for item in record.set_id.value_ids:
                    result += item.item_id
            record.allowed_qc_value_ids = result

    @api.depends(
        "allowed_qc_value_ids",
        "min_value",
        "max_value",
        "type",
        "set_id",
    )
    def _compute_valid_values(self):
        for record in self:
            if record.type == "qualitative":
                criteria = [
                    ("set_id", "=", record.set_id.id),
                    ("item_id", "=", record.qualitative_value_id.id),
                    ("ok", "=", True),
                ]
                values = self.env["qc_value_set.value"].search(criteria)
                record.valid_values = ", ".join([x.name for x in values])
            elif record.type == "quantitative":
                record.valid_values = "{}-{}".format(record.min_value, record.max_value)

    @api.depends(
        "type",
        "max_value",
        "min_value",
        "quantitative_value",
        "qualitative_value_id",
        "allowed_qc_value_ids",
        "set_id",
    )
    def _compute_result(self):
        for record in self:
            if record.type == "qualitative":
                criteria = [
                    ("set_id", "=", record.set_id.id),
                    ("item_id", "=", record.qualitative_value_id.id),
                ]
                values = self.env["qc_value_set.value"].search(criteria)
                if len(values) > 0:
                    record.success = values[0].ok
            else:
                record.success = (
                    record.max_value >= record.quantitative_value >= record.min_value
                )
