from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
customer = Table('customer', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String),
    Column('customer_type', SmallInteger),
    Column('order_no', Integer),
    Column('contact_id', Integer),
    Column('first_name', String),
    Column('surname', String),
    Column('email', String),
    Column('phone', Integer),
    Column('base_discount', Float),
)

contact = Table('contact', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('company_name', String),
    Column('post_code', Integer),
    Column('address1', String),
    Column('address2', String),
    Column('address3', String),
    Column('phone', Integer),
    Column('email', String),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['customer'].columns['phone'].drop()
    pre_meta.tables['contact'].columns['phone'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['customer'].columns['phone'].create()
    pre_meta.tables['contact'].columns['phone'].create()
