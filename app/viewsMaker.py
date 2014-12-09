# -*- coding: utf-8 -*-

from flask import render_template, flash, redirect, url_for, request, session, g
from app import app, db
from forms import AddMakerForm, SimpleSubmitForm
from models import Maker, Category, Product, Order, OrderedProducts
from flask_login import login_required, maker_allowed
from imageHelper import getImgUrls, getThumbUrls
from config import DEFAULT_PER_PAGE, NO_PHOTO_URL, NO_PHOTO_THUMB_URL
from flask.ext.babel import gettext

@app.route('/makers')
@app.route('/makers/<int:page>')
@login_required
def makers(page=1):
    makers = Maker.query.paginate(page, DEFAULT_PER_PAGE, False)
    return render_template('settings/makers.html',
                           title=gettext("Makers"),
                           makers=makers)


@app.route('/addmaker', methods=['GET', 'POST'])
@login_required
def addMaker():
    form = AddMakerForm()
    form.category.choices = [(a.id, a.name_CS) for a in Category.query.all()]
    if form.validate_on_submit():
        maker = Maker()
        maker.name = form.name.data
        maker.category_id = form.category.data
        db.session.add(maker)
        db.session.commit()
        flash(gettext("New maker successfully added."))
        return redirect(url_for("makers"))
    return render_template('settings/addMaker.html',
                           title=gettext("Add New Maker"),
                           form=form)


@app.route('/editmaker/<int:id>', methods=['GET', 'POST'])
@login_required
def editMaker(id=0):
    maker = Maker.query.filter_by(id=id).first()
    if maker == None:
        flash(gettext('Maker not found.'))
        return redirect(url_for('makers'))
    form = AddMakerForm(obj=maker)
    form.category.choices = [(a.id, a.name_CS) for a in Category.query.all()]
    if form.validate_on_submit():

        #delete maker
        if 'delete' in request.form:
            db.session.delete(maker)
            db.session.commit()
            return redirect(url_for("makers"))

        #update maker
        maker.name = form.name.data
        maker.category_id = form.category.data
        maker.standard_delivery_days = form.standard_delivery_days.data
        db.session.add(maker)
        db.session.commit()
        flash(gettext("Maker successfully changed."))
        return redirect(url_for("makers"))

    selected = maker.category_id
    return render_template('settings/editMaker.html',
                           title=gettext("Edit Maker"),
                           maker=maker,
                           selected=selected,
                           form=form)


@app.route('/maker/makerstock', methods=['GET', 'POST'])
@maker_allowed
@login_required
def makerStock():
    products = None
    if g.user.maker:
        products = Product.query.filter_by(active_flg=True)\
            .filter_by(maker_id=g.user.maker_id)\
            .all()

    if products:
        for p in products:
            if not p.price_unit:
                p.price_retail = 0
            urls = getImgUrls(p.id)
            p.img_urls = []
            p.img_thumb_urls = []
            if urls:
                for u in urls:
                    u = u.split('app')[1]
                    p.img_urls.append(u)
                    p.img_thumb_urls.append(getThumbUrls(u, height=80, width=80).split('app')[1])
            else:
                p.img_urls.append(NO_PHOTO_URL.split('app')[1])
                p.img_thumb_urls.append(NO_PHOTO_THUMB_URL.split('app')[1])

    form = SimpleSubmitForm()

    if form.is_submitted():
        string = request.form.getlist('product_data')
        if string:
            data_to_update = []
            for s in string:
                raw = s.split(',')
                id = int(raw[0].split(':')[1])
                code = raw[1].split(':')[1]
                str_qty = raw[2].split(':')[1]
                qty = 0
                if str_qty:
                    try:
                        qty = int(str_qty)
                    except ValueError:
                        qty = 0;
                data_to_update.append({'id': id, 'code': code, 'qty': qty})
            if data_to_update:
                for d in data_to_update:
                    p = Product.query.get(d['id'])
                    p.maker_code = d['code']
                    p.maker_qty_stock = d['qty']
                    db.session.add(p)
                db.session.commit()


    return render_template('maker/makerStock.html',
                           title=gettext("My Stock"),
                           products=products,
                           form=form)


@app.route('/maker/makerorders')
@app.route('/maker/makerorders/<int:page>')
@maker_allowed
@login_required
def makerOrders(page=1):

    limit = DEFAULT_PER_PAGE

    # filtering orders for specific product
    product_id = request.args.get('product_id')
    curr_product = None
    if product_id:
        active = True
        limit = -1
        curr_product = Product.query.get(product_id)
    else:
        active = session['active_orders']
        if active is None:
            active = True

    orders = Order.query\
        .filter_by(active_flg=active)\
        .filter_by(maker_id=g.user.maker_id)

    if product_id:
        orders = orders.join(OrderedProducts).filter_by(product_id=product_id)

    len_active = len(Order.query
                     .filter_by(active_flg=True)
                     .filter_by(maker_id=g.user.maker_id)
                     .all())
    len_closed = len(Order.query
                     .filter_by(active_flg=False)
                     .filter_by(maker_id=g.user.maker_id)
                     .all())

    orders = orders.paginate(page, limit, False)
    return render_template('maker/makerOrders.html',
                           title=gettext("Orders from Axis Mundi"),
                           orders=orders,
                           active=active,
                           len_active=len_active,
                           len_closed=len_closed,
                           curr_product=curr_product)