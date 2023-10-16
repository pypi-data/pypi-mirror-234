import unittest
from datetime import datetime

import pandas as pd

from finbourne_lab.common.observation import Observation


class TestObservation(unittest.TestCase):

    def test_observation_ctor(self):

        obs = Observation([1], name='EXP 1', run_id='RUN_1', meta1='test1')

        self.assertEqual('EXP 1', obs.data['name'])
        self.assertEqual('RUN_1', obs.data['run_id'])
        self.assertIsNone(obs.data['execution_id'])
        self.assertTrue(pd.isna(obs.data['start']))
        self.assertTrue(pd.isna(obs.data['end']))
        self.assertFalse(obs.data['errored'])
        self.assertIsNone(obs.data['error_message'])
        self.assertEqual(obs.data['arg0'], 1)
        self.assertEqual(obs.data['meta1'], 'test1')

    def test_observation_log_time(self):

        obs = Observation([1], name='EXP 1', run_id='RUN_1', meta1='test1')
        obs.log_time('test_time')
        self.assertIn('test_time', obs.data)
        self.assertIsInstance(obs.data['test_time'], datetime)

    def test_observation_setitem(self):
        obs = Observation([1], name='EXP 1', run_id='RUN_1', meta1='test1')
        obs['item_to_set'] = 'value'
        self.assertEqual('value', obs.data['item_to_set'])

    def test_observation_getitem(self):
        obs = Observation([1], name='EXP 1', run_id='RUN_1', meta1='test1')
        obs['item_to_get'] = 'value'
        self.assertEqual('value', obs['item_to_get'])
