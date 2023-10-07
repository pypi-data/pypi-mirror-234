import unittest
from multiprocessing import Queue
from os.path import isdir
from shutil import rmtree

import pandas as pd

from finbourne_lab import FileRecorder
from finbourne_lab.common.observation import Observation
from finbourne_lab.common.recorder.base import BaseRecorder


class TestFileRecorder(unittest.TestCase):

    fpath = '/tmp/fbn-lab-recorder-test'

    def test_file_recorder_ctor(self):
        if isdir(self.fpath):
            rmtree(self.fpath)

        fr = FileRecorder(self.fpath)
        self.assertIsInstance(fr, BaseRecorder)
        self.assertEqual(self.fpath, fr.directory)

        self.assertTrue(isdir(self.fpath))

    def test_file_recorder_(self):

        if isdir(self.fpath):
            rmtree(self.fpath)

        def make_obs(x):
            obs = Observation([x, x ** 2], name='test', run_id='<guid>', meta='AA')
            obs.log_time('test_time')
            return obs

        fr = FileRecorder(self.fpath, chunk_size=3)

        for i in range(10):
            fr.put(make_obs(i).data)

        df = pd.read_csv(f'{self.fpath}/test.csv')
        self.assertSequenceEqual([9, 11], df.shape)

        fr.flush()
        df = pd.read_csv(f'{self.fpath}/test.csv')
        self.assertSequenceEqual([10, 11], df.shape)
