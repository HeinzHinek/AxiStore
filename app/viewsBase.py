# -*- coding: utf-8 -*-

from flask import render_template, request, g, session, flash, redirect, url_for
from app import app, db, lm, babel
from forms import UserForm, EditQtyStockForm
from models import User, Product, Category, OrderedProducts, Order, Maker
from flask_login import current_user, login_required
from config import PRODUCTS_PER_PAGE, LANGUAGES, USER_ROLES
from flask.ext.babel import gettext

@app.before_request
def before_request():
    g.user = current_user
    g.USER_ROLES = USER_ROLES

    cat_id = request.args.get('cat')
    if cat_id:
        session['category_id'] = int(cat_id)
        g.category_id = int(cat_id)
        session.pop('maker_id')
        g.maker_id = None
    else:
        if 'category_id' not in session:
            g.category_id = Category.query.first().id
            session['category_id'] = g.category_id
        else:
            g.category_id = session['category_id']

    mak_id = request.args.get('mak')
    if mak_id:
        if int(mak_id) == -1:
            g.maker_id = None
            session['maker_id'] = g.maker_id
        else:
            session['maker_id'] = int(mak_id)
            g.maker_id = int(mak_id)
    else:
        if 'maker_id' not in session:
            g.maker_id = None
            session['maker_id'] = g.maker_id
        else:
            g.maker_id = session['maker_id']

    if not hasattr(g.user, 'products_per_page'):
        g.user.products_per_page = PRODUCTS_PER_PAGE


@app.after_request
def after_request(response):
    db.session.expire_all()
    return response


@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template("index.html",
                           title=gettext('Home'),
                           user=g.user)


@app.route('/stock', methods=['GET', 'POST'])
@app.route('/stock/<int:page>', methods=['GET', 'POST'])
@login_required
def stock(page=1):
    #Query products with conditions
    products = Product.query.order_by(Product.maker_id, Product.code)\
        .filter_by(category_id=int(g.category_id),
                   active_flg=True)
    if g.maker_id is not None:
        products = products.filter(Product.maker_id==int(g.maker_id))
    products = products.paginate(page, current_user.products_per_page, False)

    categories = Category.query.order_by(Category.order.asc()).all()
    curr_category = Category.query.filter_by(id=g.category_id).one()
    available_makers_id = [maker.id for maker in curr_category.makers]
    makers = Maker.query.filter(Maker.id.in_(available_makers_id)).all()
    curr_maker_name = Maker.query.filter_by(id=g.maker_id).one().name if g.maker_id else None
    form = EditQtyStockForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            qty = form.qty_stock.data
            id = request.form['product_id']
            if (qty and id) or (qty == 0 and id):
                product = Product.query.filter_by(id=int(id)).first()
                if product:
                    product.qty_stock = qty
                    db.session.add(product)
                    db.session.commit()
                    flash(gettext('Stock quantity successfully updated.'))
            else:
                flash(gettext('Input value error.'))
        else:
            flash(gettext('Input value error.'))
        return redirect(url_for("stock"))

    #compute net stock for each product
    for product in products.items:
        if product.qty_stock is not None \
                and product.request_qty is not None \
                and product.order_qty is not None:
            product.net_stock = product.qty_stock - product.request_qty + product.order_qty
        else:
            product.net_stock = None

    return render_template("stock.html",
                           title=gettext('Stock condition'),
                           categories=categories,
                           makers=makers,
                           curr_maker_name=curr_maker_name,
                           form=form,
                           products=products)


@app.route('/user', methods=['GET', 'POST'])
@login_required
def user():
    form = UserForm(obj=current_user)
    if form.validate_on_submit():
        user = current_user
        user.language = form.language.data
        user.products_per_page = form.products_per_page.data\
                                 if form.products_per_page.data\
                                 else 20
        db.session.add(user)
        db.session.commit()
        flash(gettext('User settings sucessfully updated.'))
    form.language.data = (current_user.language
                          if current_user.language
                          else 0)
    form.products_per_page.data = (current_user.products_per_page
                                   if current_user.products_per_page
                                   else PRODUCTS_PER_PAGE)
    return render_template('user.html',
                           title=gettext("User's Page"),
                           form=form)


@app.route('/settings')
@login_required
def settings():
    return render_template('settings.html',
                           title=gettext("Settings"))


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@babel.localeselector
def get_locale():
    lang = request.accept_languages.best_match(LANGUAGES.keys())
    if g.user.is_authenticated():
        lang = g.user.language
    return lang