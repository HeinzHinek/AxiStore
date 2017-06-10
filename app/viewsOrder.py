# -*- coding: utf-8 -*-

from flask import render_template, redirect, flash, url_for, request, g, session
from app import app, db
from forms import SelectMakerForm, ProductQuantityForm, EditDateTimeForm, EditQtyStockForm, SimpleSubmitForm, EditOrderForm
from models import Order, Product, OrderedProducts, Maker
from mailer import send_order_mail_to_maker
from xls import CreateXls
from permissions import login_required
from config import DEFAULT_PER_PAGE
from flask_babel import gettext
import flask, re


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

    order_items_ids = request.args.get('order_items_ids')
    maker_to_order = request.args.get('maker_to_order')
    # redirected from order management screen
    if order_items_ids and maker_to_order:
        products = Product.query.order_by(Product.code)\
            .filter_by(maker_id=int(maker_to_order),
                       active_flg=True).all()
        for p in products:
            qty_to_order = 0
            ids = order_items_ids.split(',')
            if str(p.id) in ids:
                qty_to_order = p.min_stock_limit - p.net_stock
            entry = formQuantities.fields.append_entry({'qty_order': qty_to_order})

    elif formMaker.is_submitted():
        if formMaker.validate_on_submit():

            maker_id = formMaker.maker.data
            if not maker_id:
                flash(gettext("Maker not found."))
                return redirect(url_for("orders"))

            products = Product.query.order_by(Product.code)\
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

        # Create order sheet xls
        xls = CreateXls()
        maker = Maker.query.filter_by(id=maker_id).first()
        maker_name = maker.name
        data = []
        for item in form_data:
            if item['qty_order'] < 1:
                continue
            product = Product.query.filter_by(id=item['product_id']).first()
            if product:
                data.append({'product_code': product.code, 'product_maker_code': product.maker_code,\
                             'product_name': product.desc_CS, 'quantity': item['qty_order']})
        order_xls = xls.order_sheet(maker_name, data)
        match = re.search(r"[^a-zA-Z](ordersheet)[^a-zA-Z]", order_xls)
        pos = match.start(1)
        filename = order_xls[pos:]

        flash(gettext('New order to maker was successfully created.'))

        return render_template('orders/ordersheet.html',
                               title=gettext("Order Sheet Management"),
                               ordersheet_file=filename,
                               maker=maker,
                               mail_sent=False)

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


@app.route('/order/<int:id>', methods=['GET', 'POST'])
@login_required
def order(id):
    order = Order.query.filter_by(id=id).first()
    if not order:
        flash(gettext('Data not found.'))
        return redirect(url_for('orders'))
    form = EditDateTimeForm()
    if order:
        products = order.products

    if form.validate_on_submit():
        if form.datetime.data:
            order.created_dt = form.datetime.data
            db.session.add(order)
            db.session.commit()
            flash(gettext("Date and time of order was successfully changed."))

    form.datetime.data = order.created_dt
    return render_template('orders/order.html',
                            title=gettext("Order details"),
                            order=order,
                            form=form,
                            products=products)


@app.route('/productorders/<int:id>')
@login_required
def productorders(id):
    product = Product.query.filter_by(id=id).first()
    if product:
        orders = OrderedProducts.query.filter_by(product_id=product.id)\
            .filter(OrderedProducts.quantity - OrderedProducts.qty_delivered > 0)\
            .join(Product).filter(Product.active_flg == True)\
            .join(Order).order_by(Order.created_dt)\
            .all()
        #orders = product.order_assocs

    return render_template('orders/productorders.html',
                           title=gettext("Orders to maker for product"),
                           product=product,
                           orders=orders)


@app.route('/ordermanagement', methods=['GET', 'POST'])
@login_required
def ordermanagement():

    makers = Maker.query.all()
    curr_maker_id = session['maker_id'] if session['maker_id'] else Maker.query.first().id
    products = Product.query.filter_by(active_flg=True).filter_by(maker_id=curr_maker_id).all()
    form_edit_qty = EditQtyStockForm()

    if form_edit_qty.is_submitted():

        # sumbitting products to order
        if 'checked-items-ids-hid' in request.form:
            order_items_ids = request.form['checked-items-ids-hid']
            return redirect(url_for('createOrder', maker_to_order=curr_maker_id, order_items_ids=order_items_ids))

        #submitting min. stock quantities
        if form_edit_qty.validate():
            qty = form_edit_qty.qty_stock.data
            id_text = request.form['product_id']
            ids = id_text.split(',')

            if ((qty and ids) or (qty == 0 and ids)) and ids != ['']:
                for curr_id in ids:
                    product = Product.query.filter_by(id=int(curr_id)).first()
                    if product:
                        product.min_stock_limit = qty
                        db.session.add(product)
                db.session.commit()
                flash(gettext('Minimum stock limit successfully updated.'))
            else:
                flash(gettext('Input value error.'))
        else:
            flash(gettext('Input value error.'))
        return redirect(url_for("ordermanagement"))

    return render_template('orders/ordermanagement.html',
                           title=gettext("Order management"),
                           makers=makers,
                           curr_maker_id=curr_maker_id,
                           products=products,
                           form_edit_qty=form_edit_qty)


