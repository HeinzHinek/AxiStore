from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
product = Table('product', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('code', String(length=20)),
    Column('category_id', Integer),
    Column('maker_id', Integer),
    Column('desc_CS', Unicode(length=300)),
    Column('desc_JP', Unicode(length=300)),
    Column('price_unit', Integer, default=ColumnDefault(0)),
    Column('price_retail', Integer, default=ColumnDefault(0)),
    Column('qty_stock', Integer),
    Column('axm_node', Unicode(length=300)),
    Column('package_size', Integer),
    Column('maker_code', String(length=20)),
    Column('maker_qty_stock', Integer),
    Column('active_flg', Boolean, default=ColumnDefault(True)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['product'].columns['maker_code'].create()
    post_meta.tables['product'].columns['maker_qty_stock'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['product'].columns['maker_code'].drop()
    post_meta.tables['product'].columns['maker_qty_stock'].drop()
