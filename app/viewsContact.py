# -*- coding: utf-8 -*-

from flask import render_template, flash, redirect, url_for, request
from app import app, db
from forms import AddContactForm
from models import Contact
from flask_login import login_required
from config import DEFAULT_PER_PAGE
from flask.ext.babel import gettext


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
    if form.validate_on_submit():
        contact = Contact()
        contact.company_name = form.company_name.data
        contact.post_code = form.post_code1.data + form.post_code2.data
        contact.address1 = form.address1.data
        contact.address2 = form.address2.data
        contact.address3 = form.address3.data
        contact.phone = form.phone.data
        contact.email = form.email.data
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
    if contact.post_code:
        post_code = str(contact.post_code)
    else:
        post_code = ''
    form.post_code1.data = post_code[:3]
    form.post_code2.data = post_code[3:]
    if form.is_submitted():

        #delete maker
        if 'delete' in request.form:
            db.session.delete(contact)
            db.session.commit()
            return redirect(url_for("contacts"))

        if form.validate():
            #update maker
            contact.company_name = form.company_name.data
            contact.post_code = form.post_code1.data + form.post_code2.data
            contact.address1 = form.address1.data
            contact.address2 = form.address2.data
            contact.address3 = form.address3.data
            contact.phone = form.phone.data
            contact.email = form.email.data
            db.session.add(contact)
            db.session.commit()
            flash(gettext("Contact successfully changed."))
            return redirect(url_for("contacts"))

    return render_template('settings/editContact.html',
                           title=gettext("Edit Contact"),
                           contact=contact,
                           form=form)
