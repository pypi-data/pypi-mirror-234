from __future__ import annotations
from finbourne_lab.common.experiment import Experiment
from finbourne_lab.common.observation import Observation
from multiprocessing import Queue
import numpy as np
import sys
import traceback


class Shopper:
    """The shopper class takes a set of experiments and runs them at random when started in a convener.

    """

    def __init__(self, *experiments: Experiment):
        """Constructor for the Shopper class

        Args:
            *experiments (Experiment): experiments to run in the shopper.

        """
        if len(experiments) < 2:
            raise ValueError('Shopper must contain two or more experiments.')

        if not all(isinstance(e, Experiment) for e in experiments):
            args_str = ', '.join(type(e).__name__ for e in experiments)
            raise TypeError(f'All inputs must be experiments. Were {args_str}.')

        names = [e.exp_name for e in experiments]
        if len(set(names)) != len(names):
            names_str = ', '.join(names)
            raise ValueError(f'There are duplicate experiment names: {names_str}')

        self.experiments = experiments

    def run(self, queue: Queue, seed: int, run_id: str) -> None:

        np.random.seed(seed)

        while True:

            # pick random experiment
            ex = np.random.choice(self.experiments)

            args = ex.domain_sample()

            obs = Observation(args, name=ex.exp_name, run_id=run_id)
            obs.log_time('start')

            # noinspection PyBroadException
            # ^ That's sort of the point...
            try:
                runnable = ex.build_fn(*args)
                ex.measurement(obs, runnable)
                obs.log_time('end')

            except Exception:
                obs.log_time('end')
                obs['errored'] = True
                obs['error_message'] = ''.join(traceback.format_exception(*sys.exc_info()))

            queue.put(obs.data)

    def __add__(self, other: Shopper) -> Shopper:
        return Shopper(*self.experiments, *other.experiments)

    def __repr__(self):
        cls_name = type(self).__name__
        content = '\n  '.join(repr(e) for e in self.experiments)
        return f'{cls_name}(\n  {content}\n)'
