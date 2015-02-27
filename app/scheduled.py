# -*- coding: utf-8 -*-

from app import db
from models import Product
from config import TEMP_FILES_PATH, LASTURA_SKLAD_URL
from csvHelper import parse_csv, generate_axismart_availability_csv
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
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

    # Thread safe sessioning
    session_factory = sessionmaker(bind=db.engine)
    Session = scoped_session(session_factory)
    local_session = Session()
    local_session._model_changes = {}   # flask-alchemy & pure sqlalchemy subclassing issue fix

    counter = 0
    for item in data:
        maker_code = item[0]
        try:
            maker_qty_stock = int(item[1])
        except ValueError:
            continue
        product = local_session.query(Product).filter_by(maker_code=maker_code).first()
        if product:
            product.maker_qty_stock = maker_qty_stock
            local_session.add(product)
            counter += 1

    local_session.commit()
    local_session.close()
    Session.remove()

    print "Scheduled job finished sucessfully. Number of updated values for Lastura: " + str(counter)
    return True


def scheduleExportAxismart():
    import logging
    logging.basicConfig()
    generate_axismart_availability_csv()
    return True