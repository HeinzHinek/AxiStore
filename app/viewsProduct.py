# -*- coding: utf-8 -*-

from flask import render_template, flash, redirect, url_for, request, jsonify
from app import app, db
from forms import AddProductForm
from models import Product, Maker
from flask_login import login_required
from flask.ext.babel import gettext


@app.route('/addProduct', methods=['GET', 'POST'])
@login_required
def addProduct():
    form = AddProductForm()
    makers = Maker.query.all()
    if makers:
        form.maker.choices = [(a.id, a.name) for a in makers]
    if form.validate_on_submit():
        product = Product()
        product.code = form.code.data
        product.maker_id = form.maker.data.id
        product.desc_CS = form.desc_CS.data
        product.desc_JP = form.desc_JP.data
        product.price_unit = form.price_unit.data
        product.price_retail = form.price_retail.data
        product.qty_stock = form.qty_stock.data
        category_id = Maker.query.filter_by(id=product.maker_id).first().category_id
        if category_id:
            product.category_id = category_id
        db.session.add(product)
        db.session.commit()
        flash(gettext("New product successfully added."))
        return redirect(url_for("stock"))
    return render_template("product/addProduct.html",
                           title=gettext('Add new product'),
                           form=form)


@app.route('/editproduct', methods=['GET', 'POST'])
@app.route('/editproduct/<int:id>', methods=['GET', 'POST'])
@login_required
def editProduct(id=0):
    product = Product.query.filter_by(id=id).first()
    if product == None:
        flash(gettext('Product not found.'))
        return redirect(url_for('stock'))
    form = AddProductForm(obj=product)
    makers = Maker.query.all()
    if makers:
        form.maker.choices = [(a.id, a.name) for a in makers]
    #for existing code validation
    form.request = request
    if form.validate_on_submit():

        #delete product
        if 'delete' in request.form:
            db.session.delete(product)
            db.session.commit()
            return redirect(url_for("stock"))

        #update product
        product.code = form.code.data
        product.maker_id = form.maker.data.id
        product.desc_CS = form.desc_CS.data
        product.desc_JP = form.desc_JP.data
        product.price_unit = form.price_unit.data
        product.price_retail = form.price_retail.data
        product.qty_stock = form.qty_stock.data
        category_id = Maker.query.filter_by(id=product.maker_id).first().category_id
        if category_id:
            product.category_id = category_id
        db.session.add(product)
        db.session.commit()
        flash(gettext("Product successfully changed."))
        return redirect(url_for("stock"))
    selected = product.maker_id
    return render_template('product/editProduct.html',
                           title=gettext("Edit Product"),
                           product=product,
                           selected_category=selected,
                           form=form)


@app.route('/checkProductId', methods=['POST'])
@login_required
def checkProductId():
    code = request.form['code']
    orig_id = request.form['orig_id']
    if orig_id and code == orig_id:
        result = 'OK'
    else:
        search = Product.query.filter_by(code=code).first()
        if search:
            result = 'NG'
        else:
            result = 'OK'
    return jsonify({'result': result})


@app.route('/findProductsAjax', methods=['POST'])
@login_required
def findProductAjax():
    code = request.form['code'] if request.form['code'] else None
    maker_id = request.form['maker'] if request.form['maker'] else None
    desc_CS = request.form['desc_cs'] if request.form['desc_cs'] else None
    desc_JP = request.form['desc_jp'] if request.form['desc_jp'] else None

    try:
        int_maker_id = int(maker_id)
    except ValueError:
        int_maker_id = None

    if not code and not int_maker_id and not desc_CS and not desc_JP:
        return '0'

    result = db.session.query(Product)
    if code:
        result = result.filter(Product.code.like('%' + code + '%'))
    if int_maker_id:
        result = result.filter(Product.maker_id==int_maker_id)
    if desc_CS:
        result = result.filter(Product.desc_CS.like('%' + desc_CS + '%'))
    if desc_JP:
        result = result.filter(Product.desc_JP.like('%' + desc_JP + '%'))
    result = result.filter(Product.active_flg==True)
    return jsonify(result=[i.serialize for i in result.all()])
