import pytest
from MyRuns import *
from MyRuns.config_operations import ConfigFile
import tempfile

class TestCore:
    def setup_class(self):
        self.username = "gbot"

    def setup_method(self, method):
        print("method setup : ", method.__name__)

    def setup(self):
        print("basic setup start test")

    def teardown(self):
        print("basic teardown into class")

    def teardown_method(self, method):
        print("method teardown :", method.__name__)

    def teardown_class(self):
        print("cleaning...")

    def test_read_config(self):
        path_to_config = tempfile.gettempdir()
        config = ConfigFile(path_to_config, config_name="config.yaml")
        config.write_parameter("VAR", "VAL")
        assert(config.read_parameter("VAR") == "VAL")
