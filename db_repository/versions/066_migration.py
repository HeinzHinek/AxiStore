from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
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
    Column('company_name', String(length=100)),
    Column('post_code', Integer),
    Column('address1', String(length=100)),
    Column('address2', String(length=100)),
    Column('address3', String(length=100)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['customer'].columns['address1'].create()
    post_meta.tables['customer'].columns['address2'].create()
    post_meta.tables['customer'].columns['address3'].create()
    post_meta.tables['customer'].columns['company_name'].create()
    post_meta.tables['customer'].columns['post_code'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['customer'].columns['address1'].drop()
    post_meta.tables['customer'].columns['address2'].drop()
    post_meta.tables['customer'].columns['address3'].drop()
    post_meta.tables['customer'].columns['company_name'].drop()
    post_meta.tables['customer'].columns['post_code'].drop()
