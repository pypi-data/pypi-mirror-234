from abc import ABC, abstractmethod
import pandas as pd
from finbourne_lab.common.observation import Observation


class BaseRecorder(ABC):
    """Base class for all data recorder classes in Finbourne Lab.

    """

    def __init__(self, chunk_size: int):
        """Constructor of the BaseRecorder class.

        Args:
            chunk_size (int): the max size of an experiment's staging area before it's written out.

        """

        self.chunk_size = chunk_size
        self.staging = {}

    @abstractmethod
    def _send(self, name: str) -> None:
        """Send all data corresponding to the given name to the data store.

        Args:
            name (str): the name of the experiment to send out.

        """
        raise NotImplementedError()

    def put(self, obs: Observation) -> None:
        """Add an observation to the staging area. When there are self.chunk_size-many or more send will be triggered.

        Args:
            obs (Observation): the observation to add.

        """

        name = obs['name']

        if name not in self.staging:
            self.staging[name] = []

        obs_list = self.staging[name]

        obs_list.append(obs)

        if len(obs_list) >= self.chunk_size:
            self._send(name)
            self.staging[name] = []

    def flush(self) -> None:
        """Send all staged data to the data store.

        """
        for name, obs_list in self.staging.items():
            if len(obs_list) == 0:
                continue

            self._send(name)
            self.staging[name] = []

    def put_all(self, queue) -> None:
        """Empty out the queue into the staging area.

        Args:
            queue (Queue): the multiprocessing Queue instance that the experiments are pushing observations to.

        """
        while not queue.empty():
            obs = queue.get()
            self.put(obs)

    @abstractmethod
    def get_df(self, name: str) -> pd.DataFrame:
        """Get the data for a given experiment name from the data store as a pandas dataframe.

        Args:
            name (str): the name of the experiment's data to fetch.

        Returns:
            DataFrame: the corresponding data as a DataFrame
        """
        raise NotImplementedError()


