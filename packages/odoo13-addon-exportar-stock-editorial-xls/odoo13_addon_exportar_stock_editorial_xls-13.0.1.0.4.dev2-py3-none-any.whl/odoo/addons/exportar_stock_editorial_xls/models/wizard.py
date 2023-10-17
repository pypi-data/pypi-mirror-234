# -*- coding: utf-8 -*-
#############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2019-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
#    Author:Cybrosys Techno Solutions(odoo@cybrosys.com)
#
#    You can modify it under the terms of the GNU AFFERO
#    GENERAL PUBLIC LICENSE (AGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU AFFERO GENERAL PUBLIC LICENSE (AGPL v3) for more details.
#
#    You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
#    (AGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################
import time
from datetime import date, datetime
import pytz
import json
import datetime
import io
from odoo.addons.gestion_editorial import constants
from odoo import api, fields, models, _
from odoo.tools import date_utils
try:
    from odoo.tools.misc import xlsxwriter
except ImportError:
    import xlsxwriter


class StockReport(models.TransientModel):
    _name = "wizard.stock.history"
    _description = "Current Stock History"

    warehouse = fields.Many2many('stock.warehouse', 'wh_wiz_rel', 'wh', 'wiz', string='Warehouse', required=True)
    category = fields.Many2many('product.category', 'categ_wiz_rel', 'categ', 'wiz', string='Warehouse')

    def export_xls(self):
        data = {
            'ids': self.ids,
            'model': self._name,
            'warehouse': self.warehouse.ids,
            'category': self.category.ids,

        }
        return {
            'type': 'ir_actions_xlsx_download',
            'data': {'model': 'wizard.stock.history',
                     'options': json.dumps(data, default=date_utils.json_default),
                     'output_format': 'xlsx',
                     'report_name': 'Current Stock History',
                     }
        }

    def get_warehouse(self, data):
        wh = data.warehouse.mapped('id')
        obj = self.env['stock.warehouse'].search([('id', 'in', wh)])
        l1 = []
        l2 = []
        for j in obj:
            l1.append(j.name)
            l2.append(j.id)
        return l1, l2

    def get_lines(self, data, warehouse):
        lines = []
        categ_id = data.mapped('id')
        if categ_id:
            categ_products = self.env['product.product'].search([('categ_id', 'in', categ_id)])

        else:
            categ_products = self.env['product.product'].search([])
        product_ids = tuple([pro_id.id for pro_id in categ_products])
        purchase_query = """
               SELECT sum(p_o_l.product_qty) AS product_qty, p_o_l.product_id FROM purchase_order_line AS p_o_l
               JOIN purchase_order AS p_o ON p_o_l.order_id = p_o.id
               INNER JOIN stock_picking_type AS s_p_t ON p_o.picking_type_id = s_p_t.id
               WHERE p_o.state IN ('purchase','done')
               AND s_p_t.warehouse_id = %s AND p_o_l.product_id in %s group by p_o_l.product_id"""
        params = warehouse, product_ids if product_ids else (0, 0)
        self._cr.execute(purchase_query, params)
        pol_query_obj = self._cr.dictfetchall()
        for obj in categ_products:
            purchase_value = 0

            #Calcula el total de productos "Liquidados"
            liquidated_qty = obj.get_product_quantity_in_location(constants.LOCATION_ID_CUSTOMERS)

            #Calcula el total de productos "A mano - En Stock"
            on_hand_qty = obj.get_product_quantity_in_location(constants.LOCATION_ID_STOCK)

            #Calcula el total de productos "En distribución - En librerias"
            in_distribution_qty = obj.get_product_quantity_in_location(constants.LOCATION_ID_DEPOSITO)

            for pol_product in pol_query_obj:
                if pol_product['product_id'] == obj.id:
                    purchase_value = pol_product['product_qty']

            vals = {
                'sku': obj.default_code,
                'name': obj.name,
                'category': obj.categ_id.name,
                'cost_price': obj.standard_price,
                'owned': purchase_value - liquidated_qty,
                'available': on_hand_qty,
                'in_distribution': in_distribution_qty,
                'sale_value': liquidated_qty,
                'purchase_value': purchase_value,
            }
            lines.append(vals)
        return lines

    def get_xlsx_report(self, data, response):
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        lines = self.browse(data['ids'])
        d = lines.category
        get_warehouse = self.get_warehouse(lines)
        count = len(get_warehouse[0]) * 11 + 6
        comp = self.env.user.company_id.name
        sheet = workbook.add_worksheet('Stock Info')
        format0 = workbook.add_format({'font_size': 20, 'align': 'center', 'bold': True})
        format1 = workbook.add_format({'font_size': 14, 'align': 'vcenter', 'bold': True})
        format11 = workbook.add_format({'font_size': 12, 'align': 'center', 'bold': True})
        format21 = workbook.add_format({'font_size': 10, 'align': 'center', 'bold': True})
        format3 = workbook.add_format({'bottom': True, 'top': True, 'font_size': 12})
        format4 = workbook.add_format({'font_size': 12, 'align': 'left', 'bold': True})
        font_size_8 = workbook.add_format({'font_size': 8, 'align': 'center'})
        font_size_8_l = workbook.add_format({'font_size': 8, 'align': 'left'})
        font_size_8_r = workbook.add_format({'font_size': 8, 'align': 'right'})
        red_mark = workbook.add_format({'font_size': 8, 'bg_color': 'red'})
        justify = workbook.add_format({'font_size': 12})
        format3.set_align('center')
        justify.set_align('justify')
        format1.set_align('center')
        red_mark.set_align('center')
        sheet.merge_range(1, 7, 2, 10, 'Product Stock Info', format0)
        sheet.merge_range(3, 7, 3, 10, comp, format11)
        w_house = ', '
        cat = ', '
        c = []
        d1 = d.mapped('id')
        if d1:
            for i in d1:
                c.append(self.env['product.category'].browse(i).name)
            cat = cat.join(c)
            sheet.merge_range(4, 0, 4, 1, 'Category(s) : ', format4)
            sheet.merge_range(4, 2, 4, 3 + len(d1), cat, format4)
        sheet.merge_range(5, 0, 5, 1, 'Almacenes : ', format4)
        w_house = w_house.join(get_warehouse[0])
        sheet.merge_range(5, 2, 5, 3 + len(get_warehouse[0]), w_house, format4)
        user = self.env['res.users'].browse(self.env.uid)
        tz = pytz.timezone(user.tz if user.tz else 'UTC')
        times = pytz.utc.localize(datetime.datetime.now()).astimezone(tz)
        sheet.merge_range('A8:G8', 'Fecha: ' + str(times.strftime("%Y-%m-%d %H:%M %p")), format1)
        sheet.merge_range(7, 7, 7, count, 'Almacenes', format1)
        sheet.merge_range('A9:G9', 'Información de producto', format11)
        w_col_no = 6
        w_col_no1 = 7
        for i in get_warehouse[0]:
            w_col_no = w_col_no + 11
            sheet.merge_range(8, w_col_no1, 8, w_col_no, i, format11)
            w_col_no1 = w_col_no1 + 11
        sheet.write(9, 0, 'SKU', format21)
        sheet.merge_range(9, 1, 9, 3, 'Nombre', format21)
        sheet.merge_range(9, 4, 9, 5, 'Categoría', format21)
        sheet.write(9, 6, 'Precio', format21)
        p_col_no1 = 7
        for i in get_warehouse[0]:
            sheet.merge_range(9, p_col_no1, 9, p_col_no1 + 1, 'En propiedad', format21)
            sheet.merge_range(9, p_col_no1 + 2, 9, p_col_no1 + 3, 'En stock', format21)
            sheet.merge_range(9, p_col_no1 + 4, 9, p_col_no1 + 5, 'En distribución', format21)
            sheet.merge_range(9, p_col_no1 + 6, 9, p_col_no1 + 7, 'Total Comprado', format21)
            sheet.merge_range(9, p_col_no1 + 8, 9, p_col_no1 + 9, 'Total Liquidado', format21)
            p_col_no1 = p_col_no1 + 11
        prod_row = 10
        prod_col = 0
        for i in get_warehouse[1]:
            get_line = self.get_lines(d, i)
            for each in get_line:
                sheet.write(prod_row, prod_col, each['sku'], font_size_8)
                sheet.merge_range(prod_row, prod_col + 1, prod_row, prod_col + 3, each['name'], font_size_8_l)
                sheet.merge_range(prod_row, prod_col + 4, prod_row, prod_col + 5, each['category'], font_size_8_l)
                sheet.write(prod_row, prod_col + 6, each['cost_price'], font_size_8_r)
                prod_row = prod_row + 1
            break
        prod_row = 10
        prod_col = 7
        for i in get_warehouse[1]:
            get_line = self.get_lines(d, i)
            for each in get_line:
                cell_format = red_mark if each['owned'] < 0 else font_size_8
                sheet.merge_range(prod_row, prod_col , prod_row, prod_col + 1, each['owned'], cell_format)

                cell_format = red_mark if each['available'] < 0 else font_size_8
                sheet.merge_range(prod_row, prod_col +2 , prod_row, prod_col + 3, each['available'], cell_format)

                cell_format = red_mark if each['in_distribution'] < 0 else font_size_8
                sheet.merge_range(prod_row, prod_col +4 , prod_row, prod_col + 5, each['in_distribution'], cell_format)

                cell_format = red_mark if each['purchase_value'] < 0 else font_size_8
                sheet.merge_range(prod_row, prod_col + 6, prod_row, prod_col + 7, each['purchase_value'], cell_format)

                cell_format = red_mark if each['sale_value'] < 0 else font_size_8
                sheet.merge_range(prod_row, prod_col + 8, prod_row, prod_col + 9, each['sale_value'], cell_format)

                prod_row = prod_row + 1

            prod_row = 10
            prod_col = prod_col + 11
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
