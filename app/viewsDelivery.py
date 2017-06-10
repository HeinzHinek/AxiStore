# -*- coding: utf-8 -*-

from flask import render_template, flash, redirect, url_for, request, g
from app import app, db
from forms import SelectMakerForm, ProductQuantityForm, EditDateTimeForm, EditDeliveryForm
from models import Delivery, Product, DeliveredProducts, Maker, Order, OrderedProducts
from permissions import login_required
from config import DEFAULT_PER_PAGE
from imageHelper import getImgUrls
from mailer import send_delivery_notification_to_customers
from flask_babel import gettext
import flask

@app.route('/deliveries')
@app.route('/deliveries/<int:page>')
@login_required
def deliveries(page=1):
    deliveries = Delivery.query\
        .order_by(Delivery.created_dt.desc())\
        .paginate(page, DEFAULT_PER_PAGE, False)
    return render_template('deliveries/deliveries.html',
                           title=gettext("Deliveries"),
                           deliveries=deliveries)


@app.route('/deliveries/newdelivery', methods=['GET', 'POST'])
@login_required
def newDelivery():
    formMaker = SelectMakerForm()
    formMaker.maker.choices = [(a.id, a.name) for a in Maker.query.all()]
    formQuantities = ProductQuantityForm()
    products = None
    if formMaker.is_submitted():
        if formMaker.validate_on_submit():

            maker_id = formMaker.maker.data
            if not maker_id:
                flash(gettext("Maker not found."))
                return redirect(url_for("deliveries"))

            products = Product.query.order_by(Product.maker_id, Product.code)\
                .filter_by(maker_id=int(maker_id),
                           active_flg=True).all()
            for p in products:
                formQuantities.fields.append_entry()
                urls = getImgUrls(p.id)
                if urls:
                    p.img_url = urls[0]

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
        db.session.commit()

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
                    dp.delivery_id = new_delivery.id
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
                                        if op.order in report['changed_orders']:
                                            report['changed_orders'].remove(op.order)
                                        else:
                                            break
                                    report['closed_orders'].append(op.order)
                                else:
                                    if op.order not in report['changed_orders']:
                                        report['changed_orders'].append(op.order)

                            if delta_qty == temp_qty:
                                temp_qty = 0
                                break
                        else:
                            if new_product.qty_stock is not None:
                                new_product.qty_stock += temp_qty

                            op.qty_delivered += temp_qty
                            temp_qty -= op.qty_delivered
                            if op.order not in report['changed_orders']:
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

        # Send e-mail to customers with delivered products notification
        send_delivery_notification_to_customers(report['maker'], report['products'])

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
    formMaker.maker.choices = [(a.id, a.name) for a in Maker.query.all()]
    return render_template('deliveries/newDelivery.html',
                           title=gettext("New Delivery"),
                           formMaker=formMaker,
                           formQuantities=formQuantities,
                           products=products)


@app.route('/delivery/<int:id>', methods=['GET', 'POST'])
@login_required
def delivery(id):
    delivery = Delivery.query.filter_by(id=id).first()
    if not delivery:
        flash(gettext('Data not found.'))
        return redirect(url_for('deliveries'))
    form = EditDateTimeForm()
    if delivery:
        products = delivery.products

    if form.validate_on_submit():
        if form.datetime.data:
            delivery.created_dt = form.datetime.data
            db.session.add(delivery)
            db.session.commit()
            flash(gettext("Date and time of delivery was successfully changed."))

    form.datetime.data = delivery.created_dt
    return render_template('deliveries/delivery.html',
                            title=gettext("Delivery details"),
                            delivery=delivery,
                            form=form,
                            products=products)

