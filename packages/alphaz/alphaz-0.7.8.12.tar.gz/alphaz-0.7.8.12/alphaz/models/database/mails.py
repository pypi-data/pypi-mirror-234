import ujson
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

# MODELS
from .models import (
    AlphaTable,
    AlphaTableId,
    AlphaColumn,
    AlphaFloat,
    AlphaInteger,
    AlphaTableIdUpdateDate,
    AlphaTableUpdateDate,
)

# LIBS
from ...libs.string_lib import create_hash


from core import core, DB

ma = core.ma


def _parameters_to_string(parameters):
    return ";".join([str(x) for x in parameters.values()])


class NewsLetter(DB.Model, AlphaTableIdUpdateDate):
    __bind_key__ = "MAIN"
    __tablename__ = "newsletter"
    name = AlphaColumn(String(100), primary_key=True)
    mail = AlphaColumn(String(50), primary_key=True)


class MailHistory(DB.Model, AlphaTableIdUpdateDate):
    __bind_key__ = "MAIN"
    __tablename__ = "mail_history"

    uuid = AlphaColumn(String(50), primary_key=True)
    mail_type = AlphaColumn(String(250))
    parameters = AlphaColumn(String(200))
    parameters_full = AlphaColumn(String(500))
    date = AlphaColumn(DateTime)

    hash_key = AlphaColumn(String(64), unique=True, nullable=False)

    def __init__(self, uuid, mail_type, parameters, parameters_full, *args):
        super().__init__(*args)
        self.uuid = uuid
        self.mail_type = mail_type
        self.parameters = ujson.dumps(parameters)
        self.parameters_full = ujson.dumps(parameters_full)
        self.hash_key = create_hash(
            mail_type,
            _parameters_to_string(parameters),
            _parameters_to_string(parameters_full),
        )


class MailBlacklist(DB.Model, AlphaTableId):
    __bind_key__ = "MAIN"
    __tablename__ = "mail_blacklist"
    __table_args__ = (
        UniqueConstraint("mail", "mail_type", name="unique_component_commit"),
    )

    mail = AlphaColumn(String(50), primary_key=True)
    mail_type = AlphaColumn(String(20), primary_key=True)
