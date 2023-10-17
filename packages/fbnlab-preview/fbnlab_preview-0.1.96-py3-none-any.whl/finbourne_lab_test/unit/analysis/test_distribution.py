import os
import unittest
from pathlib import Path
from shutil import rmtree

import numpy as np

from finbourne_lab import Distribution
from finbourne_lab_test.utils.test_data_generation import generate_data


class TestDistribution(unittest.TestCase):

    work_dir = '/tmp/finbourne_lab_test/distribution/'

    @classmethod
    def setUpClass(cls) -> None:

        if os.path.exists(f'{cls.work_dir}'):
            rmtree(cls.work_dir)

        path = Path(cls.work_dir)
        path.mkdir(parents=True, exist_ok=True)

        n_rows = 1000
        np.random.seed(1989)

        # Gradient = 0.0 so this is just a gaussian with mean at 1.0 and std dev 0.1 + 0.1 prob of outliers
        cls.df1 = generate_data(1, 1000, n_rows, 1.0, 0.0, 0.1, 0.1)

    def test_distribution_object_construction(self):

        d = Distribution(self.df1, 'call_time', 'test')

        self.assertEqual(d.name, 'test')
        self.assertEqual(d.x, 'call_time')
        self.assertSequenceEqual(d.data.shape, self.df1.shape)
        self.assertEqual(d.n, self.df1.shape[0])
        self.assertEqual(d.min, self.df1.call_time.min())
        self.assertEqual(d.max, self.df1.call_time.max())

    def test_distribution_object_quantile(self):

        d = Distribution(self.df1, 'call_time', 'test')

        self.assertEqual(d.quantile(0.333), 0.9711258010488496)
        self.assertSequenceEqual(d.quantile([0.333, 0.667]).tolist(), [0.9711258010488496, 1.0440960603816485])

    def test_distribution_object_quantile_df(self):

        d = Distribution(self.df1, 'call_time', 'test')

        q_df = d.quantiles_df()
        self.assertSequenceEqual(q_df.shape, [1, 5])
        self.assertSequenceEqual(q_df.columns.tolist(), [0.05, 0.25, 0.5, 0.75, 0.95])
        self.assertEqual(q_df.index[0], d.name)

    def test_distribution_object_outliers(self):

        d = Distribution(self.df1, 'call_time', 'test')
        o_df = d.outliers()
        self.assertSequenceEqual(o_df.shape, [79, 7])

    def test_distribution_object_remove_outliers(self):

        d = Distribution(self.df1, 'call_time', 'test')
        d2 = d.remove_outliers()
        self.assertEqual(d.data.shape[0], d2.data.shape[0] + d.outliers().shape[0])
