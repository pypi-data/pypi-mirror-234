from finbourne_lab.luminesce.base import BaseLumiLab
from finbourne_lab.luminesce.lusid.ensure import PortfolioData, InstrumentData, HoldingsData, TxnsData


class LusidLumiLabBase(BaseLumiLab):
    """The lusid lumi lab encapsulates standard measurements for lusid luminesce providers.

    """

    def __init__(self, atlas, verbose):
        """Creator for the LusidLumiLab class.

        Args:
            atlas (Atlas): the lumipy atlas to run luminesce queries with.
            verbose (bool): whether to run in verbose mode. This will give feedback on ensure (entity) steps
            during running.

        """

        self.pf_gen = PortfolioData(atlas, not verbose)
        self.in_gen = InstrumentData(atlas, not verbose)
        self.hl_gen = HoldingsData(atlas, not verbose)
        self.tx_gen = TxnsData(atlas, not verbose)

        super().__init__(atlas, verbose)
