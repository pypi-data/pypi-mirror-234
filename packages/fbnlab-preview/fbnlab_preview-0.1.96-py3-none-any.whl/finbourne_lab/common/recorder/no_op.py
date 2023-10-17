from finbourne_lab.common.recorder.base import BaseRecorder, Observation
import pandas as pd


class NoOpRecorder(BaseRecorder):

    def __init__(self):
        super().__init__(1)

    def put(self, obs: Observation) -> None:
        pass

    def _send(self, name):
        pass

    def get_df(self, name: str) -> pd.DataFrame:
        raise NotImplementedError("This is a no-op recorder. There is no data.")