@app.route('/order_mail_to_maker/<path:filename>/maker/<int:maker_id>')
@login_required
def order_mail_to_maker(filename, maker_id):
    maker = Maker.query.filter_by(id=maker_id).first()
    if maker:
        send_order_mail_to_maker(filename, maker.email)
        flash(gettext("Email to maker sent succesfully."))
    else:
        flash(gettext("Maker not found."))
    return render_template('orders/ordersheet.html',
                           title=gettext("Order Sheet Management"),
                           ordersheet_file=filename,
                           maker=maker,
                           mail_sent=True)


@app.route('/editorder/<int:id>', methods=['GET', 'POST'])
@login_required
def editorder(id):
    order = Order.query.get(id)
    if not order:
        flash(gettext('Data not found!'))
        return redirect(url_for('orders'))
    maker = Maker.query.get(order.maker_id)
    if not maker:
        flash(gettext('Maker data not found!'))
        return redirect(url_for('orders'))
    products = order.products.all()
    form = EditOrderForm()

    if form.validate_on_submit():

        ordered_product_id = flask.request.form['ordered_product_id']
        if not ordered_product_id:
            flash(gettext('Product data not found!'))
            return redirect(url_for('editorder', id=order.id))

        op = OrderedProducts.query\
            .filter_by(order_id=order.id)\
            .filter_by(product_id=int(ordered_product_id))\
            .first()
        if not op:
            flash(gettext('Product data not found!'))
            return redirect(url_for('editorder', id=order.id))

        # Are we deleting this ordered product completely?
        delete_str = flask.request.form['delete_ordered_product']
        if delete_str == 'true':
            if op.qty_delivered and op.qty_delivered > 0:
                flash(gettext('Cannot delete order that has been already delivered! Delete delivery item first.'))
                return redirect(url_for('editorder', id=order.id))

            db.session.delete(op)
            db.session.commit()

            # Check whether this order is still active
            if order.check_completely_delivered():
                db.session.add(order)
                db.session.commit()

            flash(gettext('Ordered product sucessfully deleted.'))
            return redirect(url_for('editorder', id=order.id))

        # We are not deleting, only changing ordered quantity
        new_order_qty = form.qty_ordered.data
        if not new_order_qty or new_order_qty < 1 or new_order_qty > 1000000:
            flash(gettext('Ordered quantity submited incorrectly!'))
            return redirect(url_for('editorder', id=order.id))
        if new_order_qty == op.quantity:
            flash(gettext('Submited quantity is the same as the current value. Nothing to change.'))
            return redirect(url_for('editorder', id=order.id))

        # Submited value seems to be ok here
        op.quantity = new_order_qty
        db.session.add(op)

        # Check whether this request is still active
        if not order.check_completely_delivered():
            order.active_flg = True
        db.session.add(order)

        db.session.commit()

        flash(gettext('Ordered quantity succesfully changed.'))
        return redirect(url_for('editorder', id=order.id))

    return render_template('orders/editorder.html',
                           title=gettext("Edit order to maker"),
                           order=order,
                           products=products,
                           maker=maker,
                           form=form)


@app.route('/cancelorder/<int:id>', methods=['GET', 'POST'])
@login_required
def cancelorder(id):
    order = Order.query.get(id)
    if not order:
        flash(gettext('Order not found!'))
        return redirect('requests')
    products = order.products
    form = SimpleSubmitForm()

    if form.validate_on_submit():
        order = Order.query.get(int(flask.request.form['order_id']))
        products = order.products
        for op in products:
            db.session.delete(op)
            pass
        db.session.delete(order)
        db.session.commit()
        flash('Order was sucessfully cancelled and deleted.')
        return redirect('orders')

    return render_template('orders/cancelorder.html',
                           title=gettext("Cancel order to maker"),
                           order=order,
                           products=products,
                           form=form)