# -*- coding: utf-8 -*-

from flask.ext.mail import Message
from app import mail
from flask import render_template
from flask_login import current_user
from config import ADMINS, USER_ROLES
from models import RequestedProducts, User
from flask.ext.babel import gettext


def send_email(subject, sender, recipients, text_body, html_body, bulk=False):
    if bulk:
        with mail.connect() as conn:
            for recipient in recipients:
                msg = Message(subject, sender=sender, recipients=[recipient])
                msg.body = text_body
                msg.html = html_body
                conn.send(msg)
    else:
        msg = Message(subject, sender=sender, recipients=recipients)
        msg.body = text_body
        msg.html = html_body
        mail.send(msg)


def order_confirmation(user, req):
    requested_products = RequestedProducts.query.filter_by(request_id=req.id).all()
    discount = 0
    if current_user.role == USER_ROLES['ROLE_CUSTOMER'] and current_user.customer:
        discount = current_user.customer.base_discount
    total = 0
    pieces = 0
    for rp in requested_products:
        if not rp.product.price_retail:
            rp.product.price_retail = 0
        unrounded_price = rp.product.price_retail * (1.0 - discount)
        rp.customer_price = int(5 * round(float(unrounded_price)/5))
        rp.subtotal = rp.customer_price * rp.quantity
        total += rp.subtotal
        pieces += rp.quantity

    send_email(gettext("Thank you for your order!"),
               ADMINS[0],
               [ADMINS[0], user.email],
               render_template("/mail/order_confirm.txt",
                               requested_products=requested_products,
                               total=total,
                               pieces=pieces),
               render_template("/mail/order_confirm.html",
                               requested_products=requested_products,
                               total=total,
                               pieces=pieces))


def send_delivery_notification_to_customers(maker, products):
    users = User.query.filter_by(role=USER_ROLES['ROLE_CUSTOMER'])\
        .filter_by(delivery_mail_receive=True).all()
    user_mails = [u.email for u in users]

    print "Sending delivery notification mail to following addresses: " +  ' '.join(user_mails)

    send_email("【AxiStoreより】入荷のご案内",
               ADMINS[0],
               user_mails,
               render_template("/mail/delivery_notification_to_customers.txt",
                               maker=maker,
                               products=products),
               render_template("/mail/delivery_notification_to_customers.html",
                               maker=maker,
                               products=products),
               bulk=True)