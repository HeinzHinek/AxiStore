# -*- coding: utf-8 -*-

from flask import render_template, flash, redirect, url_for, request, session, g
from app import app, db
from forms import SelectCustomerForm, SelectOrderNumberFormAxm, EditDateTimeForm, SimpleSubmitForm
from models import Supply, Product, Customer, SuppliedProducts, Request, RequestedProducts
from flask_login import login_required
from sqlalchemy import desc
from config import DEFAULT_PER_PAGE, CUSTOMER_TYPES
from flask.ext.babel import gettext
from xls import CreateXls
from imageHelper import getImgUrls
import datetime, re
import flask

@app.route('/supplies')
@app.route('/supplies/<int:page>')
@login_required
def supplies(page=1):
    supplies = Supply.query\
        .order_by(desc(Supply.created_dt))\
        .paginate(page, DEFAULT_PER_PAGE, False)
    return render_template('supplies/supplies.html',
                           title=gettext("Supplies"),
                           CUSTOMER_TYPES=CUSTOMER_TYPES,
                           supplies=supplies)


@app.route('/supplies/newsupply', methods=['GET', 'POST'])
@login_required
def newSupply():
    cust = flask.request.args.get('cust')
    if not cust:
        cust = 'cust'
    if cust == 'cust':
        formCustomer = SelectCustomerForm()
        cust_customers = Customer.query.filter_by(customer_type=CUSTOMER_TYPES['TYPE_CUSTOMER']).all()
        cust_customers = [(a.id, a.name) for a in cust_customers]
        cust_customers = [(0, '')] + cust_customers
        formCustomer.customer.choices = cust_customers
    elif cust == 'axm':
        formCustomer = SelectOrderNumberFormAxm()
        all_orders = Customer.query.filter_by(customer_type=CUSTOMER_TYPES['TYPE_AXM']).all()
        orders = []
        for o in all_orders:
            r = Request.query.filter_by(customer_id=o.id).first()
            if r and r.active_flg == True:
                orders.append(o)
        formCustomer.order.choices = [(a.id, a.order_no) for a in orders]
        formCustomer.order.choices.insert(0, ('', ''))

    if formCustomer.is_submitted():
        if request.form['custType']:
            session['new_supply'] = None
            if request.form['custType'] == 'cust':
                session['new_supply'] = [('custType', request.form['custType']), ('cust_id', request.form['customer'])]
            elif request.form['custType'] == 'axm':
                session['new_supply'] = [('custType', request.form['custType']), ('cust_id', request.form['order'])]
            if session['new_supply']:
                return redirect(url_for("supplyProducts"))

    return render_template('supplies/newSupply.html',
                           title=gettext("New Supply"),
                           custType=cust,
                           formCustomer=formCustomer)

