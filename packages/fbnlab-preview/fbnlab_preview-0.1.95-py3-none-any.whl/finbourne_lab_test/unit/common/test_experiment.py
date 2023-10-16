import pandas as pd

from finbourne_lab.common.experiment import Experiment
import unittest
from multiprocessing import Queue
from multiprocessing.context import ForkProcess
from uuid import uuid4
import numpy as np
from time import sleep


class TestExperiment(unittest.TestCase):

    def test_experiment_ctor(self):

        def fn(x):
            m, c = 0.001, 0.1
            return lambda: x * m + c

        exp = Experiment('test_exp_1', fn, [1, 10], meta1='a', meta2=123)

        self.assertEqual(exp.exp_name, 'test_exp_1')

        self.assertEqual(1, len(exp.ranges))
        self.assertSequenceEqual(exp.ranges[0], [1, 10])

        self.assertEqual(exp.metadata['meta1'], 'a')
        self.assertEqual(exp.metadata['meta2'], 123)

        self.assertEqual(exp.build_fn(10)(), fn(10)())

    def test_experiment_domain_sample(self):

        def fn(x):
            pass

        # Single range
        exp1 = Experiment('ex', fn, [1, 10])
        np.random.seed(1)
        obs_vals = [exp1.domain_sample() for _ in range(5)]
        self.assertSequenceEqual(obs_vals, [(6,), (9,), (10,), (6,), (1,)])

        # Const value
        exp2 = Experiment('ex', fn, "test")
        obs_vals = [exp2.domain_sample() for _ in range(5)]
        self.assertSequenceEqual(obs_vals, [("test",)] * 5)

        # Set of values
        exp3 = Experiment('ex', fn, {"a", "b", "c"})
        np.random.seed(1)
        obs_vals = [exp3.domain_sample() for _ in range(5)]
        self.assertTrue(all(v[0] in 'abc' for v in obs_vals))

        # All the above
        exp4 = Experiment('ex', fn, [1, 10], 'ABC', {1.0, 1.1, 1.2, 1.3, 1.4})
        np.random.seed(1)
        obs_vals = [exp4.domain_sample() for _ in range(5)]
        self.assertSequenceEqual(
            obs_vals,
            [(6, 'ABC', 1.3), (9, 'ABC', 1.0), (6, 'ABC', 1.2), (1, 'ABC', 1.0), (8, 'ABC', 1.1)]
        )

    def test_experiment_run(self):

        def fn(x):
            m, c, s = 0.001, 0.1, 0.01

            def call():
                val = np.random.normal(x * m + c, s)
                if np.random.uniform() <= 0.5:
                    return val
                raise ValueError('test error...')

            return call

        exp = Experiment('test_exp_1', fn, [1, 10], meta1='a', meta2=123)

        queue = Queue()
        run_id = str(uuid4())
        proc = ForkProcess(target=exp.run, args=(queue, 1989, run_id))

        proc.start()
        sleep(1)

        observations = []
        while not queue.empty():
            observations.append(queue.get())
            if len(observations) == 10:
                break

        proc.terminate()

        df = pd.DataFrame(observations)

        self.assertSequenceEqual([10, 13], df.shape)
        self.assertSequenceEqual(
            ['name', 'run_id', 'meta1', 'meta2', 'execution_id', 'start', 'end', 'errored', 'error_message', 'arg0',
             'call_start', 'call_end', 'duration'],
            df.columns.tolist()
        )
        self.assertSequenceEqual(['test_exp_1'] * 10, df.name.tolist())
        self.assertSequenceEqual([run_id] * 10, df.run_id.tolist())
        self.assertSequenceEqual([5, 7, 1, 10, 3, 7, 1, 9, 2, 10], df.arg0.astype(int).tolist())
        self.assertSequenceEqual(['a'] * 10, df.meta1.tolist())
        self.assertSequenceEqual([123] * 10, df.meta2.astype(int).tolist())

        self.assertEqual(df[df.errored].shape[0], 2)
