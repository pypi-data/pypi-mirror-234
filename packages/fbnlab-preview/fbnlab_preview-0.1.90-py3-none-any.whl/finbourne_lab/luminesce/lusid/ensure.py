from abc import ABC, abstractmethod
import datetime as dt
import lumipy as lm
from lumipy.lumiflex._common.str_utils import indent_str
from termcolor import colored


class BaseData(ABC):

    def __init__(self, atlas, writer, quiet):
        self.label = type(self).__name__
        self.atlas = atlas
        self.writer = writer
        self.quiet = quiet

    def log(self, txt):
        if not self.quiet:
            print(colored(f'[{self.label}]: ', 'blue') + txt)

    @abstractmethod
    def check_data(self, **kwargs):
        pass

    @abstractmethod
    def assemble_write_data(self, **kwargs):
        pass

    def ensure(self, **kwargs):
        self.log(f'Checking data {kwargs}')
        if self.check_data(**kwargs):
            self.log('Data are present. Ready to go!')
            return

        self.log('Data not ready. Writing...')
        to_write = self.assemble_write_data(**kwargs)

        writer = self.writer(to_write=to_write)
        cols = [writer.write_error, writer.write_error_detail]
        errs = writer.select(*cols).where(cols[0].is_not_null()).go(quiet=True)

        if len(errs) > 0:
            df = errs.head(5)
            err_msgs = "\n\n".join(df['WriteError'] + "\n" + df['WriteErrorDetail'])
            raise ValueError(f'Write failed!\n{indent_str(err_msgs)}')

        self.log('Data written. Ready to go!')

    def luids_table_var(self, scope, row_lim):
        inst = self.atlas.lusid_instrument()
        win = lm.window(lower=None)
        q = inst.select(
            inst.lusid_instrument_id, inst.client_internal, Index=win.row_number() - 1
        )
        if scope is not None:
            q = q.where(inst.scope == scope)

        return q.limit(
            row_lim
        ).to_table_var()


class PortfolioData(BaseData):

    def __init__(self, atlas, quiet):
        super().__init__(atlas, atlas.lusid_portfolio_writer, quiet)

    def check_data(self, scope, n_portfolios):
        pf = self.atlas.lusid_portfolio()
        df = pf.select(pf_count=pf.portfolio_code.count()).where(pf.portfolio_scope == scope).go(quiet=True)
        return df.iloc[0, 0] == n_portfolios

    def assemble_write_data(self, scope, n_portfolios):
        t = self.atlas.tools_range(n_portfolios, 0, 1)
        pf_codes = 'lumi-test-pf-' + t.value.cast(str)
        cols = {
            'BaseCurrency': 'GBP',
            'Created': dt.datetime(2009, 12, 31, 23),
            'Description': 'perf test portfolio',
            'DisplayName': pf_codes,
            'PortfolioCode': pf_codes,
            'PortfolioScope': scope,
            'PortfolioType': 'Transaction',
            'SubHoldingKeys': None,
        }
        return t.select(**cols).to_table_var()

    def ensure(self, scope, n_portfolios):
        super().ensure(scope=scope, n_portfolios=n_portfolios)


class InstrumentData(BaseData):

    def __init__(self, atlas, quiet):
        super().__init__(atlas, atlas.lusid_instrument_writer, quiet)

    def check_data(self, scope, n_instruments):
        ins = self.atlas.lusid_instrument()
        df = ins.select(ICount=ins.lusid_instrument_id.count()).where(ins.scope == scope).go(quiet=True)
        return df.iloc[0, 0] == n_instruments

    def assemble_write_data(self, scope, n_instruments):
        t = self.atlas.tools_range(n_instruments, 0, 1)
        cols = {
            'ClientInternal': 'lumi-test-instrument-' + t.value.cast(str),
            'DisplayName': 'Test Instrument ' + t.value.cast(str),
            'DomCcy': 'USD',
            'Scope': scope,
        }
        return t.select(**cols).to_table_var()

    def ensure(self, scope, n_instruments):
        super().ensure(scope=scope, n_instruments=n_instruments)


class HoldingsData(BaseData):

    def __init__(self, atlas, quiet):
        super().__init__(atlas, atlas.lusid_portfolio_holding_writer, quiet)

    def check_data(self, scope, n_portfolios, n_hld_per_portfolio):
        hld = self.atlas.lusid_portfolio_holding()
        df = hld.select(hld.portfolio_code).where(
            hld.portfolio_scope == scope
        ).group_by(
            hld.portfolio_code
        ).agg(
            Count=hld.portfolio_code.count()
        ).go(quiet=True)

        num_pf_ok = len(df) == n_portfolios
        hld_ok = all(v == n_hld_per_portfolio for v in df['Count'])
        return num_pf_ok and hld_ok

    def assemble_write_data(self, scope, n_portfolios, n_hld_per_portfolio):
        luids = self.luids_table_var(None, n_hld_per_portfolio)

        total = n_hld_per_portfolio * n_portfolios

        t = self.atlas.tools_range(total, 0, 1)

        join = t.left_join(
            luids,
            (t.value % n_hld_per_portfolio) == luids.index
        )

        cols = {
            'WriteAction': 'Set',
            'CostCurrency': 'GBP',
            'EffectiveAt': dt.datetime(2011, 12, 31, 23),
            'HoldingType': 'Position',
            'LusidInstrumentId': luids.lusid_instrument_id,
            'PortfolioCode': 'lumi-test-pf-' + (t.value // n_hld_per_portfolio).cast(str),
            'PortfolioScope': scope,
            'Units': 100,
        }

        return join.select(**cols).to_table_var()

    def ensure(self, scope, n_portfolios, n_hld_per_portfolio):
        super().ensure(scope=scope, n_portfolios=n_portfolios, n_hld_per_portfolio=n_hld_per_portfolio)


class TxnsData(BaseData):

    def __init__(self, atlas, quiet):
        super().__init__(atlas, atlas.lusid_portfolio_txn_writer, quiet)

    def check_data(self, scope, n_portfolios, n_txns_per_portfolio):
        tx = self.atlas.lusid_portfolio_txn()
        df = tx.select(tx.portfolio_code).where(
            tx.portfolio_scope == scope
        ).group_by(
            tx.portfolio_code
        ).agg(
            Count=tx.portfolio_code.count()
        ).go(quiet=True)

        num_pf_ok = len(df) == n_portfolios
        txn_ok = all(v == n_txns_per_portfolio for v in df['Count'])
        return num_pf_ok and txn_ok

    def assemble_write_data(self, scope, n_portfolios, n_txns_per_portfolio):
        luids = self.luids_table_var(None, n_txns_per_portfolio)

        total = n_txns_per_portfolio * n_portfolios

        t = self.atlas.tools_range(total, 0, 1)

        join = t.left_join(
            luids,
            (t.value % n_txns_per_portfolio) == luids.index
        )

        cols = {
            'LusidInstrumentId': luids.lusid_instrument_id,
            'PortfolioCode': 'lumi-test-pf-' + (t.value // n_txns_per_portfolio).cast(str),
            'PortfolioScope': scope,
            'SettlementCurrency': 'GBP',
            'SettlementDate': dt.datetime(2010, 1, 1, 23),
            'Status': 'Active',
            'TransactionDate': dt.datetime(2010, 1, 1, 23),
            'TransactionPrice': 100,
            'TxnId': 'lumi-test-trade-' + (t.value % n_txns_per_portfolio).cast(str),
            'Type': 'Buy',
            'Units': 100,
        }

        return join.select(**cols).to_table_var()

    def ensure(self, scope, n_portfolios, n_txns_per_portfolio):
        super().ensure(scope=scope, n_portfolios=n_portfolios, n_txns_per_portfolio=n_txns_per_portfolio)