@app.route('/supplies/supplyproducts', methods=['GET', 'POST'])
@login_required
def supplyProducts():

    # Redirected from unsuppliedproducts?
    cust_id = request.args.get('cust_id')
    data_to_populate = request.args.get('deliver_items_data')

    # Yes, redirected from unsuppliedproducts
    if cust_id and data_to_populate:
        custType = 'cust'

    # No, redirected from newsupply
    else:
        if not session['new_supply']:
            flash(gettext('No customer data!'))
            return redirect(url_for("supplies"))
        custType = session['new_supply'][0][1]
        cust_id = session['new_supply'][1][1]

    cust = Customer.query.filter_by(id=cust_id).first()

    if not cust:
        flash(gettext('Customer not found!'))
        return redirect(url_for("supplies"))

    if request.method == 'POST':
        ids = {}
        for attr in flask.request.form:
            if attr.startswith("supp_qty-"):
                key = attr.split('-')[1]
                if flask.request.form[attr] != '0':
                    ids[key] = flask.request.form[attr]
        if not ids:
            flash(gettext('No product quantities!'))
            return redirect(url_for("supplies"))

        last_supply = Supply.query.filter_by(customer_id=cust_id).order_by(desc(Supply.created_dt)).first()
        new_supply = Supply()
        #TODO other date than now   new_supply.created_dt =
        new_supply.customer_id = cust_id
        new_supply.user_id = g.user.id
        db.session.add(new_supply)
        db.session.commit()

        #variable for reporting purposes
        report = {'sender': g.user.nickname, 'customer': cust, 'date': new_supply.created_dt, 'order_no': cust.order_no, 'products': [],
                  'closed_requests': [], 'changed_requests': [], 'oversent_requests': False}

        for id in ids:
            new_quantity = int(ids[id])
            if new_quantity > 0:
                new_product = Product.query.filter_by(id=int(id)).first()
                if new_product:

                    rp = SuppliedProducts(quantity=new_quantity)
                    rp.product = new_product
                    rp.supply_id = new_supply.id
                    new_supply.products.append(rp)

                    report_details = {'product': new_product, 'qty': new_quantity, 'over': 0}

                    temp_qty = new_quantity
                    #get requested products from current customer for product from oldest
                    all_products = new_product.request_assocs
                    requested_products = []
                    for p in all_products:
                       if p.request.customer_id == cust.id:
                           requested_products.append(p)
                    if not requested_products:
                            flash(gettext('No requested products!'))
                            return redirect(url_for("supplies"))
                    requested_products.sort(key=lambda x: x.request.created_dt, reverse=False)

                    for rp in requested_products:
                        #count requested products quantity - qty_supplied = delta qty
                        if rp.qty_supplied is None:
                            rp.qty_supplied = 0
                        delta_qty = rp.quantity - rp.qty_supplied

                        if delta_qty <= temp_qty:

                            if new_product.qty_stock is not None:
                                new_product.qty_stock -= (rp.quantity - rp.qty_supplied)

                            rp.qty_supplied = rp.quantity

                            #if request completely supplied add to report
                            if rp.request.active_flg:
                                if rp.request.check_completely_supplied():
                                    while True:
                                        if rp.request in report['changed_requests']:
                                            report['changed_requests'].remove(rp.request)
                                        else:
                                            break
                                    report['closed_requests'].append(rp.request)
                                else:
                                    if rp.request not in report['changed_requests']:
                                        report['changed_requests'].append(rp.request)

                            if delta_qty == temp_qty:
                                temp_qty = 0
                                break

                        else:
                            if new_product.qty_stock is not None:
                                new_product.qty_stock -= temp_qty

                            rp.qty_supplied += temp_qty
                            temp_qty -= rp.qty_supplied
                            if rp.request not in report['changed_requests']:
                                report['changed_requests'].append(rp.request)
                            break

                        temp_qty -= delta_qty

                    if temp_qty > 0:
                        if new_product.qty_stock is not None:
                            new_product.qty_stock -= temp_qty

                        report_details['over'] = temp_qty
                        report['oversent_requests'] = True
                    report['products'].append(report_details)

        #set new nohinsho number if custType = customer
        if cust.customer_type == CUSTOMER_TYPES['TYPE_CUSTOMER']:
            if not cust.order_no:
                cust.order_no = 1
            else:
                if last_supply:
                    date_old = datetime.datetime(*map(int, re.split('[^\d]', str(last_supply.created_dt))[:-1]))
                    date_new = datetime.datetime(*map(int, re.split('[^\d]', str(new_supply.created_dt))[:-1]))
                    if date_old.year == date_new.year:
                        if date_old.month == date_new.month:
                            cust.order_no += 1
                        else:
                            cust.order_no += 1
                else:
                    cust.order_no = 1
            db.session.add(cust)

    #FINAL COMMIT
        db.session.commit()

        flash(gettext('New supply sent sucessfully.'))
        print report

        #prepare data for xls
        product_ids=[]
        for p in report['products']:
            product_ids.append([p['product'].id, p['qty']])
        session['new_supply_data'] = {'date': report['date'], 'customer': cust.id, 'products': product_ids}

        return render_template('supplies/supplyReport.html',
                           title=gettext("Supply Report"),
                           custType=custType,
                           report=report)


    requests = cust.requests.all()
    products = []
    for r in requests:
        for rp in r.products:
            if rp.product not in products:
                rp.product.cust_request_qty = rp.product.customer_request_qty(cust.id)
                if rp.product.cust_request_qty > 0:
                    products.append(rp.product)
    products = sorted(products, key=lambda k: (k.maker_id, k.code))
    for p in products:
        urls = getImgUrls(p.id)
        if urls:
            p.img_url = urls[0]
    return render_template('supplies/supplyProducts.html',
                           custType=custType,
                           customer=cust,
                           products=products,
                           data_to_populate=data_to_populate)


@app.route('/supply/<int:id>', methods=['GET', 'POST'])
@login_required
def supply(id):
    supply = Supply.query.filter_by(id=id).first()
    form = EditDateTimeForm()
    if supply:
        products = supply.products

    if form.validate_on_submit():
        if form.datetime.data:
            supply.created_dt = form.datetime.data
            db.session.add(supply)
            db.session.commit()
            flash(gettext("Date and time of supply was successfully changed."))

    form.datetime.data = supply.created_dt
    return render_template('supplies/supply.html',
                            title=gettext("Supply details"),
                            supply=supply,
                            form=form,
                            CUSTOMER_TYPES=CUSTOMER_TYPES,
                            products=products)


