from finbourne_lab.common.base_lab import BaseLab
from finbourne_lab.lusid import LusidClient


class BaseLusidLab(BaseLab):

    def __init__(self, **kwargs):
        self.lusid = LusidClient(**kwargs)
