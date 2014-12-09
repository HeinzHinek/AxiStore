# -*- coding: utf-8 -*-

from app import db
from models import Product
from sqlalchemy.engine.reflection import Inspector
from collections import OrderedDict
from config import CSV_PATH
from flask.ext.babel import gettext
from datetime import datetime, timedelta
import csv, os, re
import calendar

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
    headers = [gettext('Product code'), gettext('Product Name'), gettext('Quantity on stock'), gettext('Days to deliver')]
    outcsv.writerow([unicode(header).encode('utf-8') for header in headers])
    for product in products:
        dtd = product.maker.standard_delivery_days if product.maker.standard_delivery_days else None
        month_and_third = days_to_month_and_third(dtd)
        text_dtd = month_and_third_to_text(month_and_third)
        columns = [product.code, product.desc_JP, product.available_qty, text_dtd]
        outcsv.writerow([unicode(column).encode('utf-8') for column in columns])

    outfile.close()

    match = re.search(r"[^a-zA-Z](csv)[^a-zA-Z]", path)
    pos = match.start(1)
    filename = path[pos:]

    return filename

def days_to_month_and_third(days):
    if days is None:
        return None
    now = datetime.utcnow() + timedelta(hours=9)   # Correction for Japanese time
    target = now + timedelta(days=days)
    month = target.month
    day = target.day
    if day > 0 and day < 11:
        third = 1
    elif day > 10 and day < 21:
        third = 2
    else:
        third = 3
    return {'month': month, 'third': third}

def month_and_third_to_text(month_and_third):
    if not month_and_third:
        return gettext('unknown')
    month = month_and_third['month']
    third = month_and_third['third']
    months = [gettext('January'), gettext('February'), gettext('March'), gettext('April'), gettext('May'),
              gettext('June'), gettext('July'), gettext('August'), gettext('September'), gettext('October'),
              gettext('November'), gettext('December')]
    thirds = [gettext(', First third'), gettext(', Second third'), gettext(', Third third')]
    return months[month-1] + thirds[third-1]