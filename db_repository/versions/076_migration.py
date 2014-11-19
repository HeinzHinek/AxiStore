from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
catalog = Table('catalog', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('super_id', Integer),
    Column('name_CS', String(length=50)),
    Column('name_JP', String(length=50)),
    Column('order', Integer),
)

catalogedproducts = Table('catalogedproducts', post_meta,
    Column('catalog_id', Integer, primary_key=True, nullable=False),
    Column('product_id', Integer, primary_key=True, nullable=False),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['catalog'].create()
    post_meta.tables['catalogedproducts'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['catalog'].drop()
    post_meta.tables['catalogedproducts'].drop()
