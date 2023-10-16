# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class CrmLead(models.Model):
    _name = "crm.lead"
    _inherit = [
        "crm.lead",
    ]

    quotation_ids = fields.One2many(
        string="Quotations",
        comodel_name="service.quotation",
        inverse_name="lead_id",
        readonly=True,
    )
    service_currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        default=lambda self: self._default_service_currency_id(),
    )
    service_estimated_revenue = fields.Monetary(
        string="Service Estimated Revenue",
        currency_field="service_currency_id",
        compute="_compute_service_estimated_revenue",
        store=True,
    )

    @api.model
    def _default_service_currency_id(self):
        return self.env.user.company_id.currency_id

    @api.depends(
        "quotation_ids",
        "quotation_ids.amount_untaxed",
        "quotation_ids.state",
    )
    def _compute_service_estimated_revenue(self):
        for record in self:
            result = 0.0
            for quotation in record.quotation_ids.filtered(
                lambda r: r.state not in ["cancel", "lost"]
                and r.currency_id.id == record.service_currency_id.id
            ):
                result += quotation.amount_untaxed
            record.service_estimated_revenue = result
