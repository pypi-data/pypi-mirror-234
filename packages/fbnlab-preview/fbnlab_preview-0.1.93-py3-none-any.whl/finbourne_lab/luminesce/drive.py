from finbourne_lab.luminesce.base import BaseLumiLab


class DriveLumiLab(BaseLumiLab):
    """The drive lumi lab builds experiments for measuring the performance of drive providers.

    """

    def drive_csv_read_measurement(self, **kwargs):
        """Make an experiment object for drive.csv read performance.

        Keyword Args:
            rows_rng (Union[int, List[int]]): the range to sample when getting x-many rows. Given as a list containing
            two integers or a const int value. Defaults to [1, 10000].
            file_path (str): the file path in drive to read from.

        Returns:
            LumiExperiment: the drive.csv read experiment.
        """
        rows_rng = kwargs.get('rows_rng', [1, 10000])
        file_path = kwargs.get('file_path', "/honeycomb/testing/luminesceTest100k.csv")
        return self._file_reader_experiment('drive_read_csv', self.atlas.drive_csv, file_path, rows_rng)

    def drive_excel_read_measurement(self, **kwargs):
        """Make an experiment for drive.excel read performance.

        Keyword Args:
            rows_rng (Union[int, List[int]]): the range to sample when getting x-many rows. Given as a list containing
            two integers or a const int value. Defaults to [1, 10000].
            file_path (str): the file path in drive to read from.

        Returns:
            LumiExperiment: the drive.excel read experiment.
        """
        rows_rng = kwargs.get('rows_rng', [1, 10000])
        file_path = kwargs.get('file_path', "/honeycomb/testing/luminesceTest100k.xlsx")
        return self._file_reader_experiment('drive_read_excel', self.atlas.drive_excel, file_path, rows_rng)

    def drive_csv_write_measurement(self, **kwargs):
        """Make a pair of experiments for drive csv write performance.

        Keyword Args:
            source (Table): the source table to read data from for writing it to drive.
            rows_rng (Union[int, List[int]]): the range to sample when getting x-many rows. Given as a list containing
            two integers or a const int value. Defaults to [1, 10000].
            cols_rng (Union[int, List[int]]): the range to sample when getting y-many columns. Given as a list containing
            two integers or a const int value. Defaults to 50.
            file_path (str): the file path in drive to write to.

        Returns:
            List[LumiExperiment]: the drive csv write experiment and the associated baseline experiment.
        """
        source = kwargs.get('source', self.atlas.testing10m())
        rows_rng = kwargs.get('rows_rng', [1, 10000])
        cols_rng = kwargs.get('cols_rng', 50)
        cols_rng_str = self.make_cols_rng_str(cols_rng)
        file_path = kwargs.get('file_path', f'/honeycomb/testing/luminesceTest_{cols_rng_str}Cols.csv')

        return self._file_writer_experiment('drive_write_csv', source, self.atlas.drive_saveas, file_path, rows_rng, cols_rng)

    def drive_excel_write_measurement(self, **kwargs):
        """Make a pair of experiments for drive excel write performance.

        Keyword Args:
            source (Table): the source table to read data from for writing it to drive.
            rows_rng (Union[int, List[int]]): the range to sample when getting x-many rows. Given as a list containing
            two integers or a const int value. Defaults to [1, 10000].
            cols_rng (Union[int, List[int]]): the range to sample when getting y-many columns. Given as a list containing
            two integers or a const int value. Defaults to 50.
            file_path (str): the file path in drive to write to.

        Returns:
            List[LumiExperiment]: the drive excel write experiment and the associated baseline experiment.
        """
        source = kwargs.get('source', self.atlas.testing10m())
        rows_rng = kwargs.get('rows_rng', [1, 10000])
        cols_rng = kwargs.get('cols_rng', 50)
        cols_rng_str = self.make_cols_rng_str(cols_rng)
        file_path = kwargs.get('file_path', f'/honeycomb/testing/luminesceTest_{cols_rng_str}Cols.xlsx')

        return self._file_writer_experiment('drive_write_excel', source, self.atlas.drive_saveas, file_path, rows_rng, cols_rng)