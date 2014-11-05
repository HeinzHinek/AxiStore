# -*- coding: utf-8 -*-

from app import app
from flask import render_template, g, session, request
from flask_login import login_required, current_user
from flask.ext.babel import gettext
from models import Product, Category
from forms import ShopHeaderForm
from config import NO_PHOTO_URL, USER_ROLES, AXM_PRODUCT_URL_JA
from imageHelper import getImgUrls


@app.route('/shop', methods=['GET', 'POST'])
@app.route('/shop/<int:page>', methods=['GET', 'POST'])
@login_required
def shop(page=1):
    products = Product.query.filter_by(active_flg=True)

    if not g.category_id:
        g.category = Category.query.first().id
    products = products.filter_by(category_id=int(g.category_id))

    if session['available_only'] is True:
        products = products.filter(Product.available_qty > 0)

    products = products.order_by(Product.maker_id, Product.code)
    products = products.paginate(page, current_user.products_per_page, False)

    discount = 0
    if current_user.role == USER_ROLES['ROLE_CUSTOMER'] and current_user.customer:
        discount = current_user.customer.base_discount
    for p in products.items:
        p.ontheway = p.order_qty
        if p.available_qty <= 0:
            p.ontheway += p.qty_stock - p.request_qty
            if p.ontheway < 0:
                p.ontheway = 0
        if not p.price_retail:
            p.price_retail = 0
        unrounded_price = p.price_retail * (1.0 - discount)
        p.customer_price = int(5 * round(float(unrounded_price)/5))

        urls = getImgUrls(p.id)
        p.img_urls = []
        if urls:
            for u in urls:
                u = u.split('app')[1]
                p.img_urls.append(u)
        else:
            p.img_urls.append(NO_PHOTO_URL.split('app')[1])
    form = ShopHeaderForm()
    form.category.choices = [(a.id, a.name_JP) for a in Category.query.all()]
    return render_template('/shop/shop.html',
                           title=gettext('AxiStore shop'),
                           products=products,
                           curr_category=g.category_id,
                           axm_product_url=AXM_PRODUCT_URL_JA,
                           form=form)


@app.route('/shop/add_to_cart', methods=['POST'])
@login_required
def add_to_cart():
    id = request.form['id'] if request.form['id'] else None
    qty = request.form['qty'] if request.form['qty'] else None

    if not id or not qty or not is_number(id) or not is_number(qty):
        return "NG"

    product = Product.query.filter_by(id=id).first()
    if not product:
        return "NG"

    if 'cart' not in session:
        session['cart'] = []

    #SMAZAT!!!
    session['cart'] = []

    session['cart'].append({'id': id, 'qty': qty})

    print session['cart']

    discount = current_user.customer.base_discount if current_user.customer else 0
    unrounded_price = product.price_retail * (1.0 - discount)
    customer_price = int(5 * round(float(unrounded_price)/5))

    html = "<tr>" \
           "<td style='text-align: left;'>" + product.code + "</td>" \
           "<td style='text-align: left;'>" + product.desc_JP + "</td>" \
           "<td style='text-align: right;'>" + str(customer_price) + "</td>" \
           "<td style='text-align: right;'>" + str(qty) + "</td>" \
           "<td style='text-align: right;'>" + str(customer_price * int(qty)) + "</td>" \
           "<td><button class='cart-item-remove-btn btn btn-danger btn-sm'>X</button>" \
           "<input type='hidden' class='hidden-id' value='" + str(product.id) + "'/>" \
           "<input type='hidden' class='hidden-qty' value='" + str(qty) + "'/>" \
           "</td>" \
           "</tr>"
    return html


@app.route('/shop/remove_from_cart', methods=['POST'])
@login_required
def remove_from_cart():
    id = request.form['id'] if request.form['id'] else None
    qty = request.form['qty'] if request.form['qty'] else None

    if not id or not qty or not is_number(id) or not is_number(qty):
        return "NG"
    return "OK"


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False