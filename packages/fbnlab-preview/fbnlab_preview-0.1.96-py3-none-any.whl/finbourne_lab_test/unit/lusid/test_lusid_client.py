import unittest
import uuid
from finbourne_lab.lusid import LusidClient
import lumipy as lm
import os
import lusid
import shortuuid


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

    def test_ensure_instruments_does_upsert_new_instruments(self):
        scope = f"fbnlab-ut-{str(shortuuid.uuid())}"
        id_prefix = f"fbnlab-ut-{str(shortuuid.uuid())}"
        n_inst = 5

        response = self.client.ensure_instruments(n_insts=n_inst, id_prefix=id_prefix, scope=scope)
        response_code_actual = response[0]
        # the method should return 100 if the instruments did not exist and have been successfully created
        response_code_expected = 100
        upsert_data = response[1].json()
        metadata_actions_type_expected = "CreatedInstruments"
        metadata_actions_type_actual = upsert_data['metadata']['actions'][0]["type"]
        self.assertEqual(response_code_expected, response_code_actual)
        self.assertEqual(metadata_actions_type_expected, metadata_actions_type_actual)

    def test_ensure_instruments_does_not_upsert_already_existing_instruments(self):

        scope = f"fbnlab-ut-test"
        id_prefix = f"fbnlab-ut-test"
        n_inst = 5
        properties = []

        import lusid.models as models
        instruments = {
            f'inst_{i}': models.InstrumentDefinition(
                name=f'Instrument{i}',
                identifiers={"ClientInternal": models.InstrumentIdValue(f'{id_prefix}_{i}')},
                properties=properties
            )
            for i in range(n_inst)
        }

        self.client.instruments_api.upsert_instruments(request_body=instruments,
                                                       scope=scope,
                                                       _preload_content=False)

        # attempt to recreate the already existing instruments
        response = self.client.ensure_instruments(n_insts=n_inst, id_prefix=id_prefix, scope=scope)
        response_code_actual = response[0]
        # the method should return a response code 102 if the instruments did exist and no upsert was needed
        response_code_expected = 102
        self.assertEqual(response_code_expected, response_code_actual)
