from odoo import models, fields, api, _


class CliInherit(models.Model):
    _inherit = 'res.partner'

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        name_split = name.split()
        array = []
        for palavra in name_split:
            array.append('|')
            array.append('|')
            array.append(('name', operator, palavra))
            array.append(('cod_hitec', operator, palavra))
            array.append(('phone', operator, palavra))
        if name:
            pesquisa = self.search(array)
            return pesquisa.name_get()
        return self.search([('name', operator, name)] + args, limit=limit).name_get()