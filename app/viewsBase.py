# -*- coding: utf-8 -*-

from flask import render_template, request, g, session, flash, redirect, url_for, json
from app import app, db, lm, babel
from forms import UserForm, EditQtyStockForm, SearchForm
from models import User, Product, Category, Maker, Request
from flask_login import current_user, login_required
from config import PRODUCTS_PER_PAGE, LANGUAGES, USER_ROLES, CUSTOMER_TYPES
from flask.ext.babel import gettext
from sqlalchemy import or_
from datetime import datetime
import calendar


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

    search_string = request.args.get('search')
    if search_string:
        session['search_string'] = search_string
        g.category_id = None
        g.maker_id = None
    else:
        if 'search_string' not in session:
            session['search_string'] = None

    order_type = request.args.get('ord')
    if order_type:
        session['order_type'] = order_type
    else:
        if 'order_type' not in session:
            session['order_type'] = None

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
    products = Product.query.filter_by(active_flg=True)
    curr_search = None
    if session['search_string']:
        curr_search = session['search_string']
        products = products.filter(or_(Product.code.like('%' + session['search_string'] + '%'),
                                       (Product.desc_CS.like('%' + session['search_string'] + '%')),
                                       (Product.desc_JP.like('%' + session['search_string'] + '%'))))
    if g.maker_id is not None:
        products = products.filter(Product.maker_id == int(g.maker_id))
        g.category_id = Maker.query.filter_by(id=g.maker_id).one().category_id
    if g.category_id:
        curr_category = Category.query.filter_by(id=g.category_id).one()
        products = products.filter_by(category_id=int(g.category_id))
        available_makers_id = [maker.id for maker in curr_category.makers]
    else:
        available_makers_id = [maker.id for maker in Maker.query.all()]

    #Custom ordering
    if session['order_type']:
        order_type = session['order_type'].split('-')
        if order_type[0] == 'csdesc':
            property = Product.desc_CS
        elif order_type[0] == 'maker':
            property = Product.maker_id
        elif order_type[0] == 'jpdesc':
            property = Product.desc_CS
        elif order_type[0] == 'unitp':
            property = Product.price_unit
        elif order_type[0] == 'retap':
            property = Product.price_retail
        elif order_type[0] == 'stock':
            property = Product.qty_stock
        elif order_type[0] == 'req':
            property = Product.request_qty
        elif order_type[0] == 'ord':
            property = Product.order_qty
        elif order_type[0] == 'net':
            property = (Product.qty_stock - Product.request_qty + Product.order_qty)
        else:
            session['order_type'] = None
            property = None

        style = order_type[1]
        if style:
            if style == '3' or style == '4':
                products = products.filter(property > 0)
            if style == '5' or style == '6':
                products = products.filter(property <= 0)
            if style == '1' or style == '3' or style == '5':
                products = products.order_by(property.desc())
            else:
                products = products.order_by(property)

    products = products.order_by(Product.maker_id, Product.code)
    products = products.paginate(page, current_user.products_per_page, False)
#Query end

    categories = Category.query.order_by(Category.order.asc()).all()
    makers = Maker.query.filter(Maker.id.in_(available_makers_id)).all()
    curr_maker_name = Maker.query.filter_by(id=g.maker_id).one().name if g.maker_id else None

    form = EditQtyStockForm()
    if form.is_submitted():
        if form.validate():
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
        page = request.form['page'] if request.form['product_id'] else 1
        return redirect(url_for("stock", page=page))

    return render_template("stock.html",
                           title=gettext('Stock condition'),
                           categories=categories,
                           makers=makers,
                           curr_maker_name=curr_maker_name,
                           curr_search=curr_search,
                           form=form,
                           form_search=SearchForm(),
                           products=products)


@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    form_search = SearchForm(request.form)
    if form_search.is_submitted():
        string = form_search.search.data
        if string:
            if len(string) > 1:
                return redirect(url_for('stock', search=string))
    if session['search_string']:
        return redirect(url_for('stock', search=session['search_string']))
    return redirect('stock')


@app.route('/clearsearch')
@login_required
def clearsearch():
    session['search_string'] = None
    return redirect(url_for('stock'))


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


@app.route('/prepareReqGraphData', methods=['POST'])
@login_required
def prepareReqGraphData():
    data = request.form['data'] if request.form['data'] else None
    date = datetime.strptime(data[:24].encode('utf-8'), "%a %b %d %Y %H:%M:%S")
    begin_date = datetime(date.year, date.month, 1)
    today = datetime.now()
    if date.year == today.year and date.month == today.month:
        last_day = today.day
    else:
        last_day = calendar.monthrange(date.year, date.month)[1]
    end_date = datetime(date.year, date.month, last_day)
    reqs = Request.query\
        .filter(Request.created_dt >= begin_date)\
        .filter(Request.created_dt <= end_date)\
        .all()
    data = []
    cust = 0
    axm = 0
    for i in range(1, last_day + 1):
        item = {}
        item['date'] = str(date.strftime("%b")) + " " + str(i)
        for r in reqs:
            if r.created_dt.day == i and r.customer is not None:
                if r.customer.customer_type == CUSTOMER_TYPES['TYPE_CUSTOMER']:
                    cust += 1
                elif r.customer.customer_type == CUSTOMER_TYPES['TYPE_AXM']:
                    axm += 1
        item['customers'] = cust
        item['AxM'] = axm
        data.append(item)
    print data
    return json.dumps(data);