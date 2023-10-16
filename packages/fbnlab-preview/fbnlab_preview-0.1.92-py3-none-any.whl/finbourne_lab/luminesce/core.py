from lumipy.provider import DType

from finbourne_lab.luminesce.experiment import LumiExperiment
from finbourne_lab.luminesce.base import BaseLumiLab


class CoreLumiLab(BaseLumiLab):
    """The core lumi lab builds experiments for measuring performance of the luminesce query coordinator and other bits
    of luminesce's core functionality.

    """

    def sys_registration_measurement(self, **kwargs):
        """Make an experiment for measuring the performance of querying sys.registration.

        Keyword Args:
            rows_rng (Union[int, List[int]]): the range to sample when getting x-many rows. Given as a list containing
            two integers or a const int value. Defaults to [1, 1000].

        Returns:
            LumiExperiment: experiment for the sys.registration measurement

        """
        rows_rng = kwargs.get('rows_rng', [1, 1000])
        sr = self.atlas.sys_registration
        return self._reader_experiment('core_sys_registration', sr, rows_rng, None)

    def sys_file_measurement(self, **kwargs):
        """Make an experiment for measuring the performance of querying sys.file.

        Keyword Args:
            rows_rng (Union[int, List[int]]): the range to sample when getting x-many rows. Given as a list containing
            two integers or a const int value. Defaults to [1, 200].

        Returns:
            LumiExperiment: experiment for the sys.file measurement

        """
        rows_rng = kwargs.get('rows_rng', [1, 200])
        sr = self.atlas.sys_file
        return self._reader_experiment('core_sys_file', sr, rows_rng, None)

    def sys_file_history_measurement(self, **kwargs):
        """Make an experiment for measuring the performance of querying sys.file.history.

        Keyword Args:
            rows_rng (Union[int, List[int]]): the range to sample when getting x-many rows. Given as a list containing
            two integers or a const int value. Defaults to [1, 10000].

        Returns:
            LumiExperiment: experiment for the sys.file.history measurement

        """
        rows_rng = kwargs.get('rows_rng', [1, 10000])
        sr = self.atlas.sys_file_history
        return self._reader_experiment('core_sys_file_history', sr, rows_rng, None)

    def sys_field_measurement(self, **kwargs):
        """Make an experiment for measuring the performance of querying sys.field.

        Keyword Args:
            rows_rng (Union[int, List[int]]): the range to sample when getting x-many rows. Given as a list containing
            two integers or a const int value. Defaults to [1, 1000].

        Returns:
            LumiExperiment: experiment for the sys.field measurement

        """
        rows_rng = kwargs.get('rows_rng', [1, 1000])
        sr = self.atlas.sys_field
        return self._reader_experiment('core_sys_field', sr, rows_rng, None)

    def sys_service_measurement(self, **kwargs):
        """Make an experiment for measuring the performance of querying sys.service.

        Keyword Args:
            rows_rng (Union[int, List[int]]): the range to sample when getting x-many rows. Given as a list containing
            two integers or a const int value. Defaults to [1, 1000].

        Returns:
            LumiExperiment: experiment for the sys.service measurement

        """
        rows_rng = kwargs.get('rows_rng', [1, 1000])
        sr = self.atlas.sys_service
        return self._reader_experiment('core_sys_service', sr, rows_rng, None)

    def sys_connection_measurement(self, **kwargs):
        """Make an experiment for measuring the performance of querying sys.connection.

        Keyword Args:
            rows_rng (Union[int, List[int]]): the range to sample when getting x-many rows. Given as a list containing
            two integers or a const int value. Defaults to [1, 10000].

        Returns:
            LumiExperiment: experiment for the sys.connection measurement

        """
        rows_rng = kwargs.get('rows_rng', [1, 10000])
        sr = self.atlas.sys_connection
        return self._reader_experiment('core_sys_connection', sr, rows_rng, None)

    def view_measurement(self, **kwargs):
        """Make a pair of experiments for measuring the performance of querying via joins.

        Keyword Args:
            original (Table): table to query data from without view.
            view (Table): view that represents the same query.
            rows_rng (Union[int, List[int]]): the range to sample when getting x-many rows. Given as a list containing
            two integers or a const int value. Defaults to [1, 10000].
            cols_rng (Union[int, List[int]]): the range to sample when getting y-many columns. Given as a list containing
            two integers or a const int value. Defaults to 25.

        Returns:
            List[LumiExperiment]: a pair of experiments for the view measurement. One for the query and one for the
            query via a view.
        """

        original = kwargs.get('original', self.atlas.testing10m)
        view = kwargs.get('view', self.atlas.testing10mview)

        rows_rng = kwargs.get('rows_rng', [1, 10000])
        cols_rng = kwargs.get('cols_rng', 25)

        ex = self._reader_experiment('core_select_view', view, rows_rng, cols_rng)
        base = self._reader_experiment('core_select_view_base', original, rows_rng, cols_rng)
        return ex, base

    def join_measurement(self, **kwargs):
        """Make a series of experiments for measuring join performance in the luminesce query coordinator.

        Keyword Args:
            rows_rng (Union[int, List[int]]): the range to sample when getting x-many rows. Given as a list containing
            two integers or a const int value. Defaults to [1, 10000].
            cols_rng (Union[int, List[int]]): the range to sample when getting y-many columns. Given as a list containing
            two integers or a const int value. Defaults to 5.
            on_type (DType, Set[DType]): a type or set of types to do the join. A separate pair of experiments will be
            generated doe each type. Defaults to {Dtype.Text, DType.DateTime, DType.Int}.

        Returns:
            List[LumiExperiment]: a list of experiments for the join performance measurements.
        """

        p = self.atlas.testing10m()

        rows_rng = kwargs.get('rows_rng', [1, 10000])
        cols_rng = kwargs.get('cols_rng', 5)
        on_type = kwargs.get('on_type', {DType.Text, DType.Int, DType.DateTime})

        experiments = []
        for t in on_type:
            def fn(x, y, z):
                tv = self.col_sample(p, y, z).limit(x).to_table_var()

                tva = tv.with_alias('A')
                tvb = tv.with_alias('B')

                join_col_name = [c for c in tv.get_columns() if c.meta.dtype == z][0].meta.field_name
                ca = tva[join_col_name]
                cb = tvb[join_col_name]

                return tva.inner_join(tvb, ca == cb).select('*')

            def baseline(x, y, z):
                tv = self.col_sample(p, y, z).limit(x).to_table_var()
                return tv.select('*').limit(1)

            name = f'core_join_{t.name.lower()}'
            ex = LumiExperiment(name, fn, rows_rng, cols_rng, t)
            experiments.append(ex)
            base = LumiExperiment(name + '_base', baseline, rows_rng, cols_rng, t)
            experiments.append(base)

        return experiments
