from odoo import fields, models, _, api


class ProductSearch(models.TransientModel):
    _name = 'product.search'

    #barra de pesquisa
    product_search = fields.Char()

    #mensagem caso não encontre produto
    show_msg_not_found = fields.Boolean()

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
            'name': 'Informações do Produto',
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
            'name': 'Cotações',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'cotacoes',
            'views': [[self.env.ref("cotacoes.cotacoes_form_view").id,'form']],
            'context': ctx,
            'target': 'new'
        }
    
    @api.onchange('product_search')
    def search_bar(self): # função para pesquisar o produto com o campo 'product_search'
        if self.product_search:
            name_split = self.product_search.split() # função que separa o que foi escrito por espaço
            domain = [] # variável que armazenará o domain
            for palavra in name_split: # for que caminha em tudo que foi escrito e pesquisa as condições abaixo em cada palavra
                domain.append('|')
                domain.append('|')
                domain.append('|')
                domain.append('|')
                domain.append(('name', 'ilike', palavra))
                domain.append(('product_template_attribute_value_ids', 'ilike', palavra))
                domain.append(('fipe_ids', 'ilike', palavra))
                domain.append(('codigo_fipe', 'ilike', palavra))
                domain.append(('fipe_ano', 'ilike', palavra))
            products = self.env['product.product'].search(domain) # variável que armazena os produtos encontrados
            if len(products) == 0: # condição para dar valor à variável que fará com que a mensagem apareça para o vendedor
                self.show_msg_not_found = True
            else:
                self.show_msg_not_found = False
            if self.product_search: # domain final
                return {"domain": {'product_id': [('id', 'in', products.ids)]}}
            else:
                return {'domain': {'product_id': []}}
        else: # else para limpar o campo produto caso o campo de pesquisa seja apagado
            self.product_id = False

    def visualize_product(self):
        pass