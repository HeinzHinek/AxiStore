# -*- coding: utf-8 -*-

from app import app, db, mailer
from flask import render_template, g, session, request, json, redirect, url_for, flash
from flask_login import login_required, current_user, customer_allowed
from flask.ext.babel import gettext
from models import Product, Category, Cart, Request, RequestedProducts
from forms import ShopHeaderForm, CartOrderForm
from config import NO_PHOTO_URL, USER_ROLES, AXM_PRODUCT_URL_JA, MAIL_USERNAME
from imageHelper import getImgUrls
from sqlalchemy import or_


@app.route('/shop', methods=['GET', 'POST'])
@app.route('/shop/<int:page>', methods=['GET', 'POST'])
@customer_allowed
@login_required
def shop(page=1):
    products = Product.query.filter_by(active_flg=True)

    curr_search = None
    if session['search_string']:
        curr_search = session['search_string']
        products = products.filter(or_(Product.code.like('%' + session['search_string'] + '%'),
                                       (Product.desc_CS.like('%' + session['search_string'] + '%')),
                                       (Product.desc_JP.like('%' + session['search_string'] + '%'))))

    if g.category_id:
        products = products.filter_by(category_id=int(g.category_id))

    if session['available_only'] is True:
        products = products.filter(Product.available_qty > 0)

    products = products.order_by(Product.maker_id, Product.code)
    products = products.paginate(page, current_user.products_per_page, False)

    discount = 0
    if current_user.role == USER_ROLES['ROLE_CUSTOMER'] and current_user.customer:
        discount = current_user.customer.base_discount
    for p in products.items:

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
    categories = [(a.id, a.name_JP) for a in Category.query.all()]
    categories = [(0, gettext('All'))] + categories
    form.category.choices = categories
    return render_template('/shop/shop.html',
                           title=gettext('AxiStore shop'),
                           products=products,
                           curr_category=g.category_id,
                           axm_product_url=AXM_PRODUCT_URL_JA,
                           curr_search=curr_search,
                           form=form)


@app.route('/shop/restrict', methods=['POST'])
@customer_allowed
@login_required
def restrict():
    form = ShopHeaderForm(request.form)
    if form.is_submitted():
        string = form.search.data
        if string:
            if len(string) > 1:
                return redirect(url_for('shop', search=string))
    if session['search_string']:
        return redirect(url_for('shop', search=session['search_string']))
    return redirect('shop')


@app.route('/clearshopsearch')
@customer_allowed
@login_required
def clearshopsearch():
    session['search_string'] = None
    return redirect(url_for('shop'))


@app.route('/shop/placeorder', methods=['GET', 'POST'])
@customer_allowed
@login_required
def placeorder():

    cart_items = Cart.query.filter_by(user_id=current_user.id).all()

    form = CartOrderForm()
    if form.validate_on_submit():
        new_request = Request()
        new_request.user_id = current_user.id
        if not current_user.customer:
            flash(gettext("We apologize but your customer data is insufficient. Please, contact our customer support."))
            return redirect(url_for("shop"))
        new_request.customer_id = current_user.customer.id
        new_request.active_flg = True
        db.session.add(new_request)
        db.session.commit()

        for item in cart_items:
            new_product = db.session.query(Product).filter_by(id=item.product_id).first()
            if not new_product:
                flash(gettext("Product not found."))
                return redirect(url_for("shop"))
            rp = RequestedProducts(quantity=item.quantity)
            rp.product = new_product
            rp.request_id = new_request.id
            new_request.products.append(rp)
            db.session.delete(item)

        db.session.commit()

        # send confirmation email
        mailer.order_confirmation(current_user, new_request)

        flash(gettext("Order created successfully."))
        return redirect(url_for("orderconfirm", req_id=new_request.id))

    discount = 0
    if current_user.role == USER_ROLES['ROLE_CUSTOMER'] and current_user.customer:
        discount = current_user.customer.base_discount
    total = 0
    pieces = 0
    for item in cart_items:
        if not item.product.price_retail:
            item.product.price_retail = 0
        unrounded_price = item.product.price_retail * (1.0 - discount)
        item.customer_price = int(5 * round(float(unrounded_price)/5))
        total += item.customer_price * item.quantity
        pieces += item.quantity

        urls = getImgUrls(item.product.id)
        if urls:
            item.img_url = urls[0].split('app')[1]
        else:
            item.img_url = NO_PHOTO_URL.split('app')[1]

    return render_template('/shop/placeorder.html',
                           title=gettext('Place order'),
                           cart_items=cart_items,
                           total=total,
                           pieces=pieces,
                           form=form)


@app.route('/shop/orderconfirm')
@customer_allowed
@login_required
def orderconfirm():
    req_id = request.args.get('req_id')
    req = Request.query.filter_by(id=req_id).first()
    if not req:
        flash(gettext("Unfortunatelly, your request could not be processed. Please, contact our customer support."))
        redirect(url_for('shop'))

    requested_products = RequestedProducts.query.filter_by(request_id=req_id).all()
    discount = 0
    if current_user.role == USER_ROLES['ROLE_CUSTOMER'] and current_user.customer:
        discount = current_user.customer.base_discount
    total = 0
    pieces = 0
    for rp in requested_products:
        if not rp.product.price_retail:
            rp.product.price_retail = 0
        unrounded_price = rp.product.price_retail * (1.0 - discount)
        rp.customer_price = int(5 * round(float(unrounded_price)/5))
        rp.subtotal = rp.customer_price * rp.quantity
        total += rp.subtotal
        pieces += rp.quantity

    return render_template('/shop/orderconfirm.html',
                           title=gettext('Order Confirmation'),
                           requested_products=requested_products,
                           total=total,
                           pieces=pieces)


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