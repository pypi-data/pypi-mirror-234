# MODULES
import datetime, os, re, configparser, pickle
from collections import OrderedDict

# LIBS
from ..libs import converter_lib, json_lib, io_lib, dict_lib

# MODELS
from ..models.database.structure import AlphaDatabase

import numpy as np

CONSTANTS = {}
PARAMETERS = {}
CONFIGS = {}
CONFIG_FILE_EXTENSION = ".ini"


def un_pickle(value):
    decoded = base64.b64decode(value)
    value = pickle.loads(decoded)
    return value


def order(D: dict) -> OrderedDict:
    return OrderedDict(sorted(D.items(), key=lambda x: len(x[0]), reverse=True))


def get_db_constants(bind: str | None = None) -> OrderedDict:
    from core import DB

    global CONSTANTS

    """Get constants from database

    Args:
        bind (str): [description]

    Returns:
        OrderedDict: constants in a dict with <name> key and <value> value
    """
    rows = DB.select(Constants, json=True)
    values = {x["name"]: x["value"] for x in rows}

    now = datetime.datetime.now()
    values["year"] = now.year
    values["month"] = now.month  # TODO: need to update constants each time
    values["day"] = now.day
    values["hour"] = now.hour
    values["minute"] = now.minute
    values["second"] = now.second

    order(values)
    CONSTANTS = values
    return CONSTANTS


def get_db_parameters(bind: str | None = None) -> OrderedDict:
    from core import DB, core

    LOG = core.get_logger("config")
    global PARAMETERS
    """[summary]

    Args:
        db ([type]): [description]
        model ([type]): [description]

    Returns:
        [type]: [description]
    """
    model = DB.get_table_model("parameters", bind=bind)

    rows = DB.select(model)
    values = {}
    for row in rows:
        try:
            values[row.name] = pickle.loads(row.value)
        except Exception as ex:
            LOG.error(f"Cannot load parameter <{row.name}>", ex=ex)
    order(values)
    PARAMETERS = values
    return PARAMETERS


def get_db_constant(
    name: str, update: bool = False, separator=None, bind: str | None = None
) -> list[str]:
    """[summary]

    Args:
        db ([type]): [description]
        model ([type]): [description]
        core_ ([type]): [description]
        name ([type]): [description]
        update (bool, optional): [description]. Defaults to False.

    Returns:
        [type]: [description]
    """
    if update:
        get_db_constants(bind=bind)

    values = None
    if not is_db_constant(name, bind=bind):
        get_db_constants(bind=bind)
        if is_db_constant(name, bind=bind):
            values = CONSTANTS[name]
    else:
        values = CONSTANTS[name]

    if separator is not None:
        if values is not None:
            return (
                str(values)
                .replace("b", "")
                .replace('"', "")
                .replace("'", "")
                .split(separator)
            )
        return []
    return values


def get_db_parameter(name: str, update: bool = False, bind: str | None = None):
    """[summary]

    Args:
        model ([type]): [description]
        core_ ([type]): [description]
        name ([type]): [description]
        update (bool, optional): [description]. Defaults to False.
        bind (str): [description]

    Returns:
        [type]: [description]
    """
    values = None
    if update:
        get_db_parameters(bind=bind)

    if not is_db_parameter(name, bind=bind):
        get_db_parameters(bind=bind)
        if is_db_parameter(name, bind=bind):
            values = PARAMETERS[name]
    else:
        values = PARAMETERS[name]
    return values


def set_db_constant(name: str, value, bind: str | None = None):
    from core import DB

    """[summary]

    Args:
        db ([type]): [description]
        model ([type]): [description]
        name ([type]): [description]
        value ([type]): [description]
    """
    CONSTANTS[name] = value
    model = DB.get_table_model("constants", bind=bind)
    DB.add_or_update(model, parameters={"name": name, "value": value})


def set_db_parameter(name: str, value, bind: str | None = None):  # TODO: set core
    from core import DB

    """[summary]

    Args:
        db ([type]): [description]
        model ([type]): [description]
        name ([type]): [description]
        value ([type]): [description]
    """
    PARAMETERS[name] = value
    model = DB.get_table_model("parameters", bind=bind)
    # data                = json.dumps(json_lib.jsonify_data(value))
    data = pickle.dumps(value)
    DB.add_or_update(model, parameters={"name": name, "value": data})


