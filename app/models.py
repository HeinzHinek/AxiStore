# -*- coding: utf-8 -*-

from app import db
from config import USER_ROLES
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

    @hybrid_property
    def order_qty(self):
        oq = db.session.query(func.sum(OrderedProducts.quantity - OrderedProducts.qty_delivered).label('quantity'))\
            .filter(Order.active_flg==True)\
            .filter_by(product_id=self.id).one()
        if not oq.quantity:
            oq.quantity = 0
        return oq.quantity


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
