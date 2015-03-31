# -*- coding: utf-8 -*-

from flask import render_template, flash, redirect, url_for, request
from app import app, db
from forms import AddCustomerForm
from models import Customer, Product, Request, RequestedProducts, Supply, SuppliedProducts
from flask_login import login_required
from config import DEFAULT_PER_PAGE, CUSTOMER_TYPES, BASE_SHARE_FROM_RECOMMENDED
from flask.ext.babel import gettext
import re, datetime


@app.route('/customers')
@app.route('/customers/<int:page>')
@login_required
def customers(page=1):
    customers = Customer.query.filter_by(customer_type=CUSTOMER_TYPES['TYPE_CUSTOMER']).paginate(page, DEFAULT_PER_PAGE, False)
    return render_template('settings/customers.html',
                           title=gettext("Customers"),
                           customers=customers)


@app.route('/addcustomer', methods=['GET', 'POST'])
@login_required
def addCustomer():
    form = AddCustomerForm()

    form.recommender.choices = [(0, '')]
    poss_customers = Customer.query\
        .filter(Customer.customer_type == CUSTOMER_TYPES['TYPE_CUSTOMER']).all()
    for cust in poss_customers:
        form.recommender.choices.append((cust.id, cust.name))

    if form.validate_on_submit():
        customer = Customer()

        customer.name = form.name.data
        customer.email = form.email.data
        customer.base_discount = int(form.base_discount.data)/100.0

        if form.recommender.data and form.recommender.data > 0:
                customer.recommender_id = form.recommender.data

        customer.company_name = form.company_name.data
        if form.post_code1.data and form.post_code2.data:
            customer.post_code = int(str(form.post_code1.data) + str(form.post_code2.data))
        else:
            customer.post_code = None
        customer.address1 = form.address1.data
        customer.address2 = form.address2.data
        customer.address3 = form.address3.data

        db.session.add(customer)
        db.session.commit()
        flash(gettext("New customer successfully added."))
        return redirect(url_for("customers"))
    return render_template('settings/addCustomer.html',
                           title=gettext("Add New Customer"),
                           form=form)


@app.route('/editcustomer/<int:id>', methods=['GET', 'POST'])
@login_required
def editCustomer(id=0):
    customer = Customer.query.filter_by(id=id).first()
    if customer == None:
        flash(gettext('Customer not found.'))
        return redirect(url_for('customers'))
    form = AddCustomerForm(obj=customer)

    form.recommender.choices = [(0, '')]
    poss_customers = Customer.query\
        .filter(Customer.customer_type == CUSTOMER_TYPES['TYPE_CUSTOMER'])\
        .filter(Customer.id != customer.id).all()
    for cust in poss_customers:
        form.recommender.choices.append((cust.id, cust.name))

    if form.is_submitted():
        #delete customer
        if 'delete' in request.form:
            #db.session.delete(customer)
            #db.session.commit()
            flash(gettext('This operation is not allowed at the moment.'))
            return redirect(url_for("customers"))

        if form.validate():
            #update customer
            customer.name = form.name.data
            customer.email = form.email.data
            customer.base_discount = int(form.base_discount.data)/100.0
            nohinsho_letter = form.next_nohinsho_letter.data

            if nohinsho_letter and len(nohinsho_letter) == 1 and re.match("^[A-Z]+$", nohinsho_letter):
                customer.order_no = ord(nohinsho_letter) - 65

            if form.recommender.data and form.recommender.data > 0:
                customer.recommender_id = form.recommender.data
            else:
                customer.recommender_id = None

            customer.company_name = form.company_name.data
            if form.post_code1.data and form.post_code2.data:
                customer.post_code = int(str(form.post_code1.data) + str(form.post_code2.data))
            else:
                customer.post_code = None
            customer.address1 = form.address1.data
            customer.address2 = form.address2.data
            customer.address3 = form.address3.data

            db.session.add(customer)
            db.session.commit()
            flash(gettext("Customer successfully changed."))
            return redirect(url_for("customers"))

    form.base_discount.data = int(customer.base_discount*100) if customer.base_discount else 0
    if customer.order_no:
        form.next_nohinsho_letter.data = chr(customer.order_no + 65)
    else:
        form.next_nohinsho_letter.data = 'A'
    selected = customer.recommender_id if customer.recommender_id else 0
    if customer.post_code:
        post_code = str(customer.post_code)
    else:
        post_code = ''
    form.post_code1.data = post_code[:3]
    form.post_code2.data = post_code[3:]

    return render_template('settings/editCustomer.html',
                           title=gettext("Edit Customer"),
                           customer=customer,
                           selected=selected,
                           form=form)


@app.route('/settings/recommendedshares')
@app.route('/settings/recommendedshares/<int:id>')
@login_required
def recommendedshares(id=None):

    customers_with_recommended = Customer.query.filter(Customer.recommended_customers.any()).all()
    if customers_with_recommended:
        if not id:
            curr_id = customers_with_recommended[0].id
        else:
            curr_id = id
    else:
        curr_id = None

    curr_year = request.args.get('curr_year')
    curr_month = request.args.get('curr_month')

    now = datetime.datetime.utcnow() - datetime.timedelta(hours=9)
    if not curr_year:
        curr_year = now.year
    else:
        curr_year = int(curr_year)
    if not curr_month:
        curr_month = now.month
    else:
        curr_month = int(curr_month)
    curr_year_end = curr_year
    curr_month_end = curr_month + 1
    if curr_month == 12:
        curr_year_end += 1
        curr_month_end = 1

    recommended = []
    sum_request_values = 0
    sum_supply_values = 0
    if customers_with_recommended:
        recommended = next((x for x in customers_with_recommended if x.id == curr_id), None).recommended_customers
        start_dt = datetime.datetime(curr_year, curr_month, 1, 0, 0, 0) - datetime.timedelta(hours=9)  # Japanese timezone
        end_dt = datetime.datetime(curr_year_end, curr_month_end, 1, 0, 0, 0) - datetime.timedelta(hours=9)  # Japanese timezone
        for cust in recommended:
            cust.requested_value = 0
            cust.supplied_value = 0
            rp = RequestedProducts.query\
                .join(Request).filter(Request.customer_id == cust.id)\
                .filter(Request.created_dt >= start_dt)\
                .filter(Request.created_dt < end_dt)\
                .join(Product).order_by(Product.maker_id).order_by(Product.code)\
                .all()
            cust.requested_products = rp
            for r in rp:
                if r.product.price_retail:
                    cust.requested_value += r.quantity * r.product.price_retail
                else:
                    cust.request_alert = True
            sp = SuppliedProducts.query\
                .join(Supply).filter(Supply.customer_id == cust.id)\
                .filter(Supply.created_dt >= start_dt)\
                .filter(Supply.created_dt < end_dt)\
                .join(Product).order_by(Product.maker_id).order_by(Product.code)\
                .all()
            cust.supplied_products = sp
            for s in sp:
                if s.product.price_retail:
                    cust.supplied_value += s.quantity * s.product.price_retail
                else:
                    cust.supply_alert = True
            sum_request_values += cust.requested_value
            sum_supply_values += cust.supplied_value

    return render_template('settings/recommendedshares.html',
                           title=gettext("Sales of Recommended Customers"),
                           customers_with_recommended=customers_with_recommended,
                           recommended=recommended,
                           sum_request_values=sum_request_values,
                           sum_supply_values=sum_supply_values,
                           curr_id=curr_id,
                           curr_year=curr_year,
                           curr_month=curr_month,
                           this_year=now.year,
                           base_share=BASE_SHARE_FROM_RECOMMENDED)