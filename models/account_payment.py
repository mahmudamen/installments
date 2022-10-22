from odoo import fields, models, api


class AccountPayment(models.Model):
    _inherit = "account.payment"

    installment_id = fields.Many2one(comodel_name='installment.installment')