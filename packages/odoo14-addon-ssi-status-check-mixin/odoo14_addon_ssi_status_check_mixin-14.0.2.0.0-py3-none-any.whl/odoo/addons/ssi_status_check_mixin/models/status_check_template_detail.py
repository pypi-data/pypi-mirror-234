# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0-standalone.html).

from odoo import api, fields, models


class StatusCheckTemplateDetail(models.Model):
    _name = "status.check.template_detail"
    _description = "Status Check Template Detail"
    _order = "sequence, id"

    template_id = fields.Many2one(
        string="Status Check Template",
        comodel_name="status.check.template",
        ondelete="cascade",
    )
    company_id = fields.Many2one(
        related="template_id.company_id",
        store=True,
    )
    sequence = fields.Integer(
        default=5,
        required=True,
    )

    def _prepare_criteria_without_model(self):
        self.ensure_one()
        criteria = [("model", "=", False)]
        return criteria

    def _prepare_criteria_with_model(self):
        self.ensure_one()
        criteria = [("model", "=", self.template_id.model)]
        return criteria

    @api.depends(
        "template_id",
        "template_id.model_id",
    )
    def _compute_allowed_status_check_item_ids(self):
        obj_status_check_item = self.env["status.check.item"]

        for document in self:
            result = []
            without_model_ids = []
            with_model = []
            criteria_without_model = document._prepare_criteria_without_model()
            without_model_ids = obj_status_check_item.search(criteria_without_model)
            if without_model_ids:
                result += without_model_ids.ids
            criteria_with_model = document._prepare_criteria_with_model()
            with_model = obj_status_check_item.search(criteria_with_model)
            if with_model:
                result += with_model.ids
            document.allowed_status_check_item_ids = result

    allowed_status_check_item_ids = fields.Many2many(
        string="Allowed Status Check Item",
        comodel_name="status.check.item",
        compute="_compute_allowed_status_check_item_ids",
        store=False,
    )

    status_check_item_id = fields.Many2one(
        string="Status Check Item",
        comodel_name="status.check.item",
        ondelete="restrict",
        required=True,
    )
    active = fields.Boolean(
        default=True,
    )
