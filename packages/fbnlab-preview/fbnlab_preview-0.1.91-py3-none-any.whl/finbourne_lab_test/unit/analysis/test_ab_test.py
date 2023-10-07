import os
import unittest
from pathlib import Path
from shutil import rmtree

import numpy as np

from finbourne_lab import Distribution, LinearModel
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

        # Distribution A/B Test
        dist_df1 = generate_data(1, 200, n_rows, 1.0, 0.0, 1.2)
        dist_df2 = generate_data(1, 200, n_rows, 1.1, 0.0, 1.2)
        cls.d1 = Distribution(dist_df1, 'call_time', 'A')
        cls.d2 = Distribution(dist_df2, 'call_time', 'B')

        # Linear A/B Test
        linear_df1 = generate_data(1, 200, n_rows, 2.0, 0.01, 1.5)
        linear_df2 = generate_data(1, 200, n_rows, 2.5, 0.015, 1.5)
        cls.lm1 = LinearModel(linear_df1, 'arg0', 'call_time', 'A')
        cls.lm2 = LinearModel(linear_df2, 'arg0', 'call_time', 'B')

    def test_distribution_AB_test(self):
        ab_test = self.d1.ab_test(self.d2)

        # Default = 5 sigma
        h0_df = ab_test.evaluate_h0().iloc[0]
        self.assertEqual(h0_df.KS_Statistic, 0.08600)
        self.assertEqual(h0_df.PValue, 0.0012207544622917959)
        self.assertEqual(h0_df.Threshold, 2.866515719235352e-07)
        self.assertFalse(h0_df.H0_Rejected)

        # Relax to 3 sigma
        h0_df = ab_test.evaluate_h0(n_sigma=3).iloc[0]
        self.assertEqual(h0_df.KS_Statistic, 0.08600)
        self.assertEqual(h0_df.PValue, 0.0012207544622917959)
        self.assertEqual(h0_df.Threshold, 0.0013498980316301035)
        self.assertTrue(h0_df.H0_Rejected)

        # Effect sizes
        eff_df = ab_test.effect_sizes()
        self.assertSequenceEqual(eff_df.shape, [5, 4])
        self.assertSequenceEqual(eff_df.index.tolist(), [0.05, 0.25, 0.5, 0.75, 0.95])

    def test_linear_model_AB_test(self):

        ab_test = self.lm1.ab_test(self.lm2)

        fr_df = ab_test.fit_result()
        self.assertSequenceEqual(fr_df.shape, [5, 8])
        self.assertSequenceEqual(
            fr_df.columns.tolist(),
            ['const', 'arg0', 'delta_c', 'delta_m', 'const_stderr', 'arg0_stderr', 'delta_c_stderr', 'delta_m_stderr']
        )

        h0_df_1 = ab_test.evaluate_h0()
        self.assertSequenceEqual(h0_df_1.shape, [5, 6])
        self.assertSequenceEqual(h0_df_1.reject_h0_m.tolist(), [True, False, False, False, True])
        self.assertSequenceEqual(h0_df_1.reject_h0_c.tolist(), [True, True, False, False, True])

        h0_df_2 = ab_test.evaluate_h0(n_sigma=3)
        self.assertSequenceEqual(h0_df_2.shape, [5, 6])
        self.assertSequenceEqual(h0_df_2.reject_h0_m.tolist(), [True, True, False, True, True])
        self.assertSequenceEqual(h0_df_2.reject_h0_c.tolist(), [True, True, True, True, True])

        eff_df = ab_test.effect_sizes()
        self.assertSequenceEqual(eff_df.shape, [5, 6])
        self.assertSequenceEqual(
            eff_df.columns.tolist(),
            ['delta_c', 'delta_m', 'frac_diff_c', 'frac_diff_m', 'frac_diff_c_stderr', 'frac_diff_m_stderr']
        )
        self.assertSequenceEqual(eff_df.index.tolist(), [0.05, 0.25, 0.5, 0.75, 0.95])
