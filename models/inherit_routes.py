from odoo import models, fields, api, _
from odoo.exceptions import UserError
import datetime


class DiaRota(models.Model):
    _name = 'dia.rota'

    _rec_name = 'dia'
    dia = fields.Char()


class InheritRotas(models.Model):
    _inherit = 'routes'

    dia_rota = fields.Many2many(
        'dia.rota',
        string="dia da rota",
        relation="rel_dia_rota_routes"
    )

