# -*- coding: utf-8 -*-

from flask import render_template, redirect, flash, url_for, g
from app import app, db
from forms import SelectCustomerForm, OrderNumberForm, EditDateTimeForm
from models import Request, Product, RequestedProducts, Customer, Maker
from flask_login import login_required
from config import DEFAULT_PER_PAGE, CUSTOMER_TYPES
from flask.ext.babel import gettext
from datetime import *
import flask


@app.route('/requests')
@app.route('/requests/<int:page>')
@login_required
def requests(page=1):
    requests = Request.query\
        .order_by(Request.active_flg.desc())\
        .order_by(Request.created_dt)\
        .paginate(page, DEFAULT_PER_PAGE, False)
    return render_template('requests/requests.html',
                           title=gettext("Orders from Customers"),
                           CUSTOMER_TYPES=CUSTOMER_TYPES,
                           requests=requests)


@app.route('/requests/createRequest', methods=['GET', 'POST'])
@login_required
def createRequest():
    cust = flask.request.args.get('cust')
    if not cust:
        cust = 'cust'
    if cust == 'cust':
        formCustomer = SelectCustomerForm()
        cust_customers = Customer.query.filter_by(customer_type=CUSTOMER_TYPES['TYPE_CUSTOMER']).all()
        cust_customers = [(a.id, a.name) for a in cust_customers]
        cust_customers = [(0, '')] + cust_customers
        formCustomer.customer.choices = cust_customers
    else:
        formCustomer = OrderNumberForm()
    makers = Maker.query.all()
    maker_choices = [(a.id, a.name) for a in makers]
    maker_choices = [(0, '')] + maker_choices
    formCustomer.maker.choices = maker_choices
    if formCustomer.validate_on_submit():
        ids = {}
        for attr in flask.request.form:
            if attr.startswith("req_qty-"):
                key = attr.split('-')[1]
                ids[key] = flask.request.form[attr]
        if ids:
            if cust == 'cust':
                cust_id = int(formCustomer.customer.data)
                if not cust_id:
                    flash(gettext("No customer id."))
                    return redirect(url_for("requests"))
                req_cust = db.session.query(Customer).filter_by(id=cust_id).first()
                if not req_cust:
                    flash(gettext("Customer not found."))
                    return redirect(url_for("requests"))
                if req_cust.customer_type != CUSTOMER_TYPES['TYPE_CUSTOMER']:
                    flash(gettext("Invalid customer!"))
                    return redirect(url_for("requests"))

            elif cust == 'axm':
                order_no = formCustomer.order_no.data
                if not order_no:
                    flash(gettext("No order number."))
                    return redirect(url_for("requests"))
                req_cust = db.session.query(Customer).filter_by(order_no=order_no).first()
                if req_cust:
                    flash(gettext("Order number already exists!"))
                    return redirect(url_for("requests"))
                req_cust = Customer()
                req_cust.customer_type = CUSTOMER_TYPES['TYPE_AXM']
                req_cust.order_no = order_no
                db.session.add(req_cust)
                db.session.commit()
            else:
                flash(gettext("Invalid data received!"))
                return redirect(url_for("requests"))

            new_request = Request()
            new_request.user_id = g.user.id
            new_request.customer_id = req_cust.id
            if formCustomer.datetime.data:
                new_request.created_dt = formCustomer.datetime.data
            else:
                flash("Date and time date of request was entered incorrectly, request saved with current date and time.")

            new_request.active_flg = True
            db.session.add(new_request)
            db.session.commit()

            for id in ids:
                new_product = db.session.query(Product).filter_by(id=id).first()
                if not new_product:
                    flash(gettext("Product not found."))
                    return redirect(url_for("requests"))
                rp = RequestedProducts(quantity=int(ids[id]))
                rp.product = new_product
                rp.request_id = new_request.id
                new_request.products.append(rp)

            db.session.commit()
            flash(gettext("Order created successfully."))
            return redirect(url_for("requests"))

        else:
            flash(gettext("Order data not sent."))
            return redirect(url_for("requests"))

    formCustomer.datetime.data = datetime.now()
    return render_template('requests/createRequest.html',
                           title=gettext("Accept order from customer"),
                           formCustomer=formCustomer,
                           custType=cust)


@app.route('/request/<int:id>', methods=['GET', 'POST'])
@login_required
def request_detail(id):
    req = Request.query.filter_by(id=id).first()
    form = EditDateTimeForm()
    if req:
        products = req.products

    if form.validate_on_submit():
        if form.datetime.data:
            req.created_dt = form.datetime.data
            db.session.add(req)
            db.session.commit()
            flash(gettext("Date and time of request was successfully changed."))

    form.datetime.data = req.created_dt
    return render_template('requests/request.html',
                            title=gettext("Order from customer details"),
                            req=req,
                            form=form,
                            CUSTOMER_TYPES=CUSTOMER_TYPES,
                            products=products)


@app.route('/productrequests/<int:id>')
@login_required
def productrequests(id):
    product = Product.query.filter_by(id=id, active_flg=1).first()
    requests = []
    if product:
        all_requests = product.request_assocs
    for r in all_requests:
        if r.request.active_flg:
            if r.quantity - r.qty_supplied > 0:
                requests.append(r)

    return render_template('requests/productrequests.html',
                           title=gettext("Orders from customers for product"),
                           product=product,
                           CUSTOMER_TYPES=CUSTOMER_TYPES,
                           requests=requests)