from finbourne_lab.common.experiment import Experiment
from urllib3 import HTTPResponse
from typing import Callable, Any


class SdkExperiment(Experiment):
    """An experiment class for using finbourne's SDKs such as drive or lusid.

    """

    def __init__(self, name: str, build_fn: Callable, *ranges: Any, **kwargs: Any):
        """Constructor for the SdkExperiment class.

        Args:
            name (str): name of the sdk experiment
            build_fn (Callable): build function of the sdk experiment. Must return a parameterless fn that returns a
            http response object.
            *ranges (Any): parameter value ranges. Must be either constant values, pair of integers or a set of values.
            **metadata (Any): other values to be attached to observations.

        Keyword Args:
            application (str): the name of the finbourne application being used such as 'lusid'

        """

        if 'application' not in kwargs:
            raise ValueError('You must state the application this SDK corresponds to as a keyword arg. '
                             'E.g. application="lusid".')

        self.application = kwargs['application']

        super().__init__(name, build_fn, *ranges, **kwargs)

    def measurement(self, obs, runnable):

        obs.log_time('call_start')
        response = runnable()
        obs.log_time('call_end')
        obs['duration'] = (obs['call_end'] - obs['call_start']).total_seconds()

        if not isinstance(response, HTTPResponse):
            raise TypeError(
                "Response object was not an HTTPResponse instance. "
                "You might need to set _preload_content=False in your sdk method call."
            )

        if response.status >= 400:
            raise ValueError(
                f"Received error response from {self.application}: "
                f"status code = {response.status}, reason = {response.reason}"
            )

        obs['execution_id'] = response.headers.get(f'{self.application}-meta-requestId')
        obs['failed'] = not response.headers.get(f'{self.application}-meta-success')
        obs['server_time'] = int(response.headers.get(f'{self.application}-meta-duration')) / 1000
