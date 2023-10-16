import datetime
from datetime import timedelta

from sqlalchemy.sql.schema import MetaData
from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
    ForeignKey,
    SmallInteger,
    TypeDecorator,
    DateTime as DT,
    Interval as IT,
    Boolean,
    Index
)

class PrismTimeDelta(TypeDecorator):
    impl = IT
    cache_ok = True

    def process_literal_param(self, value, _) -> None:
        v = str(value).replace(", 0:00:00", "")
        return "interval '" + v + "'"


class PrismDateTime(TypeDecorator):
    impl = DT
    cache_ok = True

    def coerce_compared_value(self, op, value):
        if isinstance(value, timedelta):
            return PrismTimeDelta()
        else:
            return self

    def process_literal_param(self, value, _) -> None:
        return str(value).replace(" 00:00:00", "")


metadata = MetaData()

dataqueries = Table(
    'dataqueries',
    metadata,
    Column('dataqueryid', Integer, primary_key=True, autoincrement=True),
    Column('version', Integer, primary_key=True, autoincrement=False),
    Column('path', String),
    Column('dataqueryname', String),
    Column('username', String, ForeignKey('users.username'), nullable=False),
    Column('dataquerybody', String, nullable=False),
    Column('currentflag', SmallInteger),
    Column('lastmodified', PrismDateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow),
    Column('createdtime', PrismDateTime, default=datetime.datetime.utcnow),
    Column('shared', Boolean, default=False),
    Column('accountid', ForeignKey('accounts.accountid'), nullable=False),
    Index('idx_dataqueries_username', 'username'),
    Index('idx_dataqueries_username_path_currentflag', 'username', 'path', 'currentflag'),
)
