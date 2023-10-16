import os
import unittest
from pathlib import Path
from shutil import rmtree

from finbourne_lab import Convener, FileRecorder, Shopper
from finbourne_lab.luminesce import LumiExperiment
from finbourne_lab_test.utils.mock import MockQuery
import pandas as pd


class TestLuminesceExperiment(unittest.TestCase):

    work_dir = '/tmp/finbourne_lab_test/unit/luminesce/'

    @classmethod
    def setUpClass(cls) -> None:

        if os.path.exists(f'{cls.work_dir}'):
            rmtree(cls.work_dir)

        path = Path(cls.work_dir)
        path.mkdir(parents=True, exist_ok=True)

    def test_mock_query_job(self):

        build = MockQuery.build

        qry = build(5)

        self.assertEqual(qry.x, 5)
        self.assertEqual(qry.call_count, 0)

        job = qry.go_async()
        job.interactive_monitor()

        df = job.get_result()
        self.assertSequenceEqual(df.shape, [5, 3])
        self.assertEqual(qry.call_count, 1)

    def test_luminesce_experiment_run(self):

        build_fn = MockQuery.build
        experiment = LumiExperiment('test-1', build_fn, [1, 10], skip_download=False)
        recorder = FileRecorder(self.work_dir)
        convener = Convener(experiment, recorder)

        convener.go(6)
        df = pd.read_csv(self.work_dir + 'test-1.csv').head(3)

        self.assertSequenceEqual([3, 23], df.shape)
        self.assertTrue(all(v == 'test-1' for v in df.name))
        self.assertTrue(all(not v for v in df.errored))
        self.assertTrue(all(not v for v in df.skip_download))

    def test_luminesce_experiments_in_shopper(self):

        build_fn = MockQuery.build

        ex1 = LumiExperiment('shop-1', build_fn, [0, 10])
        ex2 = LumiExperiment('shop-2', build_fn, [0, 10])
        ex3 = LumiExperiment('shop-3', build_fn, [0, 10])
        shopper = Shopper(ex1, ex2, ex3)

        recorder = FileRecorder(self.work_dir)
        convener = Convener(shopper, recorder)

        convener.go(15)
        df1 = pd.read_csv(self.work_dir + 'shop-1.csv').head(3)
        df2 = pd.read_csv(self.work_dir + 'shop-2.csv').head(3)
        df3 = pd.read_csv(self.work_dir + 'shop-3.csv').head(3)

        self.assertGreater(df1.shape[0], 0)
        self.assertGreater(df2.shape[0], 0)
        self.assertGreater(df3.shape[0], 0)
