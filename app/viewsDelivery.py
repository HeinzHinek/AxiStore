# -*- coding: utf-8 -*-

from flask import render_template, flash, redirect, url_for, request, g
from app import app, db
from forms import SelectMakerForm, ProductQuantityForm
from models import Delivery, Product, DeliveredProducts, Maker
from flask_login import login_required
from config import DEFAULT_PER_PAGE
from flask.ext.babel import gettext

@app.route('/deliveries')
@app.route('/deliveries/<int:page>')
@login_required
def deliveries(page=1):
    deliveries = Delivery.query.paginate(page, DEFAULT_PER_PAGE, False)
    return render_template('deliveries/deliveries.html',
                           title=gettext("Deliveries"),
                           deliveries=deliveries)


@app.route('/deliveries/newdelivery', methods=['GET', 'POST'])
@login_required
def newDelivery():
    formMaker = SelectMakerForm()
    formQuantities = ProductQuantityForm()
    products = None
    if formMaker.is_submitted():
        if formMaker.validate_on_submit():

            maker_id = formMaker.maker.data.id
            if not maker_id:
                flash(gettext("Maker not found."))
                return redirect(url_for("deliveries"))

            products = Product.query.order_by(Product.maker_id, Product.code)\
                .filter_by(maker_id=int(maker_id),
                           active_flg=True).all()
            for p in products:
                formQuantities.fields.append_entry()

    return render_template('deliveries/newDelivery.html',
                           title=gettext("New Delivery"),
                           formMaker=formMaker,
                           formQuantities=formQuantities,
                           products=products)


@app.route('/deliveries/receivedelivery', methods=['GET', 'POST'])
@login_required
def receiveDelivery():
    formQuantities = ProductQuantityForm(request.form)
    maker_id = request.form['maker_id']
    if not maker_id:
        flash(gettext("Maker not found."))
        return redirect(url_for("deliveries"))

    if formQuantities.validate_on_submit():

        new_delivery = Delivery()
        #TODO other date than now   new_delivery.created_dt =
        new_delivery.maker_id = maker_id
        new_delivery.user_id = g.user.id
        db.session.add(new_delivery)

        #variable for reporting purposes
        report = {'recipient': g.user.nickname, 'maker': Maker.query.filter_by(id=maker_id).first().name, 'products': [], 'closed_orders': [],
                  'changed_orders': [], 'overreceived_products': False}

        #add received products to new delivery
        form_data = formQuantities.data['fields']
        for product in form_data:
            new_quantity = int(product['qty_order'])
            if new_quantity > 0:
                new_product = Product.query.filter_by(id=int(product['product_id'])).first()
                if new_product:

                    dp = DeliveredProducts(quantity=new_quantity)
                    dp.product = new_product
                    new_delivery.products.append(dp)

                    report_details = {'product': new_product, 'qty': new_quantity, 'over': 0}

                    '''Here we are going to take each order for given product (from oldest),
                    and add delivered quantity and also product stock quantity by subtracting
                    new quantity, one order a time, until new quantity reaches zero.
                    If delivered quantity of given order reaches ordered quantity, then we
                    have to check, whether all other products of that order have been delivered.
                    If so, the order is complete and we'll switch it's active flag to False.'''

                    #create temp qty equal to new quanity that will be substracted until there are orders
                    temp_qty = new_quantity
                    #get ordered products for product from oldest
                    ordered_products = new_product.order_assocs
                    ordered_products.sort(key=lambda x: x.order.created_dt, reverse=False)
                    for op in ordered_products:
                        #count ordered products quantity - qty_delivered = delta qty
                        if op.qty_delivered is None:
                            op.qty_delivered = 0
                        delta_qty = op.quantity - op.qty_delivered

                        if delta_qty <= temp_qty:

                            if new_product.qty_stock is not None:
                                new_product.qty_stock += (op.quantity - op.qty_delivered)

                            op.qty_delivered = op.quantity

                            #if order completely delivered add to report
                            if op.order.active_flg:
                                if op.order.check_completely_delivered():
                                    while True:
                                        if op.request in report['changed_orders']:
                                            report['changed_orders'].remove(op.request)
                                        else:
                                            break
                                    report['closed_orders'].append(op.order)
                                else:
                                    report['changed_orders'].append(op.order)

                            if delta_qty == temp_qty:
                                temp_qty = 0
                                break
                        else:
                            if new_product.qty_stock is not None:
                                new_product.qty_stock += temp_qty

                            op.qty_delivered += temp_qty
                            temp_qty -= op.qty_delivered
                            report['changed_orders'].append(op.order)
                            break

                        temp_qty -= delta_qty

                    if temp_qty > 0:
                        if new_product.qty_stock is not None:
                            new_product.qty_stock += temp_qty

                        report_details['over'] = temp_qty
                        report['overreceived_products'] = True
                    report['products'].append(report_details)

        db.session.commit()

        flash( gettext('New delivery received sucessfully.') )
        print(report)

        return render_template('deliveries/deliveryReport.html',
                           title=gettext("Delivery Report"),
                           report=report)

    #if not validated return to maker select
    products = Product.query.order_by(Product.maker_id, Product.code)\
        .filter_by(maker_id=int(maker_id),
                   active_flg=True).all()
    formMaker = SelectMakerForm()
    return render_template('deliveries/newDelivery.html',
                           title=gettext("New Delivery"),
                           formMaker=formMaker,
                           formQuantities=formQuantities,
                           products=products)


@app.route('/delivery/<int:id>')
@login_required
def delivery(id):
    delivery = Delivery.query.filter_by(id=id).first()
    if delivery:
        products = delivery.products
    return render_template('deliveries/delivery.html',
                            title=gettext("Delivery details"),
                            delivery=delivery,
                            products=products)