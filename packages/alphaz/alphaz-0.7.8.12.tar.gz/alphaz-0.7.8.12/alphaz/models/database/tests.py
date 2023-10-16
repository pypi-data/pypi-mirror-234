import datetime
from sqlalchemy.orm import relationship

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
    AlphaTablePrimaryIdUpdateDate,
)

from core import core, DB


class TestChild(DB.Model, AlphaTablePrimaryIdUpdateDate):
    __bind_key__ = "MAIN"
    __tablename__ = "test_child"

    name = AlphaColumn("name_", String(30))
    text = AlphaColumn("text_", String(300))
    number = AlphaColumn("number_", Integer)
    date = AlphaColumn("date_", DateTime)


class Test(DB.Model):
    __bind_key__ = "MAIN"
    __tablename__ = "test"

    id = AlphaColumn(Integer, primary_key=True)

    name = AlphaColumn("name_", String(30))
    text = AlphaColumn("text_", String(300))
    number = AlphaColumn("number_", Integer)
    date = AlphaColumn("date_", DateTime)

    test_child_id = AlphaColumn(Integer, ForeignKey("test_child.id"), nullable=True)
    test_child = relationship("TestChild", cascade="all, delete")

    update_date = AlphaColumn(
        DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now
    )


class TestChilds(DB.Model, AlphaTableIdUpdateDate):
    __bind_key__ = "MAIN"
    __tablename__ = "test_childs"

    id = AlphaColumn(Integer, autoincrement=True)

    parent_id = AlphaColumn(
        Integer,
        ForeignKey("test.id"),
        nullable=False,
    )
    child_parent_id = AlphaColumn(
        Integer,
        ForeignKey("test_child.id"),
        nullable=False,
    )

    name = AlphaColumn("name_", String(30), primary_key=True)
    text = AlphaColumn("text_", String(300))
    number = AlphaColumn("number_", Integer)
    date = AlphaColumn("date_", DateTime)

    parent = relationship("Test", backref="test_childs", cascade="all, delete")
