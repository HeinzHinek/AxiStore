# -*- coding: utf-8 -*-

from flask import render_template, flash, redirect, url_for, request
from app import app, db
from forms import AddCustomerForm
from models import Customer, Contact
from flask_login import login_required
from config import DEFAULT_PER_PAGE, CUSTOMER_TYPES
from flask.ext.babel import gettext


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
    if form.validate_on_submit():
        customer = Customer()

        customer.name = form.name.data
        customer.email = form.email.data
        customer.base_discount = int(form.base_discount.data)/100.0

        customer.company_name = form.company_name.data
        customer.post_code = int(str(form.post_code1.data) + str(form.post_code2.data))
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

            customer.company_name = form.company_name.data
            customer.post_code = int(str(form.post_code1.data) + str(form.post_code2.data))
            customer.address1 = form.address1.data
            customer.address2 = form.address2.data
            customer.address3 = form.address3.data

            db.session.add(customer)
            db.session.commit()
            flash(gettext("Customer successfully changed."))
            return redirect(url_for("customers"))

    form.base_discount.data = int(customer.base_discount*100) if customer.base_discount else 0
    if customer.post_code:
        post_code = str(customer.post_code)
    else:
        post_code = ''
    form.post_code1.data = post_code[:3]
    form.post_code2.data = post_code[3:]

    return render_template('settings/editCustomer.html',
                           title=gettext("Edit Customer"),
                           customer=customer,
                           form=form)
