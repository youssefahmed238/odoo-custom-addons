from odoo import fields, models, api
from odoo.exceptions import ValidationError


class PosResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    pos_control_limitation_of_products = fields.Boolean(
        string='Customize Products Limit', config_parameter='pos_control_limitation_of_products')

    pos_products_limit = fields.Integer(default=10,
                                        config_parameter='pos_products_limit')


    @api.onchange('pos_control_limitation_of_products')
    def _onchange_pos_control_limitation_of_products(self):
        if not self.pos_control_limitation_of_products:
            self.pos_products_limit = 10

    @api.onchange('pos_products_limit')
    def _onchange_pos_products_limit(self):
        if self.pos_products_limit == 10:
            self.pos_control_limitation_of_products = False

    @api.constrains('pos_products_limit')
    def _check_pos_products_limit(self):
        if self.pos_products_limit <= 0:
            raise ValidationError("The product limit must be greater than zero.")
        if self.pos_products_limit > 100:
            raise ValidationError("The product limit must not exceed 100.")