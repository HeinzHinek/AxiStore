# -*- coding: utf-8 -*-

from app import db
from models import Product
from config import TEMP_FILES_PATH, LASTURA_SKLAD_URL
from csvHelper import parse_csv
import os, urllib2

def sheduleLastura():
    import logging
    logging.basicConfig()
    print "Running scheduled job: updating maker stock quantities for Lastura."
    try:
        webFile = urllib2.urlopen(LASTURA_SKLAD_URL)
    except urllib2.HTTPError:
        print "Remote file not found! Aborting!"
        return False
    filename = os.path.join(TEMP_FILES_PATH, LASTURA_SKLAD_URL.split('/')[-1])
    localFile = open(filename, 'w')
    localFile.write(webFile.read())
    webFile.close()
    localFile.close()
    data = parse_csv(filename)[1:]
    counter = 0
    for item in data:
        maker_code = item[0]
        try:
            maker_qty_stock = int(item[1])
        except ValueError:
            continue
        product = Product.query.filter_by(maker_code=maker_code).first()
        if product:
            product.maker_qty_stock = maker_qty_stock
            db.session.add(product)
            db.session.commit()
            counter += 1

    print "Scheduled job finished sucessfully. Number of updated values for Lastura: " + str(counter)
    return True
