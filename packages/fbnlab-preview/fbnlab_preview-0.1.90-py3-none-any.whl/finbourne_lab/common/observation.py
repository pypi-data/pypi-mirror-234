from datetime import datetime

from pandas import NaT


class Observation:
    """A class that represents a single observation in an experiment. These are created and pushed onto
    a concurrent queue, then pulled from the queue and written by the recorder.

    """

    def __init__(self, args, **metadata):

        required_meta = ['name', 'run_id']
        if not all(m in metadata for m in required_meta):
            raise ValueError(
                f'An observation\'s metadata must at minimum contain the experiment name and the run_id.'
            )

        features = {
            'execution_id': None,
            'start': NaT,
            'end': NaT,
            'errored': False,
            'error_message': None,
        }
        arg_vals = {f'arg{i}': a for i, a in enumerate(args)}
        self.data = {**metadata, **features, **arg_vals}

    def log_time(self, key):
        self.data[key] = datetime.utcnow()

    def __setitem__(self, key, value):
        self.data[key] = value

    def __getitem__(self, item):
        return self.data[item]
