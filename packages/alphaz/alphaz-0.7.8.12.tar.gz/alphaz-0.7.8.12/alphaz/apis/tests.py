"""Tests methods for api."""

import datetime

from ..models.database.main_definitions import Test
from core import core

DB = core.db


def insert():
    """insert test.

    Raises:
        ex: [description]
    Raises:
        ex: [description]

    Returns:
        [type]: [description]
    """
    test = Test(name="name", number=0, text="text", date=datetime.datetime.now())

    try:
        added_test = DB.add(test)
    except Exception as ex:
        raise ex

    return DB.select(
        Test, filters=[Test.name == "name"], first=True, order_by=Test.date_.desc()
    )
