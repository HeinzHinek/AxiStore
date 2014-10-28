from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
customer = Table('customer', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String),
    Column('email', String),
    Column('customer_type', SmallInteger),
    Column('order_no', Integer),
    Column('base_discount', Float),
    Column('address1', String),
    Column('address2', String),
    Column('address3', String),
    Column('company_name', String),
    Column('post_code', Integer),
)

customer = Table('customer', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=50)),
    Column('first_name', String(length=50)),
    Column('surname', String(length=50)),
    Column('phone', String(length=16)),
    Column('email', String(length=120)),
    Column('customer_type', SmallInteger, default=ColumnDefault(0)),
    Column('order_no', Integer),
    Column('base_discount', Float),
    Column('contact_id', Integer),
)

contact = Table('contact', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('phone', String),
    Column('email', String),
    Column('first_name', String),
    Column('surname', String),
    Column('customer_id', Integer),
)

contact = Table('contact', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('company_name', String(length=100)),
    Column('post_code', Integer),
    Column('address1', String(length=100)),
    Column('address2', String(length=100)),
    Column('address3', String(length=100)),
    Column('phone', String(length=16)),
    Column('email', String(length=120)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['customer'].columns['address1'].drop()
    pre_meta.tables['customer'].columns['address2'].drop()
    pre_meta.tables['customer'].columns['address3'].drop()
    pre_meta.tables['customer'].columns['company_name'].drop()
    pre_meta.tables['customer'].columns['post_code'].drop()
    post_meta.tables['customer'].columns['contact_id'].create()
    post_meta.tables['customer'].columns['first_name'].create()
    post_meta.tables['customer'].columns['phone'].create()
    post_meta.tables['customer'].columns['surname'].create()
    pre_meta.tables['contact'].columns['customer_id'].drop()
    pre_meta.tables['contact'].columns['first_name'].drop()
    pre_meta.tables['contact'].columns['surname'].drop()
    post_meta.tables['contact'].columns['address1'].create()
    post_meta.tables['contact'].columns['address2'].create()
    post_meta.tables['contact'].columns['address3'].create()
    post_meta.tables['contact'].columns['company_name'].create()
    post_meta.tables['contact'].columns['post_code'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['customer'].columns['address1'].create()
    pre_meta.tables['customer'].columns['address2'].create()
    pre_meta.tables['customer'].columns['address3'].create()
    pre_meta.tables['customer'].columns['company_name'].create()
    pre_meta.tables['customer'].columns['post_code'].create()
    post_meta.tables['customer'].columns['contact_id'].drop()
    post_meta.tables['customer'].columns['first_name'].drop()
    post_meta.tables['customer'].columns['phone'].drop()
    post_meta.tables['customer'].columns['surname'].drop()
    pre_meta.tables['contact'].columns['customer_id'].create()
    pre_meta.tables['contact'].columns['first_name'].create()
    pre_meta.tables['contact'].columns['surname'].create()
    post_meta.tables['contact'].columns['address1'].drop()
    post_meta.tables['contact'].columns['address2'].drop()
    post_meta.tables['contact'].columns['address3'].drop()
    post_meta.tables['contact'].columns['company_name'].drop()
    post_meta.tables['contact'].columns['post_code'].drop()
