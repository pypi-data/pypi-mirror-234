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

from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship, backref


from .models import (
    AlphaTable,
    AlphaTableId,
    AlphaColumn,
    AlphaFloat,
    AlphaInteger,
    AlphaTableIdUpdateDate,
    AlphaTableUpdateDate,
)
from .tests import Test, TestChild, TestChilds
import datetime

from core import core, DB

ma = core.ma


class Constants(DB.Model, AlphaTableUpdateDate):
    __tablename__ = "constants"
    __bind_key__ = "MAIN"

    name = AlphaColumn(String(30), primary_key=True)
    type = AlphaColumn(String(10))
    value = AlphaColumn(String(100))


class Parameters(DB.Model, AlphaTableUpdateDate):
    __tablename__ = "parameters"
    __bind_key__ = "MAIN"

    name = AlphaColumn(String(30), primary_key=True)
    value = AlphaColumn(Text)


class Configs(DB.Model, AlphaTableUpdateDate):
    __tablename__ = "configs"
    __bind_key__ = "MAIN"

    name = AlphaColumn(String(30), primary_key=True)
    type = AlphaColumn(String(10))
    value = AlphaColumn(Text)