def is_db_constant(name: str, bind: str | None = None):
    """[summary]

    Args:
        core_ ([type]): [description]
        name ([type]): [description]

    Returns:
        [type]: [description]
    """
    return name in CONSTANTS


def is_db_parameter(name: str, bind: str | None = None):
    """[summary]

    Args:
        core_ ([type]): [description]
        name ([type]): [description]

    Returns:
        [type]: [description]
    """
    return name in PARAMETERS


def get_api_build(update: bool = False, bind: str | None = None):
    """[summary]

    Args:
        db ([type]): [description]
        core_ ([type]): [description]
        update (bool, optional): [description]. Defaults to False.

    Returns:
        [type]: [description]
    """
    build = get_db_constant("api_build", update=update, bind=bind)
    if build is None:
        build = 0
    return build


def upgrade_api_build(bind: str | None = None):
    """[summary]

    Args:
        db ([type]): [description]
        model ([type]): [description]
        core_ ([type]): [description]
    """
    build = get_api_build()
    set_db_constant("api_build", int(build) + 1, bind=bind)


def get_config_filename(fileName, directory, test=False):
    prefix = "test_" if test else ""
    parametersFileName = "%s/%s" % (
        directory,
        prefix + fileName + CONFIG_FILE_EXTENSION,
    )
    return parametersFileName


def get_config_from_file(fileName, directory, test=False):
    from core import core

    LOG = core.get_logger("config")
    config = configparser.RawConfigParser()
    config.optionxform = str

    parametersFileName = get_config_filename(fileName, directory=directory, test=test)

    if not os.path.isfile(parametersFileName):
        LOG.error(
            "Cannot find configuration file at %s (%s)"
            % (parametersFileName, os.getcwd())
        )
        exit()
        return None

    LOG.info("Reading config file: %s" % parametersFileName)
    config.read(parametersFileName)
    return config


def read_parameters_from_config(fileName, config, sectionHeader, directory, test=False):
    parameters = dict()

    if not sectionHeader:
        for section in config.sections():
            for options in config.options(section):
                parameters[options] = convert_config_value(
                    config.get(section, options).replace("\n", "")
                )

        if test:
            baseParameters = load_config_file(fileName, directory=directory, test=False)

            for baseParameter, value in baseParameters.items():
                if not baseParameter in parameters:
                    parameters[baseParameter] = value
    else:
        for section in config.sections():
            parameters[section] = dict()
            for options in config.options(section):
                value = config.get(section, options)
                value = value.replace("\n", "") if type(value) == str else value
                parameters[section][options] = convert_config_value(value)

        if test:
            baseParameters = load_config_file(
                fileName, directory=directory, sectionHeader=True, test=False
            )

            for section, baseParameter in baseParameters.items():
                for baseParameterName, value in baseParameter.items():
                    if not baseParameterName in parameters[section].keys():
                        parameters[section][baseParameterName] = value
    return parameters


def load_config_file(fileName, directory, sectionHeader=False, test=False):
    config = get_config_from_file(fileName, directory=directory, test=test)
    if config is None:
        return {}

    return read_parameters_from_config(
        fileName, config, sectionHeader, directory=directory, test=False
    )


def convert_config_value(value):
    if type(value) != str:
        return value

    valueStr = str(value).upper()

    rangeMatch = re.match("\[(.*:.*)\]", str(value))
    listMatch = re.match("\[(.*)\]", str(value))
    dictMatch = re.match("\{(.*)\}", str(value))

    stringMatchQuote, stringMatch = False, False
    if len(valueStr) != 0:
        stringMatchQuote = valueStr[0] == '"' and valueStr[-1] == '"'
        stringMatch = (
            valueStr[0] == "'" and valueStr[-1] == "'"
            if not stringMatchQuote
            else stringMatchQuote
        )
    # stringMatch = re.match('\'(.*)\'',str(value))

    if rangeMatch:
        match = listMatch.groups()[0]
        values = match.split(":")
        step = 1 if len(values) == 2 else convert_config_value(values[2])
        value = np.arange(
            convert_config_value(values[0]),
            convert_config_value(values[1]) + step,
            step,
        )
    elif listMatch:
        match = listMatch.groups()[0]
        listValues = match.split(",")
        value = [convert_config_value(x.lstrip()) for x in listValues]
    elif dictMatch:
        match = dictMatch.groups()[0]
        listValues = match.split(",")
        value = {}
        for el in listValues:
            key, vl = str(el).split(":")
            value[convert_config_value(key)] = convert_config_value(vl)
    elif ":" in valueStr:
        values = valueStr.split(":")
        step = 1 if len(values) == 2 else convert_config_value(values[2])
        value = np.arange(
            convert_config_value(values[0]),
            convert_config_value(values[1]) + step,
            step,
        )
    elif "," in valueStr:
        listValues = valueStr.split(",")
        value = [convert_config_value(x.lstrip()) for x in listValues]
    elif stringMatch:
        # match = stringMatch.groups()[0]
        # value = match.replace('\'','')
        value = value[1:-1]
    elif str(value) == "None" or valueStr is None:
        value = None
    elif valueStr == "FALSE":
        value = False
    elif valueStr == "TRUE":
        value = True
    elif valueStr == "FLOAT":
        value = float
    elif valueStr == "INT":
        value = int
    elif valueStr == "BOOL":
        value = bool
    elif valueStr == "STR":
        value = str
    else:
        value = converter_lib.to_num(value)

    if value is not None and type(value) == str:
        value = value

    return value


