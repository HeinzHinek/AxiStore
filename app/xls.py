# -*- coding: utf-8 -*-

from config import NOHINSHO_PATH
import xlsxwriter

class CreateXls():

    def nohinsho(self, date, customer, products):

        if not customer.order_no:
            customer.order_no = 1
        cust_name = customer.name.replace(" ", "_")

        filename = NOHINSHO_PATH + 'Nohinsho_' + chr(64 + int(customer.order_no)) + '_' + cust_name + '_' + date.strftime("%Y%m%d") + '.xlsx'

        workbook = xlsxwriter.Workbook(filename)
        worksheet = workbook.add_worksheet(unicode('納品書', 'utf-8'))

        align_right = workbook.add_format({
            'align': 'right'
        })
        title_format = workbook.add_format({
            'bold': 1,
            'align': 'center',
            'valign': 'vcenter',
            'font_name': unicode('ＭＳ Ｐ明朝', 'utf-8')})
        title_format.set_font_size(18)
        comp_name_format = workbook.add_format({
            'font_size': 16,
            'bottom': 1,
            'align': 'center'
        })
        our_address_format = workbook.add_format({
            'font_size': 9,
            'align': 'right'
        })
        header_details = workbook.add_format({
            'left': 2,
            'top': 2,
            'right': 2,
            'bottom': 1,
            'align': 'center',
            'bg_color': '#CCCCFF'
        })
        header_left = workbook.add_format({
            'left': 2,
            'top': 1,
            'right': 1,
            'bottom': 1,
            'font_size': 8,
            'align': 'center',
            'bg_color': '#CCCCFF'
        })
        header_middle = workbook.add_format({
            'left': 1,
            'top': 1,
            'right': 1,
            'bottom': 1,
            'font_size': 8,
            'align': 'center',
            'bg_color': '#CCCCFF'
        })
        header_right = workbook.add_format({
            'left': 1,
            'top': 1,
            'right': 2,
            'bottom': 1,
            'font_size': 8,
            'align': 'center',
            'bg_color': '#CCCCFF'
        })
        header_divider = workbook.add_format({
            'left': 2,
            'top': 1,
            'right': 2,
            'bottom': 7,
            'bg_color': '#CCCCFF'
        })

        prod_left = workbook.add_format({
            'left': 2,
            'top': 7,
            'right': 7,
            'bottom': 7,
            'font_size': 11
        })
        prod_middle = workbook.add_format({
            'left': 7,
            'top': 7,
            'right': 7,
            'bottom': 7,
            'font_size': 9,
            'font_name': 'MS PGothic'
        })
        prod_num = workbook.add_format({
            'left': 7,
            'top': 7,
            'right': 7,
            'bottom': 7,
            'font_size': 10,
            'align': 'right',
            'font_name': 'MS PGothic',
            'num_format': '# ##0'
        })
        prod_right = workbook.add_format({
            'left': 7,
            'top': 7,
            'right': 2,
            'bottom': 7,
            'font_size': 10,
            'align': 'right',
            'font_name': 'MS PGothic',
            'num_format': '# ##0'
        })

        total_left = workbook.add_format({
            'left': 1,
            'top': 2,
            'right': 0,
            'bottom': 1,
            'font_size': 11,
            'align': 'right',
            'font_name': 'MS PGothic'
        })
        total_middle = workbook.add_format({
            'left': 0,
            'top': 2,
            'right': 0,
            'bottom': 1,
            'font_size': 10,
            'align': 'right',
            'font_name': 'MS PGothic'
        })
        total_right = workbook.add_format({
            'left': 0,
            'top': 2,
            'right': 1,
            'bottom': 1,
            'font_size': 10,
            'align': 'right',
            'font_name': 'MS PGothic',
            'num_format': '# ##0'
        })

        account_top = workbook.add_format({
            'left': 2,
            'top': 2,
            'right': 2,
            'underline': 1,
            'font_name': 'MS PGothic',
        })
        account_middle = workbook.add_format({
            'left': 2,
            'right': 2,
            'font_name': 'MS PGothic',
        })
        account_bottom = workbook.add_format({
            'left': 2,
            'bottom': 2,
            'right': 2,
            'font_name': 'MS PGothic',
        })

        worksheet.set_column('A:A', 4)
        worksheet.set_column('B:B', 8)
        worksheet.set_column('C:C', 36)
        worksheet.set_column('D:D', 8)
        worksheet.set_column('E:E', 8)
        worksheet.set_column('F:F', 6)
        worksheet.set_column('G:G', 8)
        worksheet.set_column('H:H', 4)

        worksheet.write('H1', unicode('発送日：' + date.strftime("%Y年%m月%d日"), 'utf-8'), align_right)

        worksheet.merge_range('A2:H2', unicode('納品書' + chr(64 + int(customer.order_no)), 'utf-8'), title_format)

        worksheet.merge_range('A4:D4', customer.contact.company_name, comp_name_format)
        worksheet.write('E4', unicode('御中', 'utf-8'))
        worksheet.write('A5', str.decode('〒', 'utf-8') + unicode(customer.contact.post_code)[:3] + unicode('-') + unicode(customer.contact.post_code)[3:]\
                        + unicode(' ') + customer.contact.address1)
        worksheet.write('A6', customer.contact.address2)
        worksheet.write('A7', customer.contact.address3)

        worksheet.write('H4', unicode('Axis Mundi株式会社', 'utf-8'), our_address_format)
        worksheet.write('H5', unicode('〒 160-0022', 'utf-8'), our_address_format)
        worksheet.write('H6', unicode('東京都新宿区新宿2-6-3', 'utf-8'), our_address_format)
        worksheet.write('H7', unicode('藤和新宿コープ810', 'utf-8'), our_address_format)
        worksheet.write('H8', unicode('電  話：080-4933-4766 (代)', 'utf-8'), our_address_format)
        worksheet.write('H9', unicode('E-Mail：info@axis-mundi.jp', 'utf-8'), our_address_format)

        worksheet.write('A10', unicode('平素は格別のご高配を賜り、厚く御礼申し上げます。', 'utf-8'))
        worksheet.write('A11', unicode('以下の通り、ご請求致します。', 'utf-8'))

        worksheet.merge_range('B13:G13', unicode('明　　細', 'utf-8'), header_details)
        worksheet.write('B14', unicode('商品番', 'utf-8'), header_left)
        worksheet.write('C14', unicode('商品名', 'utf-8'), header_middle)
        worksheet.write('D14', unicode('税込み上代', 'utf-8'), header_middle)
        worksheet.write('E14', unicode('税込み下代', 'utf-8'), header_middle)
        worksheet.write('F14', unicode('数量', 'utf-8'), header_middle)
        worksheet.write('G14', unicode('小計', 'utf-8'), header_right)
        worksheet.merge_range('B15:G15', '', header_divider)

        total = 0
        for idx, item in enumerate(products):

            if not item['product'].price_retail:
                item['product'].price_retail = 0
            price_wholesale = item['product'].price_retail
            if customer.base_discount:
                 price_wholesale *= (1.0 - customer.base_discount)
            formula = '=E' + str(idx+16) + '*F' + str(idx+16)

            worksheet.write_string(idx+15, 1, item['product'].code, prod_left)
            worksheet.write_string(idx+15, 2, item['product'].desc_JP, prod_middle)
            worksheet.write_number(idx+15, 3, item['product'].price_retail, prod_num)
            worksheet.write_number(idx+15, 4, price_wholesale, prod_num)
            worksheet.write_number(idx+15, 5, item['qty'], prod_num)
            worksheet.write_formula(idx+15, 6, formula, prod_right)
            total += price_wholesale * item['qty']

        delta = len(products)+16
        range = 'B' + str(delta) + ':E' + str(delta)
        worksheet.merge_range(range, unicode('税込み合計', 'utf-8'), total_left)
        worksheet.write_string('F'+str(delta), unicode('￥', 'utf-8'), total_middle)
        worksheet.write_formula('G'+str(delta), '=SUM(G16:G' + str(len(products)+15) + ')', total_right)

        worksheet.write_string('B'+str(delta+1), unicode('※上記差引ご請求金額を下記振込指定口座へお振込み下さい。', 'utf-8'))
        worksheet.write_string('B'+str(delta+2), unicode('※お振込み頂く際の振込手数料は、御社負担にてお願い致します。', 'utf-8'))

        delta = len(products)+19
        range = 'B' + str(delta) + ':G' + str(delta)
        worksheet.merge_range(range, unicode('振込先：', 'utf-8'), account_top)
        delta = len(products)+20
        range = 'B' + str(delta) + ':G' + str(delta)
        worksheet.merge_range(range, unicode('銀行名：楽天銀行：', 'utf-8'), account_middle)
        delta = len(products)+21
        range = 'B' + str(delta) + ':G' + str(delta)
        worksheet.merge_range(range, unicode(' 支店名：第一営業支店（支店番号：251）', 'utf-8'), account_middle)
        delta = len(products)+22
        range = 'B' + str(delta) + ':G' + str(delta)
        worksheet.merge_range(range, unicode(' 預金科目：普通', 'utf-8'), account_middle)
        delta = len(products)+23
        range = 'B' + str(delta) + ':G' + str(delta)
        worksheet.merge_range(range, unicode(' 口座番号：7262776', 'utf-8'), account_middle)
        delta = len(products)+24
        range = 'B' + str(delta) + ':G' + str(delta)
        worksheet.merge_range(range, unicode('  口座名義：アクシス　ムンディ（カ　Axis　Mundi株式会社', 'utf-8'), account_bottom)

        workbook.close()
        return filename