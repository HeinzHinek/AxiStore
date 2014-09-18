from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
deliveredproducts = Table('deliveredproducts', post_meta,
    Column('delivery_id', Integer, primary_key=True, nullable=False),
    Column('product_id', Integer, primary_key=True, nullable=False),
    Column('quantity', Integer, default=ColumnDefault(1)),
)

delivery = Table('delivery', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('created_dt', DateTime),
    Column('user_id', Integer),
    Column('maker_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['deliveredproducts'].create()
    post_meta.tables['delivery'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['deliveredproducts'].drop()
    post_meta.tables['delivery'].drop()
