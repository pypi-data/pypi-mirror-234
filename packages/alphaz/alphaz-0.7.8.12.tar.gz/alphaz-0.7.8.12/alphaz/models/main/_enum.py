from enum import Enum


class AlphaEnum(Enum):
    def __str__(self):
        return str(self.value)

    def to_json(self):
        return str(self.value)


class EnumStr(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name


class MappingMode(AlphaEnum):
    AUTO = "auto"
    STRICT = "strict"


class ParameterMode(Enum):
    NONE = 0
    LIKE = 1
    IN_LIKE = 2
    START_LIKE = 3
    END_LIKE = 4

    def __str__(self):
        return str(self.value)

    def to_json(self):
        return str(self.value)
