import os
from pathlib import Path

import pandas as pd

from finbourne_lab.common.recorder.base import BaseRecorder


class FileRecorder(BaseRecorder):
    """Recorder for writing experiment data to a local directory.

    """

    def __init__(self, directory: str, chunk_size: int = 5):
        """Constructor for the FileRecorder class.

        Args:
            directory (str): path of the write directory.
            chunk_size (int): the max size of an experiment's staging area before it's written out.

        """
        self.directory = directory
        Path(directory).mkdir(parents=True, exist_ok=True)

        super().__init__(chunk_size)

    def _send(self, name):
        df = pd.DataFrame(self.staging[name])
        fpath = f'{self.directory}/{name}.csv'
        df.to_csv(fpath, index=False, mode='a', header=not os.path.exists(fpath))

    def get_df(self, name: str) -> pd.DataFrame:
        """Get the data for a given experiment name from a local file as a pandas dataframe.

        Args:
            name (str): the name of the experiment's data to fetch.

        Returns:
            DataFrame: the corresponding data as a DataFrame
        """
        fpath = f'{self.directory}/{name}.csv'
        return pd.read_csv(fpath)