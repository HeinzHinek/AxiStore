# -*- coding: utf-8 -*-

from flask_wtf import Form
from wtforms import StringField, PasswordField, FloatField, SelectField, IntegerField, FieldList, FormField, \
    HiddenField, FileField, BooleanField, SubmitField, RadioField
from wtforms import validators
from wtforms.fields.html5 import EmailField, TelField
from config import USER_ROLES, LANGUAGES, PRODUCTS_PER_PAGE, PACKAGE_SIZES
from models import Product
from flask.ext.babel import lazy_gettext
import wtforms


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
    desc_CS = StringField('desc_CS', [validators.data_required(),
                                      validators.length(max=300)])
    desc_JP = StringField('desc_CS', [validators.data_required(),
                                      validators.length(max=300)])
    price_unit = FloatField('price_unit', [validators.number_range(min=0)])
    price_retail = FloatField('price_retail', [validators.number_range(min=0)])
    qty_stock = IntegerField('qty_stock', [validators.NumberRange(min=0, max=99999)], default=0)
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

    role = [(str(v), k) for k, v in USER_ROLES.iteritems()]
    role = SelectField(lazy_gettext('User role'), choices=role)
    customer = SelectField('Customer', coerce=int)

    inv_lang = dict((v, k) for k, v in LANGUAGES.items())
    lang = [(v, k) for k, v in inv_lang.iteritems()]
    language = SelectField(lazy_gettext('User language'), choices=lang)


class EditUserForm(Form):
    nickname = StringField(lazy_gettext('User nickname'), [validators.data_required(),
                                        validators.length(max=64)])
    email = EmailField(lazy_gettext('Email'), [validators.data_required(),
                                 validators.length(max=120)])

    role = [(str(v), k) for k, v in USER_ROLES.iteritems()]
    role = SelectField(lazy_gettext('User role'), choices=role)
    customer = SelectField('Customer', coerce=int)

    inv_lang = dict((v, k) for k, v in LANGUAGES.items())
    lang = [(v, k) for k, v in inv_lang.iteritems()]
    language = SelectField(lazy_gettext('User language'), choices=lang)


class AddMakerForm(Form):
    name = StringField('name', [validators.data_required(),
                                validators.length(max=50)])
    category = SelectField('category', coerce=int)


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
    maker = SelectField('maker', coerce=int)


class OrderNumberForm(Form):
    order_no = IntegerField('order_no', [validators.data_required, validators.NumberRange(min=0, max=99999)])
    maker = SelectField('maker', coerce=int)


class SelectOrderNumberFormAxm(Form):
    order = SelectField()


class AddCustomerForm(Form):
    name = StringField('name', [validators.data_required(),
                                validators.length(max=50)])
    email = EmailField('email', [validators.data_required(),
                                 validators.length(max=120)])
    base_discount = IntegerField('base_discount', [validators.input_required(),
                                                   validators.NumberRange(min=0, max=100)])
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


class CartOrderForm(Form):
    submit = SubmitField(lazy_gettext('Submit'))