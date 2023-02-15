from datetime import date

from odoo import fields, models, api, _


class CotacaoBI(models.Model):
    _name = 'cotacao.b.i'

    # DADOS DE CLIENTE
    partner_id = fields.Many2one(comodel_name='res.partner', string='Cliente')
    partner_phone = fields.Char(related="partner_id.phone", string='Telefone')
    partner_route_id = fields.Many2one(related="partner_id.route_id", string='Rota')
    partner_street = fields.Char(related="partner_id.street", string='Rua')
    partner_city = fields.Char(related="partner_id.city", string='Cidade')
    partner_email = fields.Char(related="partner_id.email", string='E-mail')
    partner_fantasy_name = fields.Char(related="partner_id.name_fantasy", string='Nome fantasia')
    date = fields.Date(string='Data de Emissão', default=date.today(), readonly=True)
    expire_date = fields.Date(string='Data de Vencimento', default=date.today())
    payment_conditions = fields.Many2one(comodel_name='account.payment.term')

    # LISTA DE COTAÇÃO
    quote_list = fields.One2many(
        comodel_name='cotacao.b.i.list',
        inverse_name='cotacao_id',
    )

    # CAMPO QUE ARMAZENA O PRE PEDIDO CRIADO PELA COTACAO
    pre_order_id = fields.Many2one(
        comodel_name='sale.order',
        string='Pré-pedido criado',
        readonly=True
    )

    # LISTA QUE MOSTRA AS COTAÇÕES ANTERIORES DESSE MESMO CLIENTE
    previous_quotations = fields.Many2many(
        comodel_name='cotacao.b.i',
        relation="prev_quot_rel",
        column1="quotation_b_i",
        column2="previous_quotations",
        compute="fill_quotations"
    )

    # função que preenche o campo previous_quotations
    def fill_quotations(self):
        for rec in self:
            if rec.partner_id:
                quotations = self.env['cotacao.b.i'].search([('partner_id.id', '=', self.partner_id.id), ('id', '!=', rec.id)])
                rec.previous_quotations = quotations.ids

    # FUNCAO PARA ABRIR O PRE PEDIDO QUE FOI CRIADO PELA COTACAO
    def preorder(self):
        return {
            'type': "ir.actions.act_window",
            'view_type': "form",
            'view_mode': "form",
            'res_id': self.pre_order_id.id,
            'res_model': "sale.order",
            'views': [[self.env.ref("sale.view_order_form").id, 'form']],
            'target': 'current',
        }


class CotacaoBIList(models.Model):
    _name = 'cotacao.b.i.list'
    _rec_name = 'product_id'

    cotacao_id = fields.Many2one(comodel_name='cotacao.b.i')

    wish_qty = fields.Float()

    pre_wish_qty = fields.Float()

    product_id = fields.Many2one(comodel_name='product.product')

    stock_qty = fields.Float(related="product_id.virtual_available")

    product_brands = fields.Many2many(related='product_id.product_template_attribute_value_ids')

    product_price = fields.Float(related='product_id.lst_price')

    quoted_stock = fields.Boolean()

    will_quote = fields.Boolean()

    stk_ins = fields.Boolean(string="Estoque insuficiente?")