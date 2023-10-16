import unittest
import uuid
from finbourne_lab.lusid import LusidClient
import lumipy as lm
import os


class TestLusidClient(unittest.TestCase):

    lm_client = lm.get_client()
    client = LusidClient(token=lm_client.get_token(), api_url=os.environ['FBN_LUSID_API_URL'])

    def test_ensure_property_definitions(self):

        scope = f"fbnlab-ut-{str(uuid.uuid4())}"
        domain = "Instrument"
        n_props = 50
        response = self.client.ensure_property_definitions(n_props=n_props, scope=scope, domain=domain)
        self.assertTrue(response)
        