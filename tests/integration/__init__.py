import os
import click.testing
import skychain
import unittest
import json
import tempfile
from skychain.models.blockchain import Blockchain


class SkyTrackIntegrationTest(unittest.TestCase):

    def setUp(self):
        skychain.sky_app.testing = True
        self.app = skychain.sky_app.test_client()

    def tearDown(self):
        pass

    # -----------------------------------------------------------------------------------
    # TEST HASH LENGTH IS CORRECT
    # -----------------------------------------------------------------------------------
    def test_default_chain_length_is_one(self):
        service_response = self.app.get('/api/v1/chain')
        json_data = json.loads(service_response.get_data(as_text=True))
        assert json_data["length"] is 1
