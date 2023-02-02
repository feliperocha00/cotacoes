from odoo import fields, models, _, api


class ProductSearch(models.TransientModel):
    _name = 'product.search'

    # SELEÇÃO DO PRODUTO PRINCIPAL
    product_id = fields.Many2one(
        comodel_name='product.product',
        string='Produto'
    )

    # PASSAGEM DAS INFORMAÇÕES DE CLIENTE
    partner_id = fields.Many2one(comodel_name='res.partner')
    expire_date = fields.Date()
    payment_conditions = fields.Many2one(comodel_name='account.payment.term')

    # PASSAGEM DA LISTA DE COTACAO PELOS WIZARDS
    quote_list = fields.Many2many(
        comodel_name="product.product",
        relation="product_search_product_rel",
    )

    # QUANTIDADE DESEJADA
    wish_qty = fields.Float(
        string='Quantidade desejada',
        default=1
    )

    def showproduct(self):
        quotelist = []

        for quote in self.quote_list.ids:
            quotelist.append(quote)

        ctx = dict()
        ctx.update({
            'default_partner_id': self.partner_id.id,
            'default_expire_date': self.expire_date,
            'default_payment_conditions': self.payment_conditions.id,
            'default_wish_qty': self.wish_qty,
            'default_quote_list': quotelist,
            'default_product_id': self.product_id.id,
        })
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'quoted.product',
            'views': [[self.env.ref("cotacoes.quoted_product_form").id, 'form']],
            'context': ctx,
            'target': 'new'
        }

    def throwback(self):
        quotelist = []

        for quote in self.quote_list.ids:
            quotelist.append(quote)

        ctx = dict()
        ctx.update({
            'default_partner_id': self.partner_id.id,
            'default_expire_date': self.expire_date,
            'default_payment_conditions': self.payment_conditions.id,
            'default_quote_list': quotelist
        })
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'cotacoes',
            'views': [[self.env.ref("cotacoes.cotacoes_form_view").id,'form']],
            'context': ctx,
            'target': 'new'
        }
