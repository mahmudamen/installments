# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime
from odoo.exceptions import ValidationError, UserError, RedirectWarning

class installments(models.Model):
    _name = 'installment.installment'
    _rec_name = 'name'
    _description = 'installment.installment'

    name = fields.Char(string='Name', readonly=True)
    reference = fields.Char(string='Reference')
    state = fields.Selection([('draft', 'draft'),
                              ('open', 'open'),
                              ('paid', 'paid')],
                             string="State",default='draft',stored=True)
    date = fields.Date(string='Date', default=datetime.today())
    customer = fields.Many2one('res.partner', string='Customer', required=True)
    journal = fields.Many2one('account.journal', string='Journal', required=True)
    account = fields.Many2one('account.account', string='Account', required=True)
    analytic_account = fields.Many2one(comodel_name="account.analytic.account", string="Analytic Account")
    analytic_tag = fields.Many2many("account.analytic.tag", string="Analytic Tags")
    amount = fields.Float(string='Amount', required=True)
    notes = fields.Text(string='Notes')
    payment_ids = fields.One2many('account.payment','installment_id',store=True,compute='_payment')
    move_ids = fields.One2many('account.move', 'install_id', store=True)
    inv_count = fields.Integer(compute='inv_compute_count')

    _sql_constraints = [
            ('check_amount','CHECK(amount > 0)'," Amount Must be positive")
    ]

    @api.depends('payment_ids')
    def _payment(self):
        if self.state == 'open':
            total_payment = 0
            for i in self.payment_ids:
                total_payment += i.amount

            if self.amount == total_payment:
                self.state = 'paid'

    def open(self):
        if self.state == 'draft':
            for record in self:
                self.env['account.move'].create([
                    {
                        'move_type': 'out_invoice',
                        'invoice_date': record.date,
                        'partner_id': record.customer.id,
                        'amount_total': record.amount,
                        'install_id': record.id,
                    },
                ])
            self.state = 'open'
            self.name = self.env['ir.sequence'].next_by_code('installments_inv_seq')


    def payment(self):
        return {
            'name': 'payment',
            'view_mode': 'form',
            'res_model': 'account.payment',
            'domain': [],
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': {
                'default_amount': self.amount,
                'default_installment_id':self.id,
                'default_partner_id':self.customer.id,
                'default_journal_id':self.journal.id,
            },
        }




    def settlement(self):
        raise ValidationError(_("Settles the installment with the remaining amount and then set the State to paid"))


    def inv_compute_count(self):
        for record in self:
            record.inv_count = self.env['account.move'].search_count(
                [('install_id', '=', self.id)])

    def get_inv(self):
        return {
            'name': _('invoice'),
            'view_type':'form',
            'res_model':'account.move',
            'view_id':False,
            'view_mode':'tree,form',
            'type':'ir.actions.act_window',
            'domain': [('install_id', '=', self.id)],
            'context': {'default_install_id': self.id},

        }