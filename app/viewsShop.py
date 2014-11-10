# -*- coding: utf-8 -*-

from app import app, db
from flask import render_template, g, session, request, json, redirect, url_for
from flask_login import login_required, current_user, customer_allowed
from flask.ext.babel import gettext
from models import Product, Category, Cart
from forms import ShopHeaderForm
from config import NO_PHOTO_URL, USER_ROLES, AXM_PRODUCT_URL_JA
from imageHelper import getImgUrls


@app.route('/shop', methods=['GET', 'POST'])
@app.route('/shop/<int:page>', methods=['GET', 'POST'])
@customer_allowed
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


@app.route('/shop/placeorder', methods=['GET', 'POST'])
@customer_allowed
@login_required
def placeorder():
    return redirect(url_for('logout'))


# AJAX methods below

@app.route('/shop/open_cart', methods=['GET'])
@customer_allowed
@login_required
def open_cart():
    cart_items = current_user.cart_items.all()
    discount = 0
    if current_user.role == USER_ROLES['ROLE_CUSTOMER'] and current_user.customer:
        discount = current_user.customer.base_discount
    for item in cart_items:
        base_price = item.product.price_retail if item.product.price_retail else 0
        unrounded_price = base_price * (1.0 - discount)
        item.customer_price = int(5 * round(float(unrounded_price)/5))
        item.subtotal = item.customer_price * item.quantity
    return render_template('/shop/_cart_table.html',
                           cart_items=cart_items)


@app.route('/shop/add_to_cart', methods=['POST'])
@customer_allowed
@login_required
def add_to_cart():
    id = request.form['id'] if request.form['id'] else None
    qty = request.form['qty'] if request.form['qty'] else None

    if not id or not qty or not is_number(id) or not is_number(qty):
        return "NG"

    product = Product.query.filter_by(id=id).first()
    if not product:
        return "NG"

    existing = Cart.query.filter_by(user_id=current_user.id, product_id=id).first()
    if existing:
        existing.quantity += int(qty)
        cart = existing
    else:
        cart = Cart()
        cart.add_to_cart(current_user.id, id, qty)
    db.session.add(cart)
    db.session.commit()

    return "OK"


@app.route('/shop/remove_from_cart', methods=['POST'])
@customer_allowed
@login_required
def remove_from_cart():

    id = request.form['id'] if request.form['id'] else None
    if not id or not is_number(id):
        return "NG"

    item_to_remove = Cart.query.filter_by(product_id=id).first()
    db.session.delete(item_to_remove)
    db.session.commit()

    return "OK"


@app.route('/shop/update_cart', methods=['POST'])
@customer_allowed
@login_required
def update_cart():
    data = request.form['data'] if request.form['data'] else None
    values = json.loads(data)
    for item in values:
        id = int(item[0])
        qty = int(item[1])
        cart_item = Cart.query.filter_by(user_id=current_user.id, product_id=id).first();
        if not cart_item:
            return "NG"
        if qty > 0:
            cart_item.quantity = qty
            db.session.add(cart_item)
        else:
            db.session.delete(cart_item)
    db.session.commit()
    return open_cart()


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False