# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class QCWorksheetSet(models.Model):
    _name = "qc_worksheet_set"
    _inherit = ["mixin.master_data"]
    _description = "QC Worksheet Set"

    model_id = fields.Many2one(
        string="Model",
        comodel_name="ir.model",
        required=False,
        ondelete="set null",
    )
    type_ids = fields.One2many(
        string="Types",
        comodel_name="qc_worksheet_set.worksheet_type",
        inverse_name="set_id",
    )
