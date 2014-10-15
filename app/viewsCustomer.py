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
    company_choices = [(a.id, a.company_name) for a in Contact.query.all()]
    company_choices = [(0, '')] + company_choices
    form.company.choices = company_choices
    if form.validate_on_submit():
        customer = Customer()
        customer.name = form.name.data
        customer.first_name = form.first_name.data
        customer.surname = form.surname.data
        customer.phone = form.phone.data
        customer.email = form.email.data
        if form.company.data and form.company.data != 0:
            customer.contact_id = form.company.data
        customer.base_discount = int(form.base_discount.data)/100.0
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
    company_choices = [(a.id, a.company_name) for a in Contact.query.all()]
    company_choices = [(0, '')] + company_choices
    form.company.choices = company_choices
    if form.is_submitted():
        #delete maker
        if 'delete' in request.form:
            #db.session.delete(customer)
            #db.session.commit()
            flash(gettext('This operation is not allowed at the moment.'))
            return redirect(url_for("customers"))

        if form.validate():
            #update maker
            customer.name = form.name.data
            customer.first_name = form.first_name.data
            customer.surname = form.surname.data
            customer.phone = form.phone.data
            customer.email = form.email.data
            if form.company.data and form.company.data != '' and form.company.data != 0:
                customer.contact_id = form.company.data
            else:
                customer.contact_id = None
            customer.base_discount = int(form.base_discount.data)/100.0
            db.session.add(customer)
            db.session.commit()
            flash(gettext("Customer successfully changed."))
            return redirect(url_for("customers"))

    form.base_discount.data = int(customer.base_discount*100) if customer.base_discount else 0
    selected = customer.contact.id if customer.contact else 0
    return render_template('settings/editCustomer.html',
                           title=gettext("Edit Customer"),
                           customer=customer,
                           selected=selected,
                           form=form)
