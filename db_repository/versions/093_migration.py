from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
request = Table('request', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('created_dt', DateTime),
    Column('user_id', Integer),
    Column('customer_id', Integer),
    Column('payment_method', Integer),
    Column('paid_for_flg', Boolean, default=ColumnDefault(False)),
    Column('active_flg', Boolean, default=ColumnDefault(True)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['request'].columns['payment_method'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['request'].columns['payment_method'].drop()
