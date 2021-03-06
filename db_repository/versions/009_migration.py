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
)

product = Table('product', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('code', String(length=20)),
    Column('maker', Integer),
    Column('desc_CS', String(length=300)),
    Column('desc_JP', String(length=300)),
    Column('price_unit', Integer, default=ColumnDefault(0)),
    Column('price_retail', Integer, default=ColumnDefault(0)),
    Column('active_flg', Boolean),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['product'].columns['maker_id'].drop()
    post_meta.tables['product'].columns['maker'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['product'].columns['maker_id'].create()
    post_meta.tables['product'].columns['maker'].drop()
