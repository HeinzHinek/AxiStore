from flask.ext.mail import Message
from app import mail
from flask import render_template
from flask_login import current_user
from config import ADMINS, USER_ROLES
from models import RequestedProducts
from flask.ext.babel import gettext


def send_email(subject, sender, recipients, text_body, html_body):
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