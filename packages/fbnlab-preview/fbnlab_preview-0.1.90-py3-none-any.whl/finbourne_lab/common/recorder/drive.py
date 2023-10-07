import lumipy as lm
import pandas as pd

from finbourne_lab.common.recorder.base import BaseRecorder


class DriveRecorder(BaseRecorder):
    """Recorder for writing experiment data to a drive directory.

    """

    def __init__(self, atlas, directory: str, chunk_size: int = 5):
        """Constructor for the DriveRecorder class.

        Args:
            atlas (Atlas): atlas to use when writing to drive.
            directory (str): directory in drive to write to.
            chunk_size (int): the max size of an experiment's staging area before it's written out.

        """
        self.directory = directory
        self.files = atlas.drive_file
        self.write = atlas.drive_saveas
        self.read = atlas.drive_csv
        super().__init__(chunk_size)

    def _file_exists(self, name):
        f = self.files(root_path=self.directory)
        df = f.select('*').where(f.name == f'{name}.csv').go(quiet=True)
        return df.shape[0] == 1

    def _send(self, name):
        df = pd.DataFrame(self.staging[name])
        tv = lm.from_pandas(df)

        if self._file_exists(name):
            csv = self.read(file=f'{self.directory}/{name}.csv').select('*')
            tv2 = csv.union(tv.select('*')).to_table_var()
            q = self.write(tv2, type='csv', path=self.directory, file_names=name).select('*')
        else:
            q = self.write(tv, type='csv', path=self.directory, file_names=name).select('*')

        q.go_async()

    def get_df(self, name):
        """Get the data for a given experiment name from a drive file as a pandas dataframe.

        Args:
            name (str): the name of the experiment's data to fetch.

        Returns:
            DataFrame: the corresponding data as a DataFrame
        """
        csv = self.read(file=f'{self.directory}/{name}.csv', infer_type_row_count=10)
        return csv.select('*').go(quiet=True)