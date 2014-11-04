# -*- coding: utf-8 -*-

from app import app
from flask import render_template, g, session
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