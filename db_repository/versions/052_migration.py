from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
contact = Table('contact', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('company_name', String(length=100)),
    Column('post_code', Integer),
    Column('address1', String(length=100)),
    Column('address2', String(length=100)),
    Column('address3', String(length=100)),
    Column('phone', Integer),
    Column('email', String(length=120)),
)

customer = Table('customer', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=50)),
    Column('first_name', String(length=50)),
    Column('surname', String(length=50)),
    Column('customer_type', SmallInteger, default=ColumnDefault(0)),
    Column('order_no', Integer),
    Column('contact_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['contact'].create()
    post_meta.tables['customer'].columns['contact_id'].create()
    post_meta.tables['customer'].columns['first_name'].create()
    post_meta.tables['customer'].columns['surname'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['contact'].drop()
    post_meta.tables['customer'].columns['contact_id'].drop()
    post_meta.tables['customer'].columns['first_name'].drop()
    post_meta.tables['customer'].columns['surname'].drop()