def convert_config_value_for_write(value):
    value = convert_config_value(value)

    if type(value) == str:
        if not value[0] == '"' and not value[0] == "'":
            value = "'" + value
        if not value[-1] == '"' and not value[-1] == "'":
            value += "'"
        value = value.replace("\n", "<br>")
    return value


def write_defaults_config_files(fileName, values, directory):
    # Add existing values
    #     existingConfig                              = load_config_file(fileName,directory=directory,sectionHeader=True)
    existingConfig = get_config_from_file(fileName, directory=directory)

    # Set config file
    parametersFileName = get_config_filename(fileName, directory=directory)

    for header, value in values.items():
        existingConfig.set(header, "value", value)

    with open(parametersFileName, "w") as configfile:
        existingConfig.write(configfile)

    parameters = read_parameters_from_config(
        fileName, existingConfig, sectionHeader=True, directory=directory, test=False
    )


def write_config_file(filename, values, directory, upper_keys: bool = False):
    config = configparser.ConfigParser()

    for key, values in values.items():
        config[key] = {x.upper() if upper_keys else x: y for x, y in values.items()}

    if not "." in filename:
        filename = filename + ".ini"

    config_path = directory + os.sep + filename
    io_lib.ensure_dir(config_path)
    with open(config_path, "w") as configfile:
        config.write(configfile)


def write_flask_dashboard_configuration():
    from core import core

    LOG = core.get_logger("config")
    filename = "dashboard.cfg"
    directory = core.config.get("directories/tmp")
    dashboard = core.api.conf.get("dashboard")

    if dashboard is None:
        return None
    io_lib.ensure_dir(directory)
    try:
        write_config_file(filename, dashboard, directory, upper_keys=True)
        return directory + os.sep + filename
    except Exception as ex:
        LOG.error(ex)
        return None


def get_configs(config: str | None = None):
    from core import DB, LOG
    from ..models.database.main_definitions import Configs

    global CONFIGS
    configs = DB.select(Configs)
    configs_dict = {}
    for config in configs:
        keys = [x.lower() for x in config.name.split(":")]
        value = config.value
        config_type = config.type.upper().strip()

        try:
            match config_type:
                case "BOOLEAN":
                    value = True if "T" in value.upper() else False
                case "STRING":
                    value = str(value)
                case "STRING[]":
                    value = str(value).split(";")
                case "INT":
                    value = int(value)
                case "INT[]":
                    value = [int(x) for x in str(value).split(";")]
                case "FLOAT":
                    value = float(value)
                case "FLOAT[]":
                    value = [float(x) for x in str(value).split(";")]
        except:
            LOG.error(
                f"Failed to convert config parameter {config.name} to {config_type}"
            )
            value = None

        dict_keys = dict_lib.get_nested_dict_from_list(keys)
        dict_lib.set_nested(dict_keys, keys, value)
        configs_dict = dict_lib.merge_dict(configs_dict, dict_keys)
    CONFIGS = configs_dict
    return configs_dict


def get_configs_key(keys: str | list[str], config: str | None = None, default=None):
    global CONFIGS
    if type(keys) == str:
        keys = keys.split(":")
    if CONFIGS is None or len(CONFIGS) == 0:
        CONFIGS = get_configs(config)
    value = dict_lib.get_nested(CONFIGS, [x.lower() for x in keys])
    return value if value is not None else default
