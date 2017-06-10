# -*- coding: utf-8 -*-

from flask import render_template, flash, redirect, url_for, request
from app import app, db
from forms import AddContactForm
from models import Contact, Customer
from permissions import login_required
from config import DEFAULT_PER_PAGE, CUSTOMER_TYPES
from flask_babel import gettext


@app.route('/contacts')
@app.route('/contacts/<int:page>')
@login_required
def contacts(page=1):
    contacts = Contact.query.paginate(page, DEFAULT_PER_PAGE, False)
    return render_template('settings/contacts.html',
                           title=gettext("Contacts"),
                           contacts=contacts)


@app.route('/addcontact', methods=['GET', 'POST'])
@login_required
def addContact():
    form = AddContactForm()
    customer_choices = [(a.id, a.name) for a in Customer.query.filter_by(customer_type=CUSTOMER_TYPES['TYPE_CUSTOMER']).all()]
    customer_choices = [(0, '')] + customer_choices
    form.customer.choices = customer_choices
    if form.validate_on_submit():
        contact = Contact()

        contact.first_name = form.first_name.data
        contact.surname = form.surname.data
        contact.phone = form.phone.data
        contact.email = form.email.data

        if form.customer.data and form.customer.data != '' and form.customer.data != 0:
            contact.customer_id = form.customer.data
        else:
            contact.customer_id = None

        db.session.add(contact)
        db.session.commit()
        flash(gettext("New contact successfully added."))
        return redirect(url_for("contacts"))
    return render_template('settings/addContact.html',
                           title=gettext("Add New Contact"),
                           form=form)


@app.route('/editcontact/<int:id>', methods=['GET', 'POST'])
@login_required
def editContact(id=0):
    contact = Contact.query.filter_by(id=id).first()
    if contact == None:
        flash(gettext('Contact not found.'))
        return redirect(url_for('contacts'))
    form = AddContactForm(obj=contact)

    customer_choices = [(a.id, a.name) for a in Customer.query.filter_by(customer_type=CUSTOMER_TYPES['TYPE_CUSTOMER']).all()]
    customer_choices = [(0, '')] + customer_choices
    form.customer.choices = customer_choices

    if form.is_submitted():
        #delete contact
        if 'delete' in request.form:
            db.session.delete(contact)
            db.session.commit()
            return redirect(url_for("contacts"))

        if form.validate():
            #update contact

            contact.first_name = form.first_name.data
            contact.surname = form.surname.data
            contact.phone = form.phone.data
            contact.email = form.email.data

            if form.customer.data and form.customer.data != '' and form.customer.data != 0:
                contact.customer_id = form.customer.data
            else:
                contact.customer_id = None

            db.session.add(contact)
            db.session.commit()
            flash(gettext("Contact successfully changed."))
            return redirect(url_for("contacts"))

    selected = contact.customer.id if contact.customer else 0
    return render_template('settings/editContact.html',
                           title=gettext("Edit Contact"),
                           contact=contact,
                           selected=selected,
                           form=form)
