from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
ordered_goods = Table('ordered_goods', pre_meta,
    Column('order_id', Integer),
    Column('product_id', Integer),
    Column('quantity', Integer),
)

orderedproducts = Table('orderedproducts', post_meta,
    Column('order_id', Integer, primary_key=True, nullable=False),
    Column('product_id', Integer, primary_key=True, nullable=False),
    Column('quantity', Integer, default=ColumnDefault(1)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['ordered_goods'].drop()
    post_meta.tables['orderedproducts'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['ordered_goods'].create()
    post_meta.tables['orderedproducts'].drop()
