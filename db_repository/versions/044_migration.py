from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
customer = Table('customer', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=50)),
    Column('company_flg', Boolean),
)

request = Table('request', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('created_dt', DateTime),
    Column('user_id', Integer),
    Column('customer_id', Integer),
    Column('active_flg', Boolean, default=ColumnDefault(True)),
)

requestedproducts = Table('requestedproducts', post_meta,
    Column('request_id', Integer, primary_key=True, nullable=False),
    Column('product_id', Integer, primary_key=True, nullable=False),
    Column('quantity', Integer, default=ColumnDefault(1)),
    Column('qty_supplied', Integer, default=ColumnDefault(0)),
)

suppliedproducts = Table('suppliedproducts', post_meta,
    Column('supply_id', Integer, primary_key=True, nullable=False),
    Column('product_id', Integer, primary_key=True, nullable=False),
    Column('quantity', Integer, default=ColumnDefault(1)),
)

supply = Table('supply', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('created_dt', DateTime),
    Column('user_id', Integer),
    Column('customer_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['customer'].create()
    post_meta.tables['request'].create()
    post_meta.tables['requestedproducts'].create()
    post_meta.tables['suppliedproducts'].create()
    post_meta.tables['supply'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['customer'].drop()
    post_meta.tables['request'].drop()
    post_meta.tables['requestedproducts'].drop()
    post_meta.tables['suppliedproducts'].drop()
    post_meta.tables['supply'].drop()
