import numpy as np
import pandas as pd
from typing import Callable, Any, Union
from finbourne_lab.common.experiment import Experiment
from lumipy.lumiflex._common.str_utils import to_snake_case
from lumipy.lumiflex._table.operation import TableOperation


# noinspection SqlNoDataSourceInspection,SqlResolve
class LumiExperiment(Experiment):
    """Experiment class for running luminesce experiments.

    """

    def __init__(self, name: str, build_fn: Callable, *ranges: Any, **metadata: Any):
        """Constructor of the LumiExperiment class.

        Args:
            name (str): name of the luminesce experiment
            build_fn (Callable): build function of the luminesce experiment. Must return a query object given some values.
            *ranges (Any): parameter value ranges. Must be either constant values, a pair of integers or a set of values.
            **metadata (Any): other values to be attached to observations or the lumipy client to be used.

        Keyword Args:
            client (Client): the lumipy client to use when running SQL string experiments
            keep_for (int): time to keep query results for. Defaults to 900s.
            check_period (float): wait period before checking a query status. Defaults to 0.025s
            skip_download (bool): whether to skip the download step. Defaults to true.

        Notes:
            When running a sql str-based experiment you must supply the client as a keyword arg. For example,

            ```
            client = lm.get_client()

            def build(x):
                return f'select * from lusid.instrument limit {x}'

            ex = LumiExperiment('lusid_instrument', build, [1, 10000], client=client)
            ```

        """

        self.client = metadata.get('client')
        if self.client is not None:
            del metadata['client']
            self.client.run('select LusidInstrumentId from lusid.instrument limit 1', return_job=True)

        self.keep_for = metadata.get('keep_for', 900)
        self.check_period = metadata.get('check_period', 0.025)
        self.skip_download = metadata.get('skip_download', True)

        super().__init__(name, build_fn, *ranges, **metadata)

    def measurement(self, obs, qry: Union[TableOperation, str]):

        obs.log_time('send')
        if hasattr(qry, 'go_async'):
            job = qry.go_async(keep_for=self.keep_for)
        elif isinstance(qry, str):
            if self.client is None:
                raise ValueError(f'You must give a client object when running a SQL string.')
            job = self.client.run(qry, return_job=True)
        else:
            raise TypeError('Build function returned an unsupported type. Must be either a lumipy query object or str.')

        obs['execution_id'] = job.ex_id
        obs.log_time('submitted')
        obs['start_query_time'] = (obs['submitted'] - obs['send']).total_seconds()

        job.interactive_monitor(True, self.check_period)

        obs.log_time('get')
        obs['query_time'] = (obs['get'] - obs['submitted']).total_seconds()

        def make_pair(x):
            lhs, rhs = x.split(':')
            name = ''.join(s for s in lhs.strip() if s.isalnum()).title() + 'Time'
            val = float(rhs.strip().strip(' ms')) * 0.001
            return to_snake_case(name), val

        server_side = {}
        arr = [line for line in job.get_progress().split('\n') if ' ms' in line]
        for time_name, time_val in map(make_pair, arr):
            server_side[time_name] = time_val

        ss_cols = ['prep_time', 'providers_time', 'mergesql_time', 'filltable_time', 'total_time']
        for col in ss_cols:
            if col not in server_side:
                obs[col] = np.NaN
            else:
                obs[col] = server_side[col]

        if self.skip_download:
            obs['download_finish'] = pd.NaT
            obs['obs_rows'] = None
            obs['obs_cols'] = None
            obs['download_time'] = None
            return

        df = job.get_result(False)
        obs.log_time('download_finish')
        obs['obs_rows'] = df.shape[0]
        obs['obs_cols'] = df.shape[1]
        obs['download_time'] = (obs['download_finish'] - obs['get']).total_seconds()
