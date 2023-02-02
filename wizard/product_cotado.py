from odoo import models, fields, api, _


class ProductCotado(models.TransientModel):
    _name = 'quoted.product'

    # CAMPOS PRODUTO PRINCIPAL
    product_id = fields.Many2one(comodel_name='product.product')
    product_brand_ids = fields.Many2many(related='product_id.product_template_attribute_value_ids')
    product_fipe_ids = fields.Many2many(related='product_id.fipe_ids')
    product_qty = fields.Float(related='product_id.qty_available')
    product_type = fields.Selection(related='product_id.type')
    product_price = fields.Float(related='product_id.lst_price')
    product_image = fields.Binary(related='product_id.image_1920')
    product_barcode = fields.Char(related='product_id.barcode')
    product_accessories = fields.Many2many(related='product_id.accessory_product_ids',string='Acessórios')

    # INFORMAÇÕES DE CLIENTE
    partner_id = fields.Many2one(comodel_name='res.partner', string='Cliente')
    expire_date = fields.Date(string='Data de Vencimento')
    payment_conditions = fields.Many2one(comodel_name='account.payment.term')

    # PASSAGEM DA LISTA DE COTACAO PELOS WIZARDS
    quote_list = fields.Many2many(
        comodel_name="product.product",
        relation="cotacao_prod_rel",
    )

    # QUANTIDADE DESEJADA
    wish_qty = fields.Float(
        string='Quantidade desejada',
    )

    def showproductinformation(self):
        quotelist = []

        for quote in self.quote_list.ids:
            quotelist.append(quote)

        quotelist.append(self.product_id.id)

        ctx = dict()
        ctx.update({
            'default_partner_id': self.partner_id.id,
            'default_expire_date': self.expire_date,
            'default_payment_conditions': self.payment_conditions.id,
            'default_product_id': self.product_id.id,
            'default_wish_qty': self.wish_qty,
            'default_quote_list': quotelist
        })
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'quoted.product.info',
            'views': [[self.env.ref("cotacoes.product_info_form_view").id, 'form']],
            'context': ctx,
            'target': 'new'
        }

    def cancela(self):
        ctx = dict()
        ctx.update({
            'default_partner_id': self.partner_id.id,
            'default_expire_date': self.expire_date,
            'default_payment_conditions': self.payment_conditions.id,
            'default_quote_list': self.quote_list.ids
        })
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'product.search',
            'views': [[self.env.ref("cotacoes.pesquisa_de_produto_form_view").id,'form']],
            'context': ctx,
            'target': 'new'
        }