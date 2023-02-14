from odoo import models, fields, api, _
from odoo.exceptions import UserError
import datetime

class InheritRotas(models.Model):
    _inherit = 'routes'
    validade = fields.Integer(string="Validade da rota")

