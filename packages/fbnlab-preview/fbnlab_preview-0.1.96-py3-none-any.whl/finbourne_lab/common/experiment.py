from __future__ import annotations

import sys
import traceback
from multiprocessing import Queue
from typing import Tuple, Any
from uuid import uuid4

import numpy as np

from finbourne_lab.common.observation import Observation


class Experiment:
    """Base class for all experiments in finbourne lab.

    Experiments are responsible for sampling paramter values, running a build function given these values, and then running
    the result and making observations. It then puts the observation onto a queue.

    """

    def __init__(self, name, build_fn, *ranges, **metadata):
        """Constructor for the SdkExperiment class.

        Args:
            name (str): name of the experiment
            build_fn (Callable): build function of the sdk experiment. Must return a parameterless fn.
            *ranges (Any): parameter value ranges. Must be either constant values, pair of integers or a set of values.
            **metadata (Any): other values to be attached to observations.

        Keyword Args:
            application (str): the name of the finbourne application being used such as 'lusid'

        """

        self.exp_name = name
        self.build_fn = build_fn
        self.ranges = ranges
        self.metadata = metadata

        self.domain_sample()

    def __repr__(self):
        cls_name = type(self).__name__
        rngs_str = ', '.join(str(r) for r in self.ranges)
        return f'{cls_name}({self.exp_name}: {rngs_str})'

    def measurement(self, obs, runnable):
        obs.log_time('call_start')
        runnable()
        obs.log_time('call_end')
        obs['duration'] = (obs['call_end'] - obs['call_start']).total_seconds()
        obs['execution_id'] = str(uuid4())

    def domain_sample(self) -> Tuple[Any, ...]:

        args = []

        for rng in self.ranges:
            # Is it a constant value? If so, just add it to the args.
            if not hasattr(rng, '__len__') or isinstance(rng, str):
                args.append(rng)
            # Is it a range? This is either a list or tuple of length 2
            elif isinstance(rng, (list, tuple)) and len(rng) == 2:
                arg = int(np.random.randint(rng[0], rng[1] + 1))
                args.append(arg)
            # Is it a set of discrete elements? If so pick one at random
            elif isinstance(rng, set):
                args.append(np.random.choice(list(rng)))
            # Otherwise error
            else:
                raise ValueError(f'Received a bad parameter range def: {rng}. '
                                 f'Should be a constant val, list of size 2 or a set')

        return tuple(args)

    def run(self, queue: Queue, seed: int, run_id: str) -> None:

        np.random.seed(seed)

        while True:
            args = self.domain_sample()

            obs = Observation(args, name=self.exp_name, run_id=run_id, **self.metadata)
            obs.log_time('start')

            # noinspection PyBroadException
            # ^ That's sort of the point...
            try:
                runnable = self.build_fn(*args)
                self.measurement(obs, runnable)
                obs.log_time('end')

            except Exception:
                obs.log_time('end')
                obs['errored'] = True
                obs['error_message'] = ''.join(traceback.format_exception(*sys.exc_info()))

            queue.put(obs.data)