@app.route('/editdelivery/<int:id>', methods=['GET', 'POST'])
@login_required
def editdelivery(id):

    delivery = Delivery.query.get(id)
    if not delivery:
        flash(gettext('Delivery data not found!'))
        return redirect(url_for('deliveries'))
    products = delivery.products.all()

    form = EditDeliveryForm()

    if form.validate_on_submit():

        delivery_id = flask.request.form['delivery_id']

        # Are we deleting an empty delivery?
        delete_whole_str = None
        if 'delete_whole_delivery' in flask.request.form:
            delete_whole_str = flask.request.form['delete_whole_delivery']
        if delete_whole_str and delete_whole_str == 'true':
            delivery = Delivery.query.get(int(delivery_id))
            if not delivery:
                flash(gettext('Delivery data not found!'))
                return redirect(url_for('deliveries'))
            dp = delivery.products.all()
            if dp and len(dp) > 0:
                flash(gettext('Delivered products have to be deleted first!'))
                return redirect(url_for('deliveries'))
            db.session.delete(delivery)
            db.session.commit()
            flash(gettext('Delivery data sucessfully deleted.'))
            return redirect(url_for('deliveries'))

        delivered_product_id = flask.request.form['delivered_product_id']

        # Are we deleting this delivered product completely?
        delete_str = flask.request.form['delete_delivered_product']
        if delete_str == 'true':
            delete_flg = True
            new_delivery_qty = 0
        else:
            delete_flg = False
            new_delivery_qty = form.qty_delivered.data

        if delivery_id and delivered_product_id and new_delivery_qty is not None:

            delivered_product_id = int(delivered_product_id)

            delivered_products = DeliveredProducts.query\
                .filter_by(product_id=delivered_product_id)\
                .filter_by(delivery_id=delivery_id)\
                .all()
            if delivered_products and len(delivered_products) == 1:
                delivered_product = delivered_products[0]
            else:
                flash(gettext('Delivery data are corrupted! Cannot edit delivery quantity.'))
                return redirect(url_for('editdelivery', id=delivery_id))

            if delete_flg:
                qty_difference = delivered_product.quantity
            else:
                qty_difference = delivered_product.quantity - new_delivery_qty
                if qty_difference < 1:
                    flash(gettext('Delivery quantity submited incorrectly!'))
                    return redirect(url_for('editdelivery', id=delivery_id))

            # Subtract the quantity difference from stock
            if form.subtract_qty_from_stock.data:
                stock_product = Product.query.get(delivered_product.product_id)
                if not stock_product:
                    flash(gettext('Product id not found!'))
                    return redirect(url_for('editdelivery', id=delivery_id))
                stock_product.qty_stock -= qty_difference
                db.session.add(stock_product)

            # Add the quantity difference to ordered products
            if form.add_qty_to_orders.data:
                maker = Maker.query.get(Delivery.query.get(delivery_id).maker_id)
                if not maker:
                    flash(gettext('Maker data are corrupted! Cannot edit supply quantity.'))
                    return redirect(url_for('editdelivery', id=delivery_id))
                orders = Order.query\
                    .filter_by(maker_id=maker.id)\
                    .join(OrderedProducts).filter(OrderedProducts.product_id == delivered_product_id)\
                    .order_by(Order.created_dt.desc()).all()

                # Find all orders with this product id from newest, each time subtract delivered quantity till zero,
                # if it goes over, go to next order. Make inactive order active if needed.
                qty_to_subtract = qty_difference
                for o in orders:
                    ops = o.products.all()
                    this_op = None
                    for op in ops:
                        if op.product_id == delivered_product_id:
                            this_op = op
                            break
                    if not this_op:
                        continue

                    # Case1: This order has MORE or EQUAL AMOUNT of qty_delivered than remaining qty_to_subtract
                    # -> subtract qty_to_subtract from qty_delivered and break -> we are done.
                    if this_op.qty_delivered >= qty_to_subtract:
                        this_op.qty_delivered -= qty_to_subtract
                        db.session.add(op)
                        if not o.active_flg:
                            o.active_flg = True
                            db.session.add(o)
                        break
                    # Case2: This order has LESS qty_delivered than remaining qty_to_subtract
                    # -> subtract qty_delivered from qty_to_subtract, set qty_delivered to 0 and go to next order.
                    else:
                        qty_to_subtract -= this_op.qty_delivered
                        this_op.qty_delivered = 0
                        db.session.add(op)
                        if not o.active_flg:
                            o.active_flg = True
                            db.session.add(o)

            # And finally edit the delivered quantity for this product or delete if delete_flg
            if delete_flg:
                db.session.delete(delivered_product)
            else:
                if delivered_product.quantity > new_delivery_qty:
                    delivered_product.quantity = new_delivery_qty
                    db.session.add(delivered_product)

            # FINAL COMMIT
            db.session.commit()

            flash(gettext('Delivered quantity succesfully changed.'))
            return redirect(url_for('editdelivery', id=delivery_id))

    return render_template('deliveries/editdelivery.html',
                            title=gettext("Edit delivery"),
                            delivery=delivery,
                            products=products,
                            form=form)