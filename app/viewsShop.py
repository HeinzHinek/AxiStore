# -*- coding: utf-8 -*-

from app import app
from flask import render_template
from flask_login import login_required, current_user
from flask.ext.babel import gettext
from models import Product
from config import NO_PHOTO_URL, USER_ROLES
from imageHelper import getImgUrls


@app.route('/shop')
@app.route('/shop/<int:page>')
@login_required
def shop(page=1):
    products = Product.query.filter_by(category_id=1).paginate(page, current_user.products_per_page, False)
    discount = 0
    if current_user.role == USER_ROLES['ROLE_CUSTOMER'] and current_user.customer:
        discount = current_user.customer.base_discount
    for p in products.items:
        p.available = p.qty_stock - p.request_qty
        p.ontheway = p.order_qty
        if p.available < 0:
            p.ontheway += p.available
            if p.ontheway < 0:
                p.ontheway = 0
            p.available = 0
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
    return render_template('/shop/shop.html',
                           title=gettext('AxiStore shop'),
                           products=products)