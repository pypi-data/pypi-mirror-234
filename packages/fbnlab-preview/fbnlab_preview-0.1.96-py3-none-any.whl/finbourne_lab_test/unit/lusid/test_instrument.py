import unittest
import lumipy as lm
import os

import pandas as pd

from finbourne_lab import Convener, FileRecorder
from finbourne_lab.lusid import LusidInstrumentLab, LusidClient
import shortuuid


class TestInstrument(unittest.TestCase):

    lm_client = lm.get_client()
    lusid_instrument_lab = LusidInstrumentLab(token=lm_client.get_token(), api_url=os.environ['FBN_LUSID_API_URL'])
    client = LusidClient(token=lm_client.get_token(), api_url=os.environ['FBN_LUSID_API_URL'])

    domain = "Instrument"

    def test_upsert_instruments_measurement(self):

        scope = f"fbnlab-ut-{str(shortuuid.uuid())}"
        id_prefix = f"fbnlab-ut-{str(shortuuid.uuid())}"
        n_inst = 5
        n_props = 1

        experiment = self.lusid_instrument_lab.upsert_instruments_measurement(x_rng=n_inst,
                                                                              n_props=n_props,
                                                                              scope=scope,
                                                                              id_prefix=id_prefix)
        recorder = FileRecorder('test_upsert_instruments')
        convener = Convener(experiment, recorder)
        convener.go(10)

        self.client.ensure_property_definitions(n_props=n_props, scope=scope, domain=self.domain)
        properties = self.client.build_properties(n_props=n_props, scope=scope, domain=self.domain)
        property_keys = [prop.key for prop in properties]
        identifiers = [f"{id_prefix}_{i}" for i in range(n_inst)]

        instrument_api = self.client.instruments_api
        response = instrument_api.get_instruments("ClientInternal",
                                                  request_body=identifiers,
                                                  scope=scope,
                                                  property_keys=property_keys,
                                                  _preload_content=False)
        data = response.json()
        instruments_name_expected = [f"Instrument{i}" for i in range(n_inst)]
        instruments_name_actual = [data['values'][identifiers[i]]['name'] for i in range(n_inst)]
        self.assertEqual(instruments_name_expected, instruments_name_actual)

    def test_get_instruments_measurement(self):

        scope = f"fbnlab-ut-{str(shortuuid.uuid())}"
        id_prefix = f"fbnlab-ut-{str(shortuuid.uuid())}"
        x_rng = [1, 5]
        n_props = 1

        experiment = self.lusid_instrument_lab.get_instruments_measurement(
            x_rng=x_rng,
            n_props=n_props,
            scope=scope,
            id_prefix=id_prefix
        )
        path = 'test_upsert_instruments'
        recorder = FileRecorder(path)
        convener = Convener(experiment, recorder)
        convener.go(10)

        df = pd.read_csv(f"{path}/get_instruments.csv")
        if len(df) == 0:
            raise Exception('There was no data recorded')
        else:
            df_errored = df.loc[df['errored'] == True]
            # check whether we have less than 5 percent error rate
            self.assertTrue(expr=(len(df_errored)/len(df)) < 0.05, msg="Error rate is higher than 5%")
