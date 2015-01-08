# -*- coding: utf-8 -*-

from flask import render_template, flash, redirect, url_for, json
from app import app
from models import User, Customer, Catalog, CatalogedProducts, Maker
from forms import UploadForm, AddUserForm, EditUserForm, SimpleSubmitForm
from flask_login import login_required
from werkzeug.security import generate_password_hash
from flask.ext.babel import gettext
from csvHelper import *
from config import CSV_PATH
from werkzeug import secure_filename
from config import USER_ROLES, LANGUAGES, CUSTOMER_TYPES, CUSTOMER_CODES_PATH
import os
import glob


@app.route('/settings/users')
@app.route('/setings/users/<int:page>')
@login_required
def users(page=1):
    users = User.query.paginate(page, current_user.products_per_page, False)
    return render_template('/settings/users.html',
                    title=gettext("User List"),
                    roles = dict((v,k) for k,v in USER_ROLES.items()),
                    languages=LANGUAGES,
                    users=users)

@app.route('/settings/adduser', methods=['GET', 'POST'])
@login_required
def addUser():
    form = AddUserForm()
    customer_choices = [(a.id, a.name) for a in Customer.query.filter_by(customer_type=CUSTOMER_TYPES['TYPE_CUSTOMER']).all()]
    customer_choices = [(0, '')] + customer_choices
    maker_choices = [(a.id, a.name) for a in Maker.query.all()]
    maker_choices = [(0, '')] + maker_choices
    form.customer.choices = customer_choices
    form.maker.choices = maker_choices

    if form.validate_on_submit():
        if len(User.query.filter_by(nickname=form.nickname.data).all()) > 0:
            flash(gettext("Selected username already exists!"))
            return redirect(url_for('users'))

        new_email = form.email.data
        check_mail = User.query.filter_by(email=new_email).all()

        #user mail already exists
        if len(check_mail) > 0:
            flash(gettext('Selected email is already in use!'))
            return redirect(url_for('users'))

        user = User()
        user.nickname = form.nickname.data
        user.password = generate_password_hash(form.password.data)
        user.email = form.email.data
        user.role = form.role.data

        if int(form.role.data) == USER_ROLES['ROLE_CUSTOMER']:
            if form.customer.data and form.customer.data != '' and form.customer.data != 0:
                user.customer_id = form.customer.data
            else:
                user.customer_id = None
        elif int(form.role.data) == USER_ROLES['ROLE_MAKER']:
            if form.maker.data and form.maker.data != '' and form.maker.data != 0:
                user.maker_id = form.maker.data
            else:
                user.maker_id = None
        else:
            user.customer_id = None
            user.maker_id = None

        user.language = form.language.data
        db.session.add(user)
        db.session.commit()
        flash(gettext("New user successfully added."))
        return redirect(url_for("users"))
    return render_template('settings/addUser.html',
                           title=gettext("Add New User"),
                           USER_ROLES=USER_ROLES,
                           form=form)


@app.route('/settings/edituser/<int:id>', methods=['GET', 'POST'])
@login_required
def editUser(id=0):
    user = User.query.filter_by(id=id).first()
    form = EditUserForm(obj=user)
    customer_choices = [(a.id, a.name) for a in Customer.query.filter_by(customer_type=CUSTOMER_TYPES['TYPE_CUSTOMER']).all()]
    customer_choices = [(0, '')] + customer_choices
    maker_choices = [(a.id, a.name) for a in Maker.query.all()]
    maker_choices = [(0, '')] + maker_choices
    form.customer.choices = customer_choices
    form.maker.choices = maker_choices

    if form.validate_on_submit():
        if len(User.query.filter_by(nickname=form.nickname.data).all()) > 1:
            flash(gettext("Selected username already exists!"))
            return redirect(url_for('users'))

        new_email = form.email.data
        check_mail = User.query.filter_by(email=new_email).all()

        #user mail already exists
        if len(check_mail) > 0 and new_email != user.email:
            flash(gettext('Selected email is already in use!'))
            return redirect(url_for('users'))

        user.nickname = form.nickname.data
        user.email = form.email.data
        user.role = form.role.data

        if int(form.role.data) == USER_ROLES['ROLE_CUSTOMER']:
            if form.customer.data and form.customer.data != '' and form.customer.data != 0:
                user.customer_id = form.customer.data
                user.maker_id = None
            else:
                user.customer_id = None
        elif int(form.role.data) == USER_ROLES['ROLE_MAKER']:
            if form.maker.data and form.maker.data != '' and form.maker.data != 0:
                user.maker_id = form.maker.data
                user.customer_id = None
            else:
                user.maker_id = None
        else:
            user.customer_id = None
            user.maker_id = None

        user.language = form.language.data
        db.session.add(user)
        db.session.commit()
        flash(gettext("User details succesfully changed."))
        return redirect(url_for("users"))
    selected_customer = user.customer_id if user.customer_id else 0
    selected_maker = user.maker_id if user.maker_id else 0
    return render_template('settings/editUser.html',
                           title=gettext("Edit User"),
                           USER_ROLES=USER_ROLES,
                           selected_customer=selected_customer,
                           selected_maker=selected_maker,
                           form=form)


@app.route('/settings/editcatalog', methods=['GET'])
@login_required
def editCatalog():
    catalog = Catalog.query.order_by(Catalog.order).all()

    return render_template('settings/editCatalog.html',
                           title=gettext("Edit Catalog"),
                           catalog=catalog)


# AJAX
@app.route('/settings/savecatalog', methods=['POST'])
@login_required
def saveCatalog():
    data = json.loads(request.form['data'])
    if not data:
        return "0"

    order = 1
    super_id = None
    for item in data:
        id = int(item['id'].split('_')[1])
        indent = int(item['indent'])
        name_cs = item['name_cs']
        name_jp = item['name_jp']

        if id > 0:
            c = Catalog.query.filter_by(id=id).first()
        else:
            c = Catalog()
            db.session.add(c)
            db.session.commit()

        if indent >= 0:
            if indent == 0:
                super_id = c.id
                c.super_id = None
                c.order = order
            else:

                # Check whether child wasn't moved to another parent,
                # if so, add this parent to all products that have this child in catalog
                if c.super_id != super_id:
                    cataloged_products_to_update = CatalogedProducts.query.filter_by(catalog_id=c.id).all()
                    for cpu in cataloged_products_to_update:
                        control_catalog_product = CatalogedProducts.query.filter_by(product_id=cpu.product_id)\
                            .filter_by(catalog_id=super_id).first()
                        if not control_catalog_product:
                            product = Product.query.filter_by(id=cpu.product_id).first()
                            if product:
                                cp = CatalogedProducts()
                                cp.product_id = cpu.product_id
                                cp.catalog_id = super_id
                                db.session.add(cp)
                                db.session.commit()
                c.super_id = super_id
                c.order = order
            c.name_CS = name_cs
            c.name_JP = name_jp
            db.session.add(c)
            order += 1
        else:
            for cp in c.products:
                db.session.delete(cp)
            db.session.delete(c)

    db.session.commit()
    return "ok"


@app.route('/settings/dataimport', methods=['GET', 'POST'])
@login_required
def dataImport():
    form = UploadForm()
    colnames = get_colnames(Product)
    form.colnames = colnames
    if form.validate_on_submit() and form.filename.data:
        filename = secure_filename(form.filename.data.filename)
        file = request.files[form.filename.name].read()
        open(os.path.join(CSV_PATH, filename), 'w').write(file)
        result = process_csv(os.path.join(CSV_PATH, filename), Product, colnames)
        flash(result)
        redirect('/settings/dataimport')
    return render_template('/settings/dataimport.html',
                           title=gettext("Data Import"),
                           form=form)


@app.route('/settings/dataexport')
@login_required
def dataExport():
    return render_template('/settings/dataexport.html',
                           title=gettext("Data Export"))


@app.route('/settings/dataexport/products')
@login_required
def downloadProducts():

    flash('This function is not available yet')
    return redirect('/settings/dataexport')


@app.route('/settings/dataexport/downloadAvailableStock')
@login_required
def downloadAvailableStock():
    return redirect(url_for('download_file', filename=generate_available_stock_csv()))


@app.route('/settings/customercodes', methods=['GET', 'POST'])
@login_required
def customerCodes():

    if request.method == 'POST':
        id = request.form['customer_id']
        return redirect(url_for('editCustomerCodes', customer_id=id))

    filenames = getCustomerCodesDefinitionFiles()
    customer_ids_with_files = []
    for filename in filenames:
        id = filename.split('cust_')[1]
        id = id.split('.csv')[0]
        try:
            id = int(id)
        except ValueError:
            continue
        customer_ids_with_files.append(id)
    customers = Customer.query.filter_by(customer_type=CUSTOMER_TYPES['TYPE_CUSTOMER']).all()
    for customer in customers:
        if customer.id in customer_ids_with_files:
            customer.hasfile = True
    return render_template('/settings/customercodes.html',
                           title=gettext("Customer Codes"),
                           customers=customers)


@app.route('/settings/editcustomercodes/<int:customer_id>', methods=['GET', 'POST'])
@login_required
def editCustomerCodes(customer_id=None):

    form = UploadForm()

    if form.validate_on_submit() and form.filename.data:
        file = form.filename.data
        filename = 'cust_' + str(customer_id) + '.csv'
        file.save(os.path.join(CUSTOMER_CODES_PATH, filename))
        try:
            parse_csv(os.path.join(CUSTOMER_CODES_PATH, filename))
            flash(gettext('CSV uploaded and processed sucessfully.'))
        except:
            print "hovinko"
            flash(gettext('Upload unsuccessful! File could not be parsed!'))
        redirect('/settings/editcustomercodes')

    def_file_path = getCustomerCodesDefinitionFiles(customer_id)
    if def_file_path:
        try:
            def_file_data = parse_csv(def_file_path[0])
        except:
            def_file_data = []
    else:
        def_file_data = []
    customer = Customer.query.get(customer_id)

    return render_template('/settings/editcustomercodes.html',
                           title=gettext("Edit Customer Codes"),
                           customer=customer,
                           def_file_data=def_file_data,
                           form=form)


def getCustomerCodesDefinitionFiles(customer_id=None):
    filenames = []
    id = str(customer_id) if customer_id else '*'
    filenames.extend(glob.glob(CUSTOMER_CODES_PATH + 'cust_' + id + '.csv'))
    filenames = sorted(filenames)
    return filenames