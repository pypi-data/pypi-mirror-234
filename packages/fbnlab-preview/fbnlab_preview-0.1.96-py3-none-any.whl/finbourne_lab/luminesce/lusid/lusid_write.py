import string
from math import ceil
import numpy as np

from finbourne_lab.luminesce.experiment import LumiExperiment
from finbourne_lab.luminesce.lusid.base import LusidLumiLabBase


class LusidLumiLabWrite(LusidLumiLabBase):

    def __init__(self, atlas):
        super().__init__(atlas, False)

    def lusid_instrument_writer_measurement(self, **kwargs):
        """Make a pair of experiments (one main, one baseline) for the instrument writer measurement.

        Notes:
            The baseline experiment measures the time to read out test data into a table var before going to the writer.
            The main step is the test data read + writer call. To measure the writer the baseline result should be
            subtracted from the main

        Keyword Args:
            rows_rng (Union[int, List[int]]): the range to sample when getting x-many rows. Given as a list containing
            two integers or a const int value. Defaults to [1, 1000].

        Returns:
            List[LumiExperiment]: a pair of experiments for the measurement (main, base).

        """
        rows_rng = kwargs.get('rows_rng', [1, 1000])

        def baseline(x):
            scope = self._make_write_scope('instrument')
            tv = self.in_gen.assemble_write_data(scope, x)
            return tv.select('*').limit(1)

        def build(x):
            scope = self._make_write_scope('instrument')
            tv = self.in_gen.assemble_write_data(scope, x)
            writer = self.atlas.lusid_instrument_writer(to_write=tv)
            return writer.select('*')

        name = 'lusid_write_instrument'
        ex = LumiExperiment(name, build, rows_rng)
        base = LumiExperiment(name + '_base', baseline, rows_rng)
        return ex, base

    def lusid_portfolio_writer_measurement(self, **kwargs):
        """Make a pair of experiments (one main, one baseline) for the portfolio writer measurement.

        Notes:
            The baseline experiment measures the time to read out test data into a table var before going to the writer.
            The main step is the test data read + writer call. To measure the writer the baseline result should be
            subtracted from the main

        Keyword Args:
            rows_rng (Union[int, List[int]]): the range to sample when getting x-many rows. Given as a list containing
            two integers or a const int value. Defaults to [1, 25].

        Returns:
            List[LumiExperiment]: a pair of experiments for the measurement (main, base).

        """
        rows_rng = kwargs.get('rows_rng', [1, 25])

        def baseline(x):
            scope = self._make_write_scope('portfolio')
            tv = self.pf_gen.assemble_write_data(scope, x)
            return tv.select('*').limit(1)

        def build(x):
            scope = self._make_write_scope('portfolio')
            tv = self.pf_gen.assemble_write_data(scope, x)
            writer = self.atlas.lusid_portfolio_writer(to_write=tv)
            return writer.select('*')

        name = 'lusid_write_portfolio'
        ex = LumiExperiment(name, build, rows_rng)
        base = LumiExperiment(name + '_base', baseline, rows_rng)
        return ex, base

    def lusid_portfolio_holding_writer_measurement(self, **kwargs):
        """Make a list of experiments for the portfolio holdings writer measurement over different data shapes.

        Notes:
            The baseline experiment measures the time to read out test data into a table var before going to the writer.
            The main step is the test data read + writer call. To measure the writer the baseline result should be
            subtracted from the main

            Data shape is the number of portfolios the holdings are spread over. This is parameterised as the number of
            holdings per portfolio in a scope. A clean test scope will be created for a given shape for each write.

        Keyword Args:
            rows_rng (Union[int, List[int]]): the range to sample when getting x-many rows. Given as a list containing
            two integers or a const int value. Defaults to [1, 10000].
            skip_ensure (bool): whether to skip the ensure step. Defaults to False.
            hldg_per_pf_set (Set[int]): a set of integers that define the different data shapes to test for. Each value
            is the number of holdings per portfolio. Defaults to 100, 1000, 10000.

        Returns:
            List[LumiExperiment]: a list of experiments containing the main and base for each data shape.

        """

        rows_rng = kwargs.get('rows_rng', [1, 10000])
        hldg_per_pf_set = kwargs.get('hldg_per_pf_set', {100, 1000, 10000})

        experiments = []
        for hldg_per_pf in hldg_per_pf_set:
            def build(x, y):
                scope = self._make_write_scope('holding')
                n_portfolios = ceil(x / y)
                self.pf_gen.ensure(scope, n_portfolios)
                tv = self.hl_gen.assemble_write_data(scope, n_portfolios, y)
                writer = self.atlas.lusid_portfolio_holding_writer(to_write=tv)
                return writer.select('*')

            def baseline(x, y):
                scope = self._make_write_scope('holding')
                n_portfolios = ceil(x / y)
                tv = self.hl_gen.assemble_write_data(scope, n_portfolios, y)
                return tv.select('*').limit(1)

            name = f'lusid_write_holding_{hldg_per_pf}'
            ex = LumiExperiment(name, build, rows_rng, hldg_per_pf)
            experiments.append(ex)
            base = LumiExperiment(name + '_base', baseline, rows_rng, hldg_per_pf)
            experiments.append(base)

        return experiments

    def lusid_portfolio_txn_writer_measurement(self, **kwargs):
        """Make a list of experiments for the portfolio txns writer measurement over different data shapes.

        Notes:
            The baseline experiment measures the time to read out test data into a table var before going to the writer.
            The main step is the test data read + writer call. To measure the writer the baseline result should be
            subtracted from the main

            Data shape is the number of portfolios the txns are spread over. This is parameterised as the number of
            txns per portfolio in a scope. A clean test scope will be created for a given shape for each write.

        Keyword Args:
            rows_rng (Union[int, List[int]]): the range to sample when getting x-many rows. Given as a list containing
            two integers or a const int value. Defaults to [1, 10000].
            skip_ensure (bool): whether to skip the ensure step. Defaults to False.
            txns_per_pf_set (Set[int]): a set of integers that define the different data shapes to test for. Each value
            is the number of txns per portfolio. Defaults to 100, 1000, 10000.

        Returns:
            List[LumiExperiment]: a list of experiments containing the main and base for each data shape.

        """

        rows_rng = kwargs.get('rows_rng', [1, 10000])
        txns_per_pf_set = kwargs.get('txns_per_pf_set', {100, 1000, 10000})

        experiments = []
        for txns_per_pf in txns_per_pf_set:
            def build(x, y):
                scope = self._make_write_scope('txn')
                n_portfolios = ceil(x / y)
                self.pf_gen.ensure(scope, n_portfolios)
                tv = self.tx_gen.assemble_write_data(scope, n_portfolios, y)
                writer = self.atlas.lusid_portfolio_txn_writer(to_write=tv)
                return writer.select('*')

            def baseline(x, y):
                scope = self._make_write_scope('txn')
                n_portfolios = ceil(x / y)
                tv = self.tx_gen.assemble_write_data(scope, n_portfolios, y)
                return tv.select('*').limit(1)

            name = f'lusid_write_txn_{txns_per_pf}'
            ex = LumiExperiment(name, build, rows_rng, txns_per_pf)
            experiments.append(ex)
            base = LumiExperiment(name + '_base', baseline, rows_rng, txns_per_pf)
            experiments.append(base)

        return experiments

    def _make_write_scope(self, label: str) -> str:
        letters = list(string.ascii_lowercase + string.digits)
        rand_id = ''.join(np.random.choice(letters, size=8))
        return f'fbn-lab-{label}-writer-{rand_id}'
