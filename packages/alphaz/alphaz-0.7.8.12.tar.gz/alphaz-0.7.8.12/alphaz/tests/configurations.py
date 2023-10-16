from ..models.tests import test, AlphaTest
from ..libs import config_lib

from core import core

DB = core.db


class ConfigConstants(AlphaTest):
    def begin(self):
        self.constant_name = "test"
        config_lib.set_db_constant(self.constant_name, 0)
        pass

    @test(stop=True)
    def is_db_constant(self):
        return config_lib.is_db_constant(self.constant_name)

    @test(stop=True)
    def get_db_constants(self):
        constants = config_lib.get_db_constants()
        self.assert_is_not_empty(constants)

    @test()
    def get_db_constant(self):
        value = config_lib.get_db_constant(self.constant_name)
        self.assert_equal(value, 0)

    @test()
    def set_db_constant(self):
        config_lib.set_db_constant(self.constant_name, 1)
        value = config_lib.get_db_constant(self.constant_name)
        self.assert_equal(value, 1)


class ConfigParameters(AlphaTest):
    disable = True

    def begin(self):
        self.parameter_name = "test"
        config_lib.set_db_parameter(self.parameter_name, 0)
        pass

    @test(stop=True)
    def is_db_parameter(self):
        return config_lib.is_db_parameter(self.parameter_name)

    @test(stop=True)
    def get_db_parameters(self):
        self.assert_is_not_empty(config_lib.get_db_parameters())

    @test()
    def get_db_parameter(self):
        return config_lib.get_db_parameter(self.parameter_name) == 0

    @test()
    def set_db_parameter(self):
        config_lib.set_db_parameter(self.parameter_name, 1)
        return config_lib.get_db_parameter(self.parameter_name) == 1
