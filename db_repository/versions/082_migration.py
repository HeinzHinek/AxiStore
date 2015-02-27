from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
migration_tmp = Table('migration_tmp', pre_meta,
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
    Column('delivery_mail_receive', Boolean),
)

customer = Table('customer', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=50)),
    Column('email', String(length=120)),
    Column('customer_type', SmallInteger, default=ColumnDefault(0)),
    Column('order_no', Integer),
    Column('base_discount', Float),
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
    pre_meta.tables['migration_tmp'].drop()
    post_meta.tables['customer'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['migration_tmp'].create()
    post_meta.tables['customer'].drop()
