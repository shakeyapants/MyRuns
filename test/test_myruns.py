import pytest
# from MyRuns import *
from MyRuns.config_operations import ConfigFile
import tempfile
import os
from pathlib import Path

class TestCore:
    def setup_class(self):
        self.workdir = tempfile.mkdtemp()

    def setup_method(self, method):
        print("method setup : ", method.__name__)

    def setup(self):
        print("basic setup start test")
        print(self.workdir)

    def teardown(self):
        print("basic teardown into class")

    def teardown_method(self, method):
        print("method teardown :", method.__name__)

    def teardown_class(self):
        print("cleaning...")

    def test_create_config(self):
        path_to_config = self.workdir
        config_file = "config.yaml"
        config = ConfigFile(path_to_config, config_name=config_file)
        config.create()
        assert(Path(path_to_config).joinpath(config_file).exists() is True)

    def test_io_config(self):
        path_to_config = self.workdir
        config_file = "config.yaml"
        config = ConfigFile(path_to_config, config_name=config_file)
        config.create()
        config.write_parameter("VAR", "VAL")
        assert(config.read_parameter("VAR") == "VAL")
        config.write_parameter("VAR1", "VAL1")
        assert (config.read_parameter("VAR1") == "VAL1")
        config.write_parameter("VAR2", "VAL2")
        assert (config.read_parameter("VAR2") == "VAL2")
        config.write_parameter("VAR", "VAL10")
        assert (config.read_parameter("VAR") == "VAL10")

    def test_read_config(self):
        path_to_config = self.workdir
        config_file = "config.yaml"
        config = ConfigFile(path_to_config, config_name=config_file)
        with pytest.raises(FileNotFoundError) as ex:
            config.read_parameter("SomeFile")
        val = ''
        try:
            val = config.read_parameter("SomeFile", "AnyText")
        except FileNotFoundError as ex:
            config.create()
            val = config.read_parameter("SomeFile", "AnyText")
        finally:
            assert ( val == "AnyText" )



