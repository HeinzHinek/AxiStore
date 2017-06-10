# -*- coding: utf-8 -*-

from app import db
from models import Product
from sqlalchemy.engine.reflection import Inspector
from collections import OrderedDict
from config import CSV_PATH
from flask import request
from flask_babel import gettext
from flask_login import current_user
from datetime import datetime, timedelta
from config import USER_ROLES
from imageHelper import getImgUrls
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
import csv, os, re


def parse_csv(path):
    with open(path, 'rb') as csvfile:
        reader = csv.reader(csvfile)
        data = []
        for row in reader:
            data.append([item.decode('utf-8', 'ignore') for item in row])
    return data


def process_csv(path, orm, cols):
    with open(path, 'rb') as csvfile:
        reader = csv.reader(csvfile)
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


def generate_available_stock_csv(categories=[]):
    path = os.path.join(CSV_PATH, ('axm_stock_' + datetime.utcnow().strftime("%Y%m%d") + '.csv'))
    outfile = open(path, 'wb+')
    outcsv = csv.writer(outfile)
    products = Product.query\
        .filter_by(active_flg=True)
    if categories:
        products = products.filter(Product.category_id.in_(categories))
    products = products.order_by(Product.category_id)\
        .order_by(Product.maker_id)\
        .order_by(Product.code)\
        .all()
    headers = [gettext('Product code'), gettext('Product Name'), gettext('Quantity on stock'), gettext('Planned time of delivery')]
    outcsv.writerow([unicode(header).encode('utf-8') for header in headers])
    for product in products:
        dtd = product.maker.standard_delivery_days if product.maker.standard_delivery_days else None
        month_and_third = days_to_month_and_third(dtd)
        if product.limited_flg:
            text_dtd = gettext('Product with limited number of items')
        else:
            text_dtd = month_and_third_to_text(month_and_third)
        columns = [product.code, product.desc_JP, product.available_qty, text_dtd]
        outcsv.writerow([unicode(column).encode('utf-8') for column in columns])

    outfile.close()

    match = re.search(r"[^a-zA-Z](csv)[^a-zA-Z]", path)
    pos = match.start(1)
    filename = path[pos:]

    return filename


def generate_product_details_csv(categories=[]):
    path = os.path.join(CSV_PATH, ('axm_products_' + datetime.utcnow().strftime("%Y%m%d") + '.csv'))
    outfile = open(path, 'wb+')
    outcsv = csv.writer(outfile)
    products = Product.query\
        .filter_by(active_flg=True)
    if categories:
        products = products.filter(Product.category_id.in_(categories))
    products = products.order_by(Product.category_id)\
        .order_by(Product.maker_id)\
        .order_by(Product.code)\
        .all()
    headers = [gettext('Product code'), gettext('Product Name'), gettext('Retail price'), gettext('Purchase price'),
               gettext('Image 1 URL'), gettext('Image 2 URL'), gettext('Image 3 URL'), gettext('Image 4 URL'),
               gettext('Image 5 URL')]
    outcsv.writerow([unicode(header).encode('utf-8') for header in headers])

    discount = 0
    if current_user.role == USER_ROLES['ROLE_CUSTOMER'] and current_user.customer:
        discount = current_user.customer.base_discount
    for product in products:
        if not product.price_retail:
            product.price_retail = 0
        unrounded_price = product.price_retail * (1.0 - discount)
        product.customer_price = int(5 * round(float(unrounded_price)/5))

        columns = [product.code, product.desc_JP, product.price_retail, product.customer_price]

        urls = getImgUrls(product.id)
        product.img_urls = []
        if urls:
            for i in xrange(5):
                if i >= len(urls):
                    columns.append('')
                else:
                    url = request.url_root + urls[i].split('app')[1]
                    url = url.replace('\\', '/')
                    url = url.replace('//', '/')
                    columns.append(url)
        else:
            for i in xrange(5):
                columns.append('')

        outcsv.writerow([unicode(column).encode('utf-8') for column in columns])

    outfile.close()

    match = re.search(r"[^a-zA-Z](csv)[^a-zA-Z]", path)
    pos = match.start(1)
    filename = path[pos:]

    return filename


def generate_axismart_availability_csv():
    path = os.path.join(CSV_PATH, 'axismart', 'availability.csv')
    outfile = open(path, 'wb+')
    outcsv = csv.writer(outfile, delimiter=';')     # Delimiter is set to ';' here!

    headers = ['NID', 'STATUS']
    outcsv.writerow([unicode(header).encode('utf-8') for header in headers])

    # Thread safe sessioning
    session_factory = sessionmaker(bind=db.engine)
    Session = scoped_session(session_factory)
    local_session = Session()
    products = local_session.query(Product).all()


    for product in products:
        if not product.axm_node or product.axm_node == "":
            continue
        if product.available_qty > 0 and product.active_flg == 1:
            availability = 1
        else:
            availability = 0
        columns = [product.axm_node, availability]
        outcsv.writerow([unicode(column).encode('utf-8') for column in columns])

    local_session.close()
    Session.remove()
    outfile.close()


def days_to_month_and_third(days):
    if days is None:
        return None
    now = datetime.utcnow() + timedelta(hours=9)   # Correction for Japanese time
    target = now + timedelta(days=days)
    month = target.month
    day = target.day
    year = target.year
    if day > 0 and day < 11:
        third = 1
    elif day > 10 and day < 21:
        third = 2
    else:
        third = 3
    return {'year': year, 'month': month, 'third': third}


def month_and_third_to_text(month_and_third):
    if not month_and_third:
        return gettext('unknown')
    year = month_and_third['year']
    month = month_and_third['month']
    third = month_and_third['third']
    years = str(year) + gettext('year, ')
    months = [gettext('January'), gettext('February'), gettext('March'), gettext('April'), gettext('May'),
              gettext('June'), gettext('July'), gettext('August'), gettext('September'), gettext('October'),
              gettext('November'), gettext('December')]
    thirds = [gettext(', First third'), gettext(', Second third'), gettext(', Third third')]
    return years + months[month-1] + thirds[third-1]
