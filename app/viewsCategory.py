# -*- coding: utf-8 -*-

from flask import render_template, flash, redirect, url_for, request
from app import app, db
from forms import AddCategoryForm
from models import Category
from flask_login import login_required
from sqlalchemy.sql import func
from flask.ext.babel import gettext

@app.route('/categories')
@login_required
def categories():
    categories = Category.query.order_by(Category.order.asc()).all()
    return render_template('settings/categories.html',
                           title=gettext("Product Categories"),
                           categories=categories)


@app.route('/addcategory', methods=['GET', 'POST'])
@login_required
def addCategory():
    form = AddCategoryForm()
    if form.validate_on_submit():
        category = Category()
        category.name_CS = form.name_CS.data
        category.name_JP = form.name_JP.data
        ol = db.session.query(func.max(Category.order).label('order_max')).one()
        category.order = ol.order_max if ol else 1
        db.session.add(category)
        db.session.commit()
        flash(gettext("New product category successfully added."))
        return redirect(url_for("categories"))
    return render_template('settings/addCategory.html',
                           title=gettext("Add New Product Category"),
                           form=form)


@app.route('/editcategory/<int:id>', methods=['GET', 'POST'])
@login_required
def editCategory(id=0):
    category = Category.query.filter_by(id=id).first()
    if category == None:
        flash(gettext('Category not found.'))
        return redirect(url_for('categories'))
    form = AddCategoryForm(obj=category)
    if form.validate_on_submit():

        #delete category
        if 'delete' in request.form:
            db.session.delete(category)
            db.session.commit()
            return redirect(url_for("categories"))

        #update category
        category.name_CS_ = form.name_CS.data
        category.name_JP = form.name_JP.data
        db.session.add(category)
        db.session.commit()
        flash(gettext("Category successfully changed."))
        return redirect(url_for("categories"))
    return render_template('settings/editCategory.html',
                           title=gettext("Edit Category"),
                           category=category,
                           form=form)

@app.route('/categories/saveorder', methods=['POST'])
@login_required
def saveOrder():
    data = request.form.getlist('cat[]')
    for idx, val in enumerate(data):
        c = Category.query.filter_by(id=val).first()
        c.order = idx+1
        db.session.add(c)
        db.session.commit()
    return "ok"