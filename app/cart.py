# -*- coding: utf-8 -*-

__author__ = 'Hinek'

from models import Product

class Cart():

    def __init__(self):
        self.products = []

    def add_to_cart(self, id, qty=1, discount=0):
        product = Product.query.filter_by(id=id).first()
        if product:
            for p in self.products:
                if p.id == product.id:
                    p.cart_qty += int(qty)
                    p.subtotal = int(p.customer_price) * int(p.cart_qty)
                    break
            else:
                product.cart_qty = int(qty)
                base_price = product.price_retail if product.price_retail else 0
                unrounded_price = base_price * (1.0 - discount)
                product.customer_price = int(5 * round(float(unrounded_price)/5))
                product.subtotal = int(product.customer_price) * int(product.cart_qty)
                self.products.append(product)
            return id
        return None

    def remove_from_cart(self, id):
        for p in self.products:
            if p.id == int(id):
                self.products.remove(p)
                return self
        return None

    def get_product_count(self):
        return len(self.products)