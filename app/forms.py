# -*- coding: utf-8 -*-

from flask_wtf import Form
from wtforms import StringField, PasswordField, FloatField, SelectField, IntegerField, FieldList, FormField, \
    HiddenField, FileField, BooleanField, SubmitField, DateTimeField, TextAreaField
from wtforms import validators
from wtforms.fields.html5 import EmailField, TelField
from config import USER_ROLES, LANGUAGES, PRODUCTS_PER_PAGE, PACKAGE_SIZES
from models import Product
from flask.ext.babel import lazy_gettext
import wtforms
import operator


class LoginForm(Form):
    nickname = StringField('nickname', [validators.data_required()])
    password = PasswordField('password', [validators.data_required(),
                                          validators.length(min=5, max=30)])
    #remember_me = BooleanField('remember_me', default=False)


class UserForm(Form):
    nickname = StringField(lazy_gettext('Nickname'), [validators.data_required(),
                                                      validators.length(min=5, max=30)])
    email = EmailField(lazy_gettext('Email'), [validators.data_required(),
                                 validators.length(max=120)])
    delivery_mail_receive = BooleanField(lazy_gettext('Email notification of new goods arrival'), default=True)
    inv_lang = dict((v, k) for k, v in LANGUAGES.items())
    lang = [(v, k) for k, v in inv_lang.iteritems()]
    language = SelectField(lazy_gettext('Preferred language'), choices=lang)
    products_per_page = IntegerField(lazy_gettext('Number of products displayed per page'), [validators.NumberRange(min=3)],
                                     default=PRODUCTS_PER_PAGE)


class PasswordChangeForm(Form):
    old_password = PasswordField(lazy_gettext('Old password'),
                                 [validators.data_required(),
                                  validators.length(min=5, max=30)])
    new_password = PasswordField(lazy_gettext('New password'),
                                 [validators.data_required(),
                                  validators.length(min=5, max=30),
                                  validators.equal_to('new_password_confirm',
                                                      message=lazy_gettext('New password must match confirmation!'))])
    new_password_confirm = PasswordField(lazy_gettext('New password confirmation'),
                                         [validators.data_required(),
                                          validators.length(min=5, max=30)])


class SearchForm(Form):
    search = StringField('search', [validators.length(min=2)])


class AddProductForm(Form):
    code = StringField('code', [validators.data_required(),
                                validators.length(min=3, max=20)])
    maker = SelectField('maker', coerce=int)
    maker_code = StringField('maker_code', [validators.length(max=300)])
    desc_CS = StringField('desc_CS', [validators.data_required(),
                                      validators.length(max=300)])
    desc_JP = StringField('desc_CS', [validators.data_required(),
                                      validators.length(max=300)])

    long_desc = TextAreaField('long_desc', [validators.length(max=5000)])
    detailed_desc = TextAreaField('detailed_desc', [validators.length(max=5000)])
    subcategory_desc = TextAreaField('subcategory_desc', [validators.length(max=5000)])
    keywords = StringField('keywords', [validators.length(max=1000)])

    price_unit = FloatField('price_unit', [validators.number_range(min=0)])
    price_retail = FloatField('price_retail', [validators.number_range(min=0)])
    qty_stock = IntegerField('qty_stock', [validators.NumberRange(min=0, max=99999)], default=0)
    limited_flg = BooleanField('limited', default=False)
    axm_node = StringField('axm_node', [validators.length(max=300)])

    sizes = []
    sizes.append(['', lazy_gettext('(unknown)')])
    for k, v in PACKAGE_SIZES.iteritems():
        if v == 0:
            sizes.append([str(v), lazy_gettext('Envelope')])
        elif v == 1:
            sizes.append([str(v), lazy_gettext('YuPack')])
        elif v == 2:
            sizes.append([str(v), lazy_gettext('Box')])
        else:
            sizes.append([str(v), k])
    package_size = SelectField(lazy_gettext('Package size'), choices=sizes, coerce=str)

    #for validation
    request = None

    def validate_code(self, field):
        product = Product.query.filter_by(code=field.data).first()
        if product:
            #error only if not original code of product
            if self.request and (product.code == self.request.form['orig_code']):
                pass
            else:
                pass
                #raise ValidationError(lazy_gettext('This product code is already in use!'))


class AddUserForm(Form):
    nickname = StringField(lazy_gettext('User nickname'), [validators.data_required(),
                                        validators.length(max=64)])
    password = PasswordField(lazy_gettext('User password'), [validators.data_required(),
                                          validators.length(min=5, max=30),
                                          validators.EqualTo('confirm', message=lazy_gettext('Passwords must match'))])
    confirm = PasswordField(lazy_gettext('Password confirmation'))
    email = EmailField(lazy_gettext('Email'), [validators.data_required(),
                                 validators.length(max=120)])

    role = [(str(v), k) for k, v in iter(sorted(USER_ROLES.iteritems(), key=operator.itemgetter(1)))]
    role = SelectField(lazy_gettext('User role'), choices=role)
    customer = SelectField('Customer', coerce=int)
    maker = SelectField('Maker', coerce=int)

    inv_lang = dict((v, k) for k, v in LANGUAGES.items())
    lang = [(v, k) for k, v in inv_lang.iteritems()]
    language = SelectField(lazy_gettext('User language'), choices=lang)


class EditUserForm(Form):
    nickname = StringField(lazy_gettext('User nickname'), [validators.data_required(),
                                        validators.length(max=64)])
    email = EmailField(lazy_gettext('Email'), [validators.data_required(),
                                 validators.length(max=120)])

    role = [(str(v), k) for k, v in iter(sorted(USER_ROLES.iteritems(), key=operator.itemgetter(1)))]
    role = SelectField(lazy_gettext('User role'), choices=role)
    customer = SelectField('Customer', coerce=int)
    maker = SelectField('Maker', coerce=int)

    inv_lang = dict((v, k) for k, v in LANGUAGES.items())
    lang = [(v, k) for k, v in inv_lang.iteritems()]
    language = SelectField(lazy_gettext('User language'), choices=lang)


class AddMakerForm(Form):
    name = StringField(lazy_gettext('Name'), [validators.data_required(),
                                validators.length(max=50)])
    category = SelectField(lazy_gettext('Category'), coerce=int)
    email = EmailField(lazy_gettext('Email'), [validators.length(max=120)])
    standard_delivery_days = IntegerField(lazy_gettext('Average days to deliver'),
                                          [validators.NumberRange(min=0, max=200)],
                                          default=14)


class AddCategoryForm(Form):
    name_CS = StringField('name_CS', [validators.data_required(),
                                      validators.length(max=50)])
    name_JP = StringField('name_JP', [validators.data_required(),
                                      validators.length(max=50)])


class EditQtyStockForm(Form):
    qty_stock = IntegerField('qty_stock', [validators.input_required(),
                                           validators.NumberRange(min=0, max=99999)])


class SelectMakerForm(Form):
    maker = SelectField('maker', coerce=int)


class ProductQuantityWithHiddenForm(wtforms.Form):
    qty_order = IntegerField('qty_order', [validators.NumberRange(min=0, max=99999)], default=0)
    product_id = HiddenField('product_id')


class ProductQuantityForm(Form):
    fields = FieldList(FormField(ProductQuantityWithHiddenForm))


class UploadForm(Form):
    filename = FileField()


class SelectCustomerForm(Form):
    customer = SelectField('customer', coerce=int)
    datetime = DateTimeField('datetime', [validators.data_required()])
    maker = SelectField('maker', coerce=int)


class OrderNumberForm(Form):
    order_no = IntegerField('order_no', [validators.data_required, validators.NumberRange(min=0, max=99999)])
    datetime = DateTimeField('datetime', [validators.data_required()])
    payments = [(1, lazy_gettext('Bank transfer')), (2, lazy_gettext('PayPal')), (3, lazy_gettext('On delivery'))]
    payment_method = SelectField('payment_method', choices=payments, coerce=int)
    flg_options = [(0, lazy_gettext('No')), (1, lazy_gettext('Yes'))]
    paid_for_flg = SelectField('paid_for', choices=flg_options, coerce=int)
    maker = SelectField('maker', coerce=int)


class SelectOrderNumberFormAxm(Form):
    order = SelectField()


class EditDateTimeForm(Form):
    datetime = DateTimeField('datetime', [validators.data_required()])


class AddCustomerForm(Form):
    name = StringField('name', [validators.data_required(),
                                validators.length(max=50)])
    email = EmailField('email', [validators.data_required(),
                                 validators.length(max=120)])
    base_discount = IntegerField('base_discount', [validators.input_required(),
                                                   validators.NumberRange(min=0, max=100)])
    next_nohinsho_letter = StringField('next_nohinsho_letter', default='A')
    recommender = SelectField(lazy_gettext('Recommender'), coerce=int)
    company_name = StringField('company_name', [validators.data_required(),
                                validators.length(max=100)])
    post_code1 = StringField('post_code1', [validators.length(max=3),
                                             validators.Regexp('^([0-9][0-9][0-9])?$')])
    post_code2 = StringField('post_code2', [validators.length(max=4),
                                             validators.Regexp('^([0-9][0-9][0-9][0-9])?$')])
    address1 = StringField('address1', [validators.length(max=100)])
    address2 = StringField('address2', [validators.length(max=100)])
    address3 = StringField('address3', [validators.length(max=100)])



class AddContactForm(Form):
    first_name = StringField('first_name', [validators.length(max=50)])
    surname = StringField('surname', [validators.length(max=50)])
    phone = TelField('phone', [validators.length(max=16)])
    email = EmailField('email', [validators.data_required(),
                                 validators.length(max=120)])

    customer = SelectField('customer', coerce=int)


class ShopHeaderForm(Form):
    category = SelectField(lazy_gettext('Category'), coerce=int)
    available_only = BooleanField(lazy_gettext('Available item only'))
    search = StringField(lazy_gettext('Search'), [validators.length(min=2)])


class SimpleSubmitForm(Form):
    submit = SubmitField(lazy_gettext('Submit'))


class EditSupplyForm(Form):
    qty_supplied = IntegerField('qty_supplied')
    add_qty_to_stock = BooleanField('add_qty_to_stock', default=True)
    add_qty_to_requests = BooleanField('add_qty_to_requests', default=True)
    submit = SubmitField(lazy_gettext('Submit'))


class EditDeliveryForm(Form):
    qty_delivered = IntegerField('qty_delivered')
    subtract_qty_from_stock = BooleanField('subtract_qty_to_stock', default=True)
    add_qty_to_orders = BooleanField('add_qty_to_orders', default=True)
    submit = SubmitField(lazy_gettext('Submit'))


class EditRequestForm(Form):
    qty_requested = IntegerField('qty_requested')
    submit = SubmitField(lazy_gettext('Submit'))


class EditOrderForm(Form):
    qty_ordered = IntegerField('qty_ordered')
    submit = SubmitField(lazy_gettext('Submit'))