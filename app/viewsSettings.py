# -*- coding: utf-8 -*-

from flask import render_template, flash, redirect, request, url_for
from app import app, db
from models import Product, User
from forms import UploadForm, AddUserForm
from flask_login import login_required
from flask.ext.babel import gettext
from flask_login import current_user
from config import CSV_PATH
from werkzeug import secure_filename
from sqlalchemy.engine.reflection import Inspector
from collections import OrderedDict
from config import USER_ROLES, LANGUAGES
import os
import csv


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
    if form.validate_on_submit():
        user = User()
        user.nickname = form.nickname.data
        user.password = form.password.data
        user.email = form.email.data
        user.role = form.role.data
        user.language = form.language.data
        db.session.add(user)
        db.session.commit()
        flash(gettext("New user successfully added."))
        return redirect(url_for("users"))
    return render_template('settings/addUser.html',
                           title=gettext("Add New User"),
                           form=form)


@app.route('/settings/dataimport', methods=['GET', 'POST'])
@login_required
def dataImport():
    form = UploadForm()
    form.colnames = get_colnames(Product)
    if form.validate_on_submit() and form.filename.data:
        filename = secure_filename(form.filename.data.filename)
        file = request.files[form.filename.name].read()
        open(os.path.join(CSV_PATH, filename), 'w').write(file)
        result = process_csv(os.path.join(CSV_PATH, filename), Product)
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


def process_csv(path, orm):
    with open(path, 'rb') as csvfile:
        reader = csv.reader(csvfile)
        cols = get_colnames(orm)
        for row in reader:
            obj = orm()
            items = OrderedDict(zip(cols, row))
            for item in items:
                setattr(obj, item, items[item].decode('utf-8-sig'))
                db.session.add(obj)
    db.session.commit()
    return gettext('CSV uploaded and processed sucessfully.')


def get_colnames(orm):
    insp = Inspector.from_engine(db.engine)
    cols = insp.get_columns(orm.__tablename__)
    colnames = []
    for c in cols:
        colnames.append(c['name'])
    colnames.remove('id')
    return colnames