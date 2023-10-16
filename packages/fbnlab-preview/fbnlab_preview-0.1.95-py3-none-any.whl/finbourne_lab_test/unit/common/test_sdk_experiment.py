from finbourne_lab.common.sdk_experiment import SdkExperiment
import pandas as pd
import unittest
from multiprocessing import Queue
from multiprocessing.context import ForkProcess
from urllib3 import HTTPResponse
from time import sleep
from uuid import uuid4


def mock_sdk_call(application='fbn-mock', status=200, reason='ok'):

    def call(t):
        headers = [
            (f'{application}-meta-requestId', str(uuid4())),
            (f'{application}-meta-success', 'true' if status == 200 else 'false'),
            (f'{application}-meta-duration', str(int(1000*t/100)))
        ]
        sleep(t/100)
        return HTTPResponse(status=status, headers=headers, reason=reason)

    return call


class TestSdkExperiment(unittest.TestCase):

    def test_sdk_experiment_ctor(self):

        def fn(x):
            call = mock_sdk_call()
            return lambda: call(x)

        exp = SdkExperiment('ex', fn, [1, 10], application='fbn-mock', meta1='a', meta2=321)

        self.assertEqual(exp.exp_name, 'ex')

        self.assertEqual(1, len(exp.ranges))
        self.assertSequenceEqual(exp.ranges[0], [1, 10])

        self.assertEqual(exp.metadata['meta1'], 'a')
        self.assertEqual(exp.metadata['meta2'], 321)

        self.assertIsInstance(exp.build_fn(1)(), HTTPResponse)

    def test_sdk_experiment_run(self):

        def fn(x):
            call = mock_sdk_call()
            return lambda: call(x)

        exp = SdkExperiment('ex', fn, [1, 10], application='fbn-mock', meta1='a', meta2=321)

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

        self.assertSequenceEqual([10, 16], df.shape)
        self.assertSequenceEqual(
            ['name', 'run_id', 'application', 'meta1', 'meta2', 'execution_id', 'start', 'end', 'errored', 'error_message', 'arg0',
             'call_start', 'call_end', 'duration', 'failed', 'server_time'],
            df.columns.tolist()
        )
