# -*- coding: utf-8 -*-

from flask import render_template, redirect, flash, url_for, request, g
from app import app, db
from forms import SelectMakerForm, ProductQuantityForm
from models import Order, Product, OrderedProducts, Maker
from flask_login import login_required
from config import DEFAULT_PER_PAGE
from flask.ext.babel import gettext


@app.route('/orders')
@app.route('/orders/<int:page>')
@login_required
def orders(page=1):
    orders = Order.query\
        .order_by(Order.active_flg.desc())\
        .order_by(Order.created_dt)\
        .paginate(page, DEFAULT_PER_PAGE, False)
    return render_template('orders/orders.html',
                           title=gettext("Orders to maker"),
                           orders=orders)


@app.route('/order/create', methods=['GET', 'POST'])
@login_required
def createOrder():
    formMaker = SelectMakerForm()
    formMaker.maker.choices = [(a.id, a.name) for a in Maker.query.all()]
    formQuantities = ProductQuantityForm()
    products = None
    if formMaker.is_submitted():
        if formMaker.validate_on_submit():

            maker_id = formMaker.maker.data
            if not maker_id:
                flash(gettext("Maker not found."))
                return redirect(url_for("orders"))

            products = Product.query.order_by(Product.net_stock, Product.maker_id, Product.code)\
                .filter_by(maker_id=int(maker_id),
                           active_flg=True).all()
            for p in products:
                formQuantities.fields.append_entry()

    return render_template('orders/createOrder.html',
                           title=gettext("Place new order to maker"),
                           formMaker=formMaker,
                           formQuantities=formQuantities,
                           products=products)


@app.route('/order/placeorder', methods=['GET', 'POST'])
@login_required
def placeOrder():
    formQuantities = ProductQuantityForm(request.form)
    maker_id = request.form['maker_id']
    if not maker_id:
        flash(gettext("Maker not found."))
        return redirect(url_for("orders"))

    if formQuantities.validate_on_submit():

        new_order = Order()
        #TODO other date than now   new_order.created_dt =
        new_order.maker_id = maker_id
        new_order.user_id = g.user.id
        db.session.add(new_order)
        db.session.commit()

        #add ordered products to new order
        form_data = formQuantities.data['fields']
        for product in form_data:
            new_quantity = int(product['qty_order'])
            if new_quantity > 0:
                new_product = Product.query.filter_by(id=int(product['product_id'])).first()
                if new_product:
                    op = OrderedProducts(quantity=new_quantity)
                    op.product = new_product
                    op.order_id = new_order.id
                    new_order.products.append(op)

        db.session.commit()
        return redirect(url_for("orders"))

    #if not validated return to maker select
    products = Product.query.order_by(Product.maker_id, Product.code)\
        .filter_by(maker_id=int(maker_id),
                   active_flg=True).all()
    formMaker = SelectMakerForm()
    formMaker.maker.choices = [(a.id, a.name) for a in Maker.query.all()]
    return render_template('orders/createOrder.html',
                           title=gettext("Place new order to maker"),
                           formMaker=formMaker,
                           formQuantities=formQuantities,
                           products=products)


@app.route('/order/<int:id>')
@login_required
def order(id):
    order = Order.query.filter_by(id=id).first()
    if order:
        products = order.products
    return render_template('orders/order.html',
                            title=gettext("Order details"),
                            order=order,
                            products=products)


@app.route('/productorders/<int:id>')
@login_required
def productorders(id):
    product = Product.query.filter_by(id=id).first()
    if product:
        #TODO: only active ones!
        orders = product.order_assocs

    return render_template('orders/productorders.html',
                           title=gettext("Orders to maker for product"),
                           product=product,
                           orders=orders)