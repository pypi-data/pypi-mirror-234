from finbourne_lab import Convener, FileRecorder, Shopper
from finbourne_lab.common.experiment import Experiment
import unittest
from os.path import isdir
from shutil import rmtree
import pandas as pd
from time import sleep, time


class TestConvener(unittest.TestCase):

    @staticmethod
    def make_experiment(name, t):

        def fn(x):
            return lambda: sleep(t)

        return Experiment(name, fn, [1, 10], meta1='a')

    @classmethod
    def setUpClass(cls) -> None:
        fpath = '/tmp/fbnlab-convener-test/'
        if isdir(fpath):
            rmtree(fpath)
        cls.recorder = FileRecorder(fpath, chunk_size=10000)

    def test_convener_ctor_experiment(self):
        ex = self.make_experiment('ex', 0.1)
        c = Convener(ex, self.recorder, 5)

        self.assertEqual(ex.exp_name, c.to_run.exp_name)
        self.assertEqual(self.recorder.directory, c.recorder.directory)
        self.assertEqual(5, c.n_parallel)

    def test_convener_go_experiment(self):
        ex = self.make_experiment('ex', 0.1)

        n_parallel, duration, t = 4, 5, 0.1

        c = Convener(ex, self.recorder, 4)

        start = time()
        c.go(5)
        obs_duration = time() - start

        self.assertGreaterEqual(obs_duration, 5)
        self.assertAlmostEqual(duration, obs_duration, 1)

        df = pd.read_csv(self.recorder.directory + 'ex.csv')
        self.assertLessEqual(abs(df.shape[0] - 200), 5)

    def test_convener_ctor_shopper(self):
        ex1 = self.make_experiment('ex1', 0.1)
        ex2 = self.make_experiment('ex2', 0.2)
        ex3 = self.make_experiment('ex3', 0.05)

        shopper = Shopper(ex1, ex2, ex3)
        c = Convener(shopper, self.recorder, 5)
        self.assertEqual(len(shopper.experiments), len(c.to_run.experiments))
        self.assertEqual(self.recorder.directory, c.recorder.directory)
        self.assertEqual(5, c.n_parallel)

    def test_convener_go_shopper(self):
        ex1 = self.make_experiment('shopper-ex1', 0.1)
        ex2 = self.make_experiment('shopper-ex2', 0.2)
        ex3 = self.make_experiment('shopper-ex3', 0.05)

        shopper = Shopper(ex1, ex2, ex3)
        c = Convener(shopper, self.recorder, 4)
        c.go(5)

        df1 = pd.read_csv(self.recorder.directory + 'shopper-ex1.csv')
        df2 = pd.read_csv(self.recorder.directory + 'shopper-ex2.csv')
        df3 = pd.read_csv(self.recorder.directory + 'shopper-ex3.csv')

        self.assertGreater(df1.shape[0], 0)
        self.assertGreater(df2.shape[0], 0)
        self.assertGreater(df3.shape[0], 0)
