# -*- coding: utf-8 -*-

from app import db
from models import Product
from sqlalchemy.engine.reflection import Inspector
from collections import OrderedDict
from config import CSV_PATH
from flask.ext.babel import gettext
from datetime import datetime
import csv, os, re

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
        columns = [product.code, product.desc_JP, product.available_qty, dtd]
        outcsv.writerow([unicode(column).encode('utf-8') for column in columns])

    outfile.close()

    match = re.search(r"[^a-zA-Z](csv)[^a-zA-Z]", path)
    pos = match.start(1)
    filename = path[pos:]

    return filename