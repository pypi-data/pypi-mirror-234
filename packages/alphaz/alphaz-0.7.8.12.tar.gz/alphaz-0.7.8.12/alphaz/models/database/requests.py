import datetime
from sqlalchemy import (
    Table,
    Column,
    ForeignKey,
    Integer,
    String,
    Text,
    DateTime,
    UniqueConstraint,
    Float,
    BLOB,
)
from .models import (
    AlphaTable,
    AlphaTableId,
    AlphaColumn,
    AlphaFloat,
    AlphaInteger,
    AlphaTableIdUpdateDate,
    AlphaTableUpdateDate,
)

from core import core, DB


class Requests(DB.Model, AlphaTableIdUpdateDate):
    __bind_key__ = "MAIN"
    __tablename__ = "requests"

    uuid = AlphaColumn(String(100))
    process = AlphaColumn(Integer, primary_key=True)
    message = AlphaColumn(Text, primary_key=True)
    message_type = AlphaColumn(String(20))
    lifetime = AlphaColumn(Integer)
    creation_date = AlphaColumn(DateTime, default=datetime.datetime.now)


class Answers(DB.Model, AlphaTableIdUpdateDate):
    __bind_key__ = "MAIN"
    __tablename__ = "answers"

    uuid = AlphaColumn(String(100))
    process = AlphaColumn(Integer, primary_key=True)
    message = AlphaColumn(Text, primary_key=True)
    message_type = AlphaColumn(String(20))
    lifetime = AlphaColumn(Integer)
    creation_date = AlphaColumn(DateTime, default=datetime.datetime.now)
