import datetime as dt
from multiprocessing import Queue
from multiprocessing.context import ForkProcess
from typing import Optional, Union
from uuid import uuid4

import numpy as np
from tqdm import tqdm

from finbourne_lab.common.experiment import Experiment
from finbourne_lab.common.recorder.base import BaseRecorder
from finbourne_lab.common.shopper import Shopper
from finbourne_lab.common.recorder.no_op import NoOpRecorder


class Convener:
    """The Convener class is responsible for running an experiment/shopper with a given degree of paralellism, and
    the recorder for storing their observations.

    """

    def __init__(
            self,
            to_run: Union[Experiment, Shopper],
            recorder: Union[BaseRecorder, None],
            n_parallel: Optional[int] = 1,
    ):
        """Constructor for the Convener class.

        Args:
            to_run (Union[Experiment, Shopper]): the experiment/shopper instance to run in the convener.
            recorder (BaseRecorder): recorder to record experimental observations with.
            n_parallel (int): number of parallel copies to run of 'to_run'. Defaults to one.
        """

        self.to_run = to_run
        if recorder is None:
            print(f'⚠️ No client-side data is being recorded (recorder = None)')
            recorder = NoOpRecorder()
        self.recorder = recorder
        self.n_parallel = n_parallel

    @staticmethod
    def _pbar(time_limit):

        # Very important. Do not remove.
        emoji = np.random.choice(['🧪', '🔭', '⚗️', '🧬', '🔬', '📐'])

        if time_limit is None:
            return tqdm(desc=f'{emoji}Doing Science Forever! ', bar_format='{desc}|{bar:30}|(∞️)')
        else:
            return tqdm(
                desc=f'{emoji}Doing Science! ',
                total=time_limit,
                bar_format='{desc}|{bar:30}|{percentage:3.0f}% ' + f'(Running for {time_limit}s)',
                colour='GREEN'
            )

    def go(self, time_limit: Union[int, None]):
        """Run the experiment or shopper for a period of time.

        Args:
            time_limit (Union[int, None]): time to run for. If set to None it will run indefinitely.

        """

        queue = Queue(maxsize=-1)
        run_id = str(uuid4())
        seed = int(np.random.randint(10000))

        def make_process(i):
            return ForkProcess(target=self.to_run.run, args=(queue, seed + i, run_id))

        ex_processes = [make_process(i) for i in range(self.n_parallel)]

        try:

            with self._pbar(time_limit) as t:
                start = dt.datetime.utcnow()
                period = lambda: int((dt.datetime.utcnow() - start).total_seconds())
                criterion = lambda: time_limit is None or period() < time_limit

                for p in ex_processes:
                    t.update(period() - t.n)
                    p.start()

                while True:
                    t.update(period() - t.n)

                    while not queue.empty() and criterion():
                        self.recorder.put(queue.get())
                        t.update(period() - t.n)

                    if not criterion():
                        break

                t.update(period() - t.n)

                for p in ex_processes:
                    p.terminate()

        except KeyboardInterrupt:
            print('🛑 Halting run...')
            for p in ex_processes:
                p.terminate()

        self.recorder.put_all(queue)
        self.recorder.flush()
