from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
product = Table('product', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('code', String),
    Column('desc_CS', String),
    Column('desc_JP', String),
    Column('price_unit', Integer),
    Column('price_retail', Integer),
    Column('active_flg', Boolean),
    Column('maker_id', Integer),
    Column('category_id', Integer),
    Column('qty_stock', Integer),
    Column('axm_node', String),
    Column('package_size', Integer),
    Column('maker_code', String),
    Column('maker_qty_stock', Integer),
    Column('created_dt', DateTime),
    Column('min_stock_limit', Integer),
    Column('limited_flg', Boolean),
    Column('keywords', String),
    Column('long_desc', String),
    Column('subcategory_1', String),
    Column('subcategory_2', String),
    Column('subcategory_3', String),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['product'].columns['subcategory_1'].drop()
    pre_meta.tables['product'].columns['subcategory_2'].drop()
    pre_meta.tables['product'].columns['subcategory_3'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['product'].columns['subcategory_1'].create()
    pre_meta.tables['product'].columns['subcategory_2'].create()
    pre_meta.tables['product'].columns['subcategory_3'].create()
