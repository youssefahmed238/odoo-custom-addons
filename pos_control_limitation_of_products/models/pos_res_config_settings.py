from odoo import fields, models, api
from odoo.exceptions import ValidationError


class PosResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    pos_control_limitation_of_products = fields.Boolean('Customize Products Limit')
    pos_products_limit = fields.Integer(default=10)

    @api.constrains('pos_products_limit')
    def _check_pos_products_limit(self):
        for rec in self:
            if rec.pos_products_limit <= 0:
                raise ValidationError("The product limit must be greater than zero.")
            if rec.pos_products_limit > 100:
                raise ValidationError("The product limit must not exceed 100.")

    @api.onchange('pos_control_limitation_of_products')
    def _onchange_pos_control_limitation_of_products(self):
        if not self.pos_control_limitation_of_products:
            self.pos_products_limit = 10

    @api.onchange('pos_products_limit')
    def _onchange_pos_products_limit(self):
        self.pos_control_limitation_of_products = self.pos_products_limit != 10

    def get_values(self):
        res = super(PosResConfigSettings, self).get_values()
        icp = self.env['ir.config_parameter'].sudo()

        is_custom_limit = bool(icp.get_param('pos_control_limitation_of_products', default='False'))
        limit = int(icp.get_param('point_of_sale.limited_product_count', default='11'))

        if limit == 11:
            is_custom_limit = False

        res.update(
            pos_control_limitation_of_products=is_custom_limit,
            pos_products_limit=limit - 1,
        )
        return res

    def set_values(self):
        super(PosResConfigSettings, self).set_values()
        icp = self.env['ir.config_parameter'].sudo()

        if not self.pos_control_limitation_of_products:
            icp.set_param('point_of_sale.limited_product_count', '11')
        else:
            icp.set_param('point_of_sale.limited_product_count', str(self.pos_products_limit + 1))

        icp.set_param('pos_control_limitation_of_products', str(self.pos_control_limitation_of_products))
