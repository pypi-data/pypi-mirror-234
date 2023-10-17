from finbourne_lab import Shopper
from finbourne_lab.common.experiment import Experiment
from multiprocessing.context import ForkProcess
from multiprocessing import Queue
import unittest
from time import sleep


class TestShopper(unittest.TestCase):

    @staticmethod
    def make_experiment(name, m, c):

        def fn(x):
            return lambda: x * m + c

        return Experiment(name, fn, [1, 10], meta1='a')

    def test_shopper_ctor(self):
        ex1 = self.make_experiment('ex1', 0.001, 0.1)
        ex2 = self.make_experiment('ex2', 0.0005, 0.2)
        ex3 = self.make_experiment('ex3', 0.002, 0.05)

        shopper = Shopper(ex1, ex2, ex3)
        self.assertEqual(3, len(shopper.experiments))
        self.assertTrue(all(isinstance(e, Experiment) for e in shopper.experiments))

    def test_shopper_run(self):
        ex1 = self.make_experiment('ex1', 0.001, 0.1)
        ex2 = self.make_experiment('ex2', 0.0005, 0.2)
        ex3 = self.make_experiment('ex3', 0.002, 0.05)

        shopper = Shopper(ex1, ex2, ex3)

        queue = Queue()
        run_id = '<a guid>'
        proc = ForkProcess(target=shopper.run, args=(queue, 1989, run_id))

        proc.start()
        sleep(1)

        observations = []
        while not queue.empty():
            observations.append(queue.get())
            if len(observations) == 10:
                break

        proc.terminate()
        exp_names = [obs['name'] for obs in observations]

        self.assertSequenceEqual(
            ['ex3', 'ex1', 'ex3', 'ex1', 'ex1', 'ex1', 'ex2', 'ex3', 'ex3', 'ex2'],
            exp_names
        )
