# -*- coding: utf-8 -*-

from app import db
from config import USER_ROLES, CUSTOMER_TYPES
from datetime import datetime
from sqlalchemy.sql import func
from sqlalchemy.ext.hybrid import hybrid_property


class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nickname = db.Column(db.String(64), index = True, unique = True)
    password = db.Column(db.String(64))
    email = db.Column(db.String(120), index = True, unique = True)
    role = db.Column(db.SmallInteger, default = USER_ROLES['ROLE_USER'])
    language = db.Column(db.String(3))
    products_per_page = db.Column(db.Integer, default = 20)

    orders = db.relationship('Order', backref='orderer', lazy='dynamic')
    deliveries = db.relationship('Delivery', backref='recipient', lazy='dynamic')
    requests = db.relationship('Request', backref='receiver', lazy='dynamic')
    supplies = db.relationship('Supply', backref='sender', lazy='dynamic')

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % (self.nickname)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    maker_id = db.Column(db.Integer, db.ForeignKey('maker.id'))
    desc_CS = db.Column(db.Unicode(300))
    desc_JP = db.Column(db.Unicode(300))
    price_unit = db.Column(db.Integer, default=0)
    price_retail = db.Column(db.Integer, default=0)
    qty_stock = db.Column(db.Integer)
    active_flg = db.Column(db.Boolean, default=True)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'code': self.code,
            'category_id': self.category_id,
            'maker_id': self.maker_id,
            'maker_name': self.maker.name,
            'desc_CS': self.desc_CS,
            'desc_JP': self.desc_JP,
            'price_unit': self.price_unit,
            'price_retail': self.price_retail,
            'qty_stock': self.qty_stock,
            'active_flg': self.active_flg
        }

    @hybrid_property
    def request_qty(self):
        req_qties = 0
        for ra in self.request_assocs:
            if ra.request.active_flg:
                req_qties += ra.quantity
                req_qties -= ra.qty_supplied
        return req_qties

    @hybrid_property
    def order_qty(self):
        order_qties = 0
        for oa in self.order_assocs:
            if oa.order.active_flg:
                order_qties += oa.quantity
                order_qties -= oa.qty_delivered
        return order_qties

    def customer_request_qty(self, cust_id):
        req_qties = 0
        for ra in self.request_assocs:
            if ra.request.active_flg and ra.request.customer_id == cust_id:
                req_qties += ra.quantity
                req_qties -= ra.qty_supplied
        return req_qties


class Maker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

    products = db.relationship('Product', backref='maker', lazy='dynamic')
    orders = db.relationship('Order', backref='maker', lazy='dynamic')
    deliveries = db.relationship('Delivery', backref='maker', lazy='dynamic')


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_CS = db.Column(db.String(50))
    name_JP = db.Column(db.String(50))
    order = db.Column(db.Integer)

    makers = db.relationship('Maker', backref='category', lazy='dynamic')
    products = db.relationship('Product', backref='category', lazy='dynamic')


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_dt = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    maker_id = db.Column(db.Integer, db.ForeignKey('maker.id'))
    active_flg = db.Column(db.Boolean, default=True)
    products = db.relationship('OrderedProducts', backref='order')

    def __init__(self):
        self.created_dt = datetime.utcnow()

    #check whether order has undelivered products, if not, switch active flg to False
    def check_completely_delivered(self):
        for op in self.products:
            if op.quantity != op.qty_delivered:
                return False
        self.active_flg = False
        return True


class OrderedProducts(db.Model):
    __tablename__ = 'orderedproducts'
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), primary_key=True)
    quantity = db.Column(db.Integer, default=1)
    qty_delivered = db.Column(db.Integer, default=0)
    product = db.relationship('Product', backref='order_assocs')


class Delivery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_dt = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    maker_id = db.Column(db.Integer, db.ForeignKey('maker.id'))
    products = db.relationship('DeliveredProducts',
                               backref='delivery')

    def __init__(self):
        self.created_dt = datetime.utcnow()


class DeliveredProducts(db.Model):
    __tablename__ = 'deliveredproducts'
    delivery_id = db.Column(db.Integer, db.ForeignKey('delivery.id'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), primary_key=True)
    quantity = db.Column(db.Integer, default=1)
    product = db.relationship('Product', backref='delivery_assocs')


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    customer_type = db.Column(db.SmallInteger, default=CUSTOMER_TYPES['TYPE_CUSTOMER'])
    order_no = db.Column(db.Integer)

    requests = db.relationship('Request', backref='customer', lazy='dynamic')
    supplies = db.relationship('Supply', backref='customer', lazy='dynamic')


class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_dt = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    active_flg = db.Column(db.Boolean, default=True)
    products = db.relationship('RequestedProducts', backref='request')

    def __init__(self):
        self.created_dt = datetime.utcnow()

    #check whether request has unsupplied products, if not, switch active flg to False
    def check_completely_supplied(self):
        for rp in self.products:
            if rp.quantity != rp.qty_supplied:
                return False
        self.active_flg = False
        return True


class RequestedProducts(db.Model):
    __tablename__ = 'requestedproducts'
    request_id = db.Column(db.Integer, db.ForeignKey('request.id'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), primary_key=True)
    quantity = db.Column(db.Integer, default=1)
    qty_supplied = db.Column(db.Integer, default=0)
    product = db.relationship('Product', backref='request_assocs')


class Supply(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_dt = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    products = db.relationship('SuppliedProducts',
                               backref='supply')

    def __init__(self):
        self.created_dt = datetime.utcnow()


class SuppliedProducts(db.Model):
    __tablename__ = 'suppliedproducts'
    supply_id = db.Column(db.Integer, db.ForeignKey('supply.id'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), primary_key=True)
    quantity = db.Column(db.Integer, default=1)
    product = db.relationship('Product', backref='supply_assocs')