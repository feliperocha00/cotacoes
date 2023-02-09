from datetime import date

from odoo import fields, models, api, _


class ProductData(models.TransientModel):
    _name = 'quoted.product.info'

    # PRODUTO PRINCIPAL
    product_id = fields.Many2one(
        comodel_name='product.product'
    )

    # QUANTIDADE EM ESTOQUE DO PRODUTO PRINCIPAL
    product_qty = fields.Float(
        related='product_id.virtual_available',
        string='Quant. em estoque'
    )

    # QUANTIDADE DESEJADA
    wish_qty = fields.Float(
        string='Quantidade desejada',
        readonly=True
    )

    # QUANTIDADE DESEJADA CASO SEM ESTOQUE SUF.
    wish_sec_qty = fields.Float(
        string='Nova quantidade desejada'
    )

    # IMAGEM DO PRODUTO PRINCIPAL
    product_image = fields.Binary(
        related='product_id.image_1920'
    )

    # PREÇO DO PRODUTO PRINCIPAL
    product_price = fields.Float(
        related='product_id.lst_price',
        string='Preço'
    )

    # ACESSÓRIOS DO PRODUTO PRINCIPAL
    accessories_ids = fields.Many2many(
        comodel_name='product.product',
        relation='product_info_acessories_product_rel',
        string='Acessórios',
        domain="[('id','in',product_accessories_ids),('virtual_available','>',0)]"
    )

    # SELEÇÃO DO PRODUTO VARIANTE
    variant_ids = fields.Many2many(
        comodel_name='product.product',
        relation='product_info_variant_product_rel',
        string='Produtos Variante',
        domain="[('product_tmpl_id','=',product_template_id),('id','!=',product_id),('virtual_available','>',0)]"
    )

    # SELEÇÃO DO ACESSÓRIO DO PRODUTO VARIANTE
    var_accessory_ids = fields.Many2many(
        comodel_name='product.product',
        relation='product_info_var_accessories_product_rel',
        string='Acessórios',
        domain="[('virtual_available','>',0)]"
    )

    # SELEÇÃO DO PRODUTO OPCIONAL
    optional_ids = fields.Many2many(
        comodel_name='product.product',
        relation='product_info_optional_product_rel',
        string='Produtos Opcionais',
        domain="[('product_tmpl_id','in',opt_product_ids),('virtual_available','>',0)]"
    )

    # SELEÇÃO DO ACESSÓRIO DO PRODUTO OPCIONAL
    opt_accessories_ids = fields.Many2many(
        comodel_name='product.product',
        relation='product_info_opt_accessories_search_rel',
        string='Acessórios',
        domain="[('virtual_available','>',0)]"
    )

    # RELACIONADO AOS PRODUTOS OPCIONAIS DO PRODUTO SELECIONADO
    #   USADO SOMENTE PARA DOMAIN
    opt_product_ids = fields.Many2many(
        related='product_id.optional_product_ids'
    )

    # RELACIONADO AOS ACESSÓRIOS DO PRODUTO SELECIONADO
    #   USADO SOMENTE PARA DOMAIN
    product_accessories_ids = fields.Many2many(
        related='product_id.accessory_product_ids'
    )

    # RELACIONADO AO TEMPLATE DO PRODUTO SELECIONADO
    #   USADO SOMENTE PARA DOMAIN
    product_template_id = fields.Many2one(
        related='product_id.product_tmpl_id'
    )

    # INFORMAÇÕES DE CLIENTE
    partner_id = fields.Many2one(comodel_name='res.partner', string='Cliente')
    expire_date = fields.Date(string='Data de Vencimento')
    payment_conditions = fields.Many2one(comodel_name='account.payment.term')

    # PASSAGEM DA LISTA DE COTACAO PELOS WIZARDS
    quote_list = fields.Many2many(
        comodel_name="product.product",
        relation="cotacao_info_prod_rel",
    )

    # SELEÇÃO OU CADASTRO DO CONCORRENTE
    concorrente = fields.Many2one(
        comodel_name='res.partner',
        string='Concorrente',
        domain="[('is_concorrente','=',True)]"
    )

    # INSERÇÃO DE VALOR DO PRODUTO NA CONCORRÊNCIA
    value = fields.Float(
        string='Valor na concorrência'
    )

    data = fields.Date(
        default=date.today()
    )

    precos_de_concorrente = fields.One2many(
        related='product_id.concorrente_prices',
        string='Preços de concorrente'
    )

    # Booleano de disponibilidade para usar no attrs
    is_unv = fields.Integer()

    @api.onchange('wish_qty')
    def isunv(self):
        if self.wish_qty:
            if self.wish_qty > self.product_qty:
                self.is_unv = 1
            else:
                self.is_unv = 0

    @api.onchange('product_qty')
    def wish_sec(self):
        if self.wish_qty > self.product_qty:
            self.wish_sec_qty = self.product_qty

    @api.onchange('product_id')
    def prod_accessories(self):
        accessory = []
        if self.product_id:
            if self.product_id.virtual_available > 0:
                for acess in self.product_accessories_ids.ids:
                    accessory.append(acess)
                self.accessories_ids = accessory

    @api.onchange('variant_ids')
    def var_accessories(self):
        accessory = []
        if self.variant_ids:
            for acess in self.variant_ids.accessory_product_ids.ids:
                accessory.append(acess)
            self.var_accessory_ids = accessory

    @api.onchange('optional_ids')
    def opt_accessories(self):
        accessory = []
        if self.optional_ids:
            for acess in self.optional_ids.accessory_product_ids.ids:
                accessory.append(acess)
            self.opt_accessories_ids = accessory

    def quote(self):
        quotelist = []
        for quote in self.quote_list.ids:
            quotelist.append(quote)
        for acess in self.accessories_ids.ids:
            quotelist.append(acess)
        for var in self.variant_ids.ids:
            quotelist.append(var)
        for varacess in self.var_accessory_ids.ids:
            quotelist.append(varacess)
        for opt in self.optional_ids.ids:
            quotelist.append(opt)
        for optacess in self.opt_accessories_ids.ids:
            quotelist.append(optacess)
        if self.wish_qty > self.product_qty:
            self.product_id.write({'wish_qty': self.wish_sec_qty})
            self.product_id.write({'pre_wish_qty': self.wish_qty})
        else:
            self.product_id.write({'wish_qty': self.wish_qty})

        ctx = dict()
        ctx.update({
            'default_partner_id': self.partner_id.id,
            'default_expire_date': self.expire_date,
            'default_payment_conditions': self.payment_conditions.id,
            'default_quote_list': quotelist
        })

        if self.concorrente and self.value:
            vals = {'product_id': self.product_id.id,
                    'name': self.concorrente.id,
                    'data': self.data,
                    'value': self.value}

            self.env['preco.concorrente'].create(vals)

        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'cotacoes',
            'views': [[self.env.ref("cotacoes.cotacoes_form_view").id, 'form']],
            'context': ctx,
            'target': 'new'
        }
