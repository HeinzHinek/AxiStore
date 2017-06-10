# -*- coding: utf-8 -*-
from flask import abort
from functools import wraps
from flask_login import current_user, login_required as flask_login_required
from config import USER_ROLES


def login_required(func):
    @flask_login_required
    @wraps(func)
    def inner(*args, **kwargs):
        cust_ok = False
        maker_ok = False

        if 'customer_ok' in kwargs:
            del kwargs['customer_ok']
            cust_ok = True
        if 'maker_ok' in kwargs:
            del kwargs['maker_ok']
            maker_ok = True
        if current_user.is_authenticated() and current_user.role == USER_ROLES['ROLE_CUSTOMER']:
            if not cust_ok:
                abort(403)
        if current_user.is_authenticated() and current_user.role == USER_ROLES['ROLE_MAKER']:
            if not maker_ok:
                abort(403)

        return func(*args, **kwargs)
    return inner


def customer_allowed(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        return func(customer_ok=True, *args, **kwargs)

    return decorated_view


def maker_allowed(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        return func(maker_ok=True, *args, **kwargs)

    return decorated_view
