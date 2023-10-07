from finbourne_lab.lusid.base import BaseLusidLab
from finbourne_lab.lusid import LusidExperiment


class LusidInstrumentLab(BaseLusidLab):
    """Lab class for lusid instrument endpoint methods.

    """

    def list_instruments_measurement(self, **kwargs) -> LusidExperiment:
        """Make an experiment object for lusid list instruments read performance.

        Keyword Args:
            x_rng (Union[int, List[int]]): the range to sample when getting x-many instruments. Given as a list containing
            two integers or a const int value. Defaults to [1, 5000].

        Returns:
            LusidExperiment: the list instruments experiment object.
        """
        method = self.lusid.instruments_api.list_instruments

        def build(x):
            return lambda: method(limit=x, _preload_content=False)

        rng = kwargs.get('x_rng', [1, 5000])
        return LusidExperiment('list_instruments', build, rng)
