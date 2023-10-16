# MODULES
import sqlalchemy
from pathlib import Path

# CORE
from core import core

# MODELS
from ...models.database.users_definitions import Application
from ...models.tests import Levels
from ...models.database.tests import Test

# UTILS
from ...utils.api import route, Parameter

# LIBS
from ...libs import test_lib, io_lib, database_lib

# LOCALS
from .database import DB_INIT_PARAMETERS

API = core.api

TESTS_PARAMETERS = [
    Parameter("category", ptype=str),
    Parameter("categories", ptype=list),
    Parameter("group", ptype=str),
    Parameter("groups", ptype=list),
    Parameter("name", ptype=str),
    Parameter("names", ptype=list),
    Parameter("run", ptype=bool),
    Parameter("file_path", ptype=str),
    Parameter("coverage", ptype=str),
    Parameter("load_from_db", ptype=bool),
    Parameter("stop", ptype=bool),
    Parameter("report", ptype=str),
    Parameter("coverage", ptype=str),
    Parameter("levels", ptype=list[Levels], default=[]),
    Parameter("failed_only", ptype=bool),
]


@route(
    "/tests",
    parameters=[
        *TESTS_PARAMETERS,
        *DB_INIT_PARAMETERS,
    ],
)
def get_tests():
    database_lib.init_databases(
        core, **API.gets(without=[p.name for p in TESTS_PARAMETERS])
    )
    return test_lib.get_tests_auto(
        **API.gets(without=[p.name for p in DB_INIT_PARAMETERS])
    )


@route("/tests/coverage", parameters=[Parameter("file", required=True)])
def get_coverage_file():
    coverages = io_lib.unarchive_object(API["file"])
    return coverages


def test_null(update_date=None):
    return core.db.select(
        Application, optional_filters=[Application.update_date == update_date]
    )


@route(
    "/test/null",
    parameters=[
        Parameter(
            "update_date",
            required=False,
            none_value=sqlalchemy.null(),
        )
    ],
)
def test():
    return test_null(**API.get_parameters())


@route("/test/select", pagination=True)
def select_test():
    return core.db.select(Test, **API.gets())


@route("/test/download")
def generate_pdf() -> None:
    from fpdf import FPDF

    directory = core.config.get("directories/tmp")
    wd_path = Path(directory)
    file_path = wd_path / "test"
    file_name = f"test.pdf"
    pdf = FPDF(unit="mm", format="A4")
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)

    # Écrire un titre
    pdf.cell(0, 10, "Page de test", 0, 1, "C")

    # Définir la police et la taille du texte pour le contenu
    pdf.set_font("Arial", "", 12)

    # Écrire un paragraphe
    lorem_ipsum = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec at tincidunt lorem, ut tempus felis. In hac habitasse platea dictumst. Nulla hendrerit, justo id congue placerat, tellus ante ullamcorper ex, eget aliquet enim nisl sit amet orci. Morbi efficitur dolor sed metus rhoncus, a feugiat tortor pulvinar. Mauris ultrices gravida faucibus. Proin fermentum mi a erat efficitur malesuada. Morbi in purus eget lectus feugiat rhoncus. Suspendisse egestas tincidunt metus, sed consectetur turpis aliquet in."

    pdf.multi_cell(0, 10, lorem_ipsum)
    pdf.output(file_path / file_name, "F")
    API.get_file(directory=file_path, filename=file_name)
