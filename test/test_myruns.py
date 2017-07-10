import pytest

from MyRuns import *

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
        config = YamlConfig(name="config.yaml")
        db_address = YamlConfig(name="db_address.yaml")
        assert(config.get(Parameters.STRAVA_CLIENT_ID, default=None) != None )
        assert(config.get(Parameters.STRAVA_SECRET, default=None) != None )
        assert(config.get(Parameters.REDIRECT_URI, default=None) != None )
        assert(config.get(Parameters.SECRET_KEY, default=None) != None )
        assert(db_address.get(Parameters.DB_ADDRESS, default=None) != None )