@app.route('/supplies/createnohinsho')
@login_required
def createNohinsho():
    xlsdata = session['new_supply_data']
    #session['new_supply_data'] = None
    date = xlsdata['date']
    customer = Customer.query.filter_by(id=xlsdata['customer']).first()
    products = []
    pr = xlsdata['products']
    if not pr:
        flash(gettext('No product data!'))
        return redirect(url_for("supplies"))
    for p in pr:
        products.append({'product': Product.query.filter_by(id=p[0]).first(), 'qty': p[1]})
    products = sorted(products, key=lambda k: (k['product'].maker_id, k['product'].code))

    if xlsdata:
        xls = CreateXls()
        nohinsho = xls.nohinsho(date, customer, products)
        match = re.search(r"[^a-zA-Z](nohinsho)[^a-zA-Z]", nohinsho)
        pos = match.start(1)
        filename = nohinsho[pos:]
        return redirect(url_for('download_file', filename=filename))

    flash(gettext('Invalid data received.'))
    return redirect(url_for("supplies"))


@app.route('/supplies/unsuppliedproducts', methods=['GET', 'POST'])
@app.route('/supplies/unsuppliedproducts/<int:id>', methods=['GET', 'POST'])
@login_required
def unsuppliedProducts(id=None):

    form = SimpleSubmitForm()

    if form.is_submitted():
        if 'checked-items-ids-hid' in request.form:
            cust_id = request.form['curr-customer-id-hid']
            data = request.form['checked-items-ids-hid']
            return redirect(url_for('supplyProducts', cust_id=cust_id, deliver_items_data=data))

    unsupplied_requests = Request.query.filter_by(active_flg=True).all()
    customer_ids = []
    for ur in unsupplied_requests:
        if ur.customer_id not in customer_ids:
            customer_ids.append(ur.customer_id)
    unsupplied_customers = db.session.query(Customer)\
        .filter(Customer.id.in_(customer_ids)).order_by(Customer.id)\
        .all()

    for uc in unsupplied_customers:
        uc.unsupplied_products_count = 0
        for ur in unsupplied_requests:
            if ur.customer_id == uc.id:
                for product in ur.products:
                    if product.quantity > product.qty_supplied:
                        uc.unsupplied_products_count += (product.quantity - product.qty_supplied)

    if not id:
        id = unsupplied_customers[0].id
    cust = Customer.query.filter_by(id=id).first()
    requests = cust.requests.all()
    products = []
    for r in requests:
        for rp in r.products:
            if rp.product not in products:
                rp.product.cust_request_qty = rp.product.customer_request_qty(cust.id)
                if rp.product.cust_request_qty > 0:
                    products.append(rp.product)

    # Load number of products reserved earlier by other customers
    for p in products:
        stock = p.qty_stock
        cust_earliest_request_dt = RequestedProducts.query.filter_by(product_id=p.id)\
            .filter(RequestedProducts.quantity - RequestedProducts.qty_supplied > 0)\
            .join(Request).order_by(Request.created_dt)\
            .join(Customer).filter(Customer.id == cust.id)\
            .first().request.created_dt
        earlier_requests = RequestedProducts.query.filter_by(product_id=p.id)\
            .filter(RequestedProducts.quantity - RequestedProducts.qty_supplied > 0)\
            .join(Request).filter(Request.created_dt < cust_earliest_request_dt)\
            .join(Customer).filter(Customer.id != cust.id)\
            .all()
        p.reserved_earlier_qty = 0
        for er in earlier_requests:
            p.reserved_earlier_qty += er.quantity - er.qty_supplied

        temp = p.qty_stock - p.reserved_earlier_qty
        if temp <= 0:
            p.deliverable_qty = 0
        elif temp > p.cust_request_qty:
            p.deliverable_qty = p.cust_request_qty
        else:
            p.deliverable_qty = temp

    products = sorted(products, key=lambda k: (k.maker_id, k.code))
    for p in products:
        urls = getImgUrls(p.id)
        if urls:
            p.img_url = urls[0]
    return render_template('supplies/unsuppliedproducts.html',
                           title=gettext("Unsupplied products"),
                           form=form,
                           unsupplied_customers=unsupplied_customers,
                           products=products,
                           CUSTOMER_TYPES=CUSTOMER_TYPES,
                           curr_id=id)