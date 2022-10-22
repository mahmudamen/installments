from odoo import fields, models, api


class accountmove(models.Model):
    _inherit = 'account.move'
    _description = 'Description'

    install_id = fields.Many2one(comodel_name='installment.installment')
