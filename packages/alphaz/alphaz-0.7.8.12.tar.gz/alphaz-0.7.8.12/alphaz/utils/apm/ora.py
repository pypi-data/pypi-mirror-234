import re
from elasticapm.instrumentation.packages.dbapi2 import (
    ConnectionProxy,
    CursorProxy,
    DbApi2Instrumentation,
    extract_signature,
)
from elasticapm.instrumentation import register
from elasticapm.utils import default_ports


def get_dsn_match(dsn: str, name: str, default=None) -> str:
    matchs = re.findall(f"{name}\s*=\s*([^\)]*)\)", dsn)
    return matchs[0] if len(matchs) != 0 else default


class OracleCursorProxy(CursorProxy):
    provider_name = "oracle"

    def extract_signature(self, sql):
        return extract_signature(sql)

    @property
    def _self_database(self) -> str:
        # for unknown reasons, the connection is available as the `_connection` attribute on Python 3.6,
        # and as `_cnx` on later Python versions
        dsn = self.connection.dsn if hasattr(self, "connection") else ""
        return get_dsn_match(dsn, "SID")
        # connection = getattr(self, "_cnx") or getattr(self, "_connection")
        # return connection.database if connection else ""


class OracleConnectionProxy(ConnectionProxy):
    cursor_proxy = OracleCursorProxy


class OracleInstrumentation(DbApi2Instrumentation):
    name = "oracle"

    instrument_list = [("cx_Oracle", "connect")]

    def call(self, module, method, wrapped, instance, args, kwargs):
        dsn = kwargs.get("dsn", "")
        destination_info = {
            "address": get_dsn_match(dsn, "HOST"),
            "port": int(get_dsn_match(dsn, "PORT", 0)),
        }
        return OracleConnectionProxy(
            wrapped(*args, **kwargs), destination_info=destination_info
        )


register.register("alphaz.utils.apm.ora.OracleInstrumentation")
