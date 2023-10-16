import numpy as np

from finbourne_lab.common.base_lab import BaseLab
from finbourne_lab.luminesce.experiment import LumiExperiment


class BaseLumiLab(BaseLab):
    """The base lumi lab is the base class for all luminesce lab classes. It encapsulates useful shared functionality
    for building luminesce experiments.

    """

    def __init__(self, atlas, verbose=False):
        """Constructor for the base lumi lab class.

        Args:
            atlas (Atlas): the lumipy atlas to run luminesce queries with.
            verbose (bool): whether to run in verbose mode. This will give feedback on ensure (entity) steps
            during running. Defaults to false.

        """

        self.atlas = atlas
        self.verbose = verbose

    def log(self, line, indent=0):
        """Print a line with a given number of spaces indented if verbose=True

        Args:
            line (str): line to print.
            indent (int): number of spaces to indent by (defaults to 0).

        """
        if self.verbose:
            print(' '*indent + line)

    @staticmethod
    def col_sample(p, y, idx_type=None):
        if y is None:
            return p.select('*')

        if idx_type is None:
            cols = np.random.choice(p.get_columns(), size=y, replace=False)
        else:
            idx_col = np.random.choice([c for c in p.get_columns() if c.meta.dtype == idx_type])
            other_cols = [c for c in p.get_columns() if hash(c) != hash(idx_col)]

            cols = [idx_col] + list(np.random.choice(other_cols, size=y - 1, replace=True))

        return p.select(*cols)

    @staticmethod
    def make_cols_rng_str(cols_rng):
        if cols_rng is None:
            return 'all'
        elif isinstance(cols_rng, int):
            return str(cols_rng)
        elif isinstance(cols_rng, (list, tuple)) and len(cols_rng) == 2:
            return f'{cols_rng[0]}-{cols_rng[1]}'
        else:
            raise ValueError('Cols range must be None, an int or a pair of ints.')

    def _reader_experiment(self, name, reader, rows_rng, cols_rng):

        def build(x, y):
            p = reader()
            return self.col_sample(p, y).limit(x)

        return LumiExperiment(name, build, rows_rng, cols_rng)

    def _file_reader_experiment(self, name, reader, fpath, rows_rng):

        def build(x, y):
            return reader(file=y, apply_limit=x).select('*')

        return LumiExperiment(name, build, rows_rng, fpath)

    def _writer_experiment(self, name, writer, test_data_path, rows_rng):

        csv = self.atlas.drive_csv(file=test_data_path, apply_limit=rows_rng[1])

        def base_fn(x):
            tv = csv.select('*').limit(x).to_table_var()
            return tv.select('*').limit(1)

        def writer_fn(x):
            tv = csv.select('*').limit(x).to_table_var()
            return writer(to_write=tv).select('*')

        ex = LumiExperiment(name, writer_fn, rows_rng)
        base = LumiExperiment(name, base_fn, rows_rng)
        return ex, base

    def _file_writer_experiment(self, name, source, writer, file_path, rows_rng, cols_rng):

        def base_fn(x, y, z):
            tv = self.col_sample(source, y).limit(x).to_table_var()
            return tv.select('*').limit(1)

        def write_fn(x, y, z):
            tv = self.col_sample(source, y).limit(x).to_table_var()
            parts = z.split('/')
            directory = '/'.join(parts[:-1])
            filename, file_type = parts[-1].split('.')
            if file_type.lower() == 'xlsx':
                file_type = 'excel'
            return writer(tv, type=file_type, path=directory, file_names=filename).select('*')

        ex = LumiExperiment(name, write_fn, rows_rng, cols_rng, file_path)
        base = LumiExperiment(name + '_base', base_fn, rows_rng, cols_rng, file_path)
        return ex, base
