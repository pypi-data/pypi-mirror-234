import unittest
import uuid
from finbourne_lab.lusid import LusidClient
import lumipy as lm
import os
import lusid


class TestLusidClient(unittest.TestCase):

    lm_client = lm.get_client()
    client = LusidClient(token=lm_client.get_token(), api_url=os.environ['FBN_LUSID_API_URL'])

    def test_ensure_property_definitions(self):

        scope = f"fbnlab-ut-{str(uuid.uuid4())}"
        domain = "Instrument"
        n_props = 50
        response = self.client.ensure_property_definitions(n_props=n_props, scope=scope, domain=domain)
        self.assertTrue(response)

    def test_build_properties(self):
        scope = f"fbnlab-ut-prop"
        domain = "Instrument"
        n_props = 2
        properties_actual = self.client.build_properties(n_props=n_props, scope=scope, domain=domain)
        print(properties_actual)

        properties_expected = [
            lusid.models.ModelProperty(
                key=f'Instrument/fbnlab-ut-prop/test_prop0',
                value=lusid.PropertyValue(metric_value=lusid.models.MetricValue(value=0))
            ),
            lusid.models.ModelProperty(
                key=f'Instrument/fbnlab-ut-prop/test_prop1',
                value=lusid.PropertyValue(metric_value=lusid.models.MetricValue(value=100))
            )
        ]

        self.assertEqual(properties_expected, properties_actual)

