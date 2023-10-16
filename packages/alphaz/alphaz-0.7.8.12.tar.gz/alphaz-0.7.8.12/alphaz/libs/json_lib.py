import dataclasses

import ujson

from flask_sqlalchemy.model import DefaultMeta
from sqlalchemy.orm.attributes import instance_state
from sqlalchemy import null

from ..libs.time_lib import timer

from ..models.database.row import Row


def jsonify_database_models(
    model: DefaultMeta,
    first=False,
    relationship: bool = True,
    disabled_relationships: list[str] = None,
):
    """Convert a database model structure to json

    Args:
        model (DefaultMeta): database mode structure
        first (bool, optional): [description]. Defaults to False.

    Returns:
        [type]: [description]
    """
    if not hasattr(model, "_sa_instance_state"):
        return (
            str(model)
            if not hasattr(model, "get_table_model")
            else model.get_table_model()
        )
    state = instance_state(model)
    # if not state.transient or state.persistent:
    if hasattr(model, "get_schema"):
        schema = model.get_schema(
            relationship=relationship, disabled_relationships=disabled_relationships
        )

        structures = schema()  # schema(many=True) if not first else
        results_json = structures.dump(model)  # TODO: ? wtf why does it works
    else:
        try:
            results_json = ujson.dumps(model.__dict__)
        except:
            results_json = str(model)
    return results_json


def is_standard(data) -> bool:
    if type(data) == Row:
        return False
    elif hasattr(data, "schema") or hasattr(data, "get_schema"):
        return False
    elif hasattr(data, "_fields"):
        return False
    elif hasattr(data, "to_json"):
        return False
    elif dataclasses.is_dataclass(data):
        return False
    return True


def jsonify_data(data, string_output: bool = False):
    """Convert any data to a json structure

    Args:
        data ([type]): data to convert

    Returns:
        [type]: data converted as a json structure
    """
    try:
        if str(data) == str(null()):
            return "null()"
    except:
        pass
    if type(data) == str:
        return data
    if type(data) == tuple:
        result = (jsonify_data(x) for x in data)
    elif type(data) == list:
        result = [jsonify_data(x) for x in data]
    elif type(data) == dict:
        if len(data) and not is_standard(list(data.keys())[0]):
            result = {jsonify_data(x): jsonify_data(y) for x, y in data.items()}
        else:
            result = {x: jsonify_data(y) for x, y in data.items()}
    elif type(data) == Row:
        result = dict(data)
    else:
        result = data

        if hasattr(data, "schema") or hasattr(data, "get_schema"):
            result = jsonify_database_models(data)
        elif hasattr(data, "_fields"):
            result = {x: data[i] for i, x in enumerate(data._fields)}
        elif hasattr(data, "to_json"):
            result = data.to_json()
        elif dataclasses.is_dataclass(data):
            result = dataclasses.asdict(data)
    if string_output:
        result = ujson.dumps(result)
    return result


def load_json(string: str):
    if string is None:
        return None
    if type(string) != str:
        string = str(string)
    string = string.strip()

    if len(string) != 0 and string[0] == "{" and string[-1] == "}":
        try:
            return ujson.loads(string)
        except Exception as ex:
            print(f"Cannot convert to json: {string[:100]}")
            raise ex

    if len(string) == 0:
        string = '""'
    string = '{"json":' + string + "}"
    try:
        data = ujson.loads(string)
    except Exception as ex:
        print(f"Cannot convert to json: {string[:100]}")
        raise ex
    return data["json"]
