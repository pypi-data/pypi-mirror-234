import datetime as dt
from typing import Optional, Dict, Union

from pandas import DataFrame

from lumipy.provider.base_provider import BaseProvider
from lumipy.provider.metadata import ColumnMeta, ParamMeta, TableParam
from lumipy.lumiflex import DType


class CreatePortfolioTestData(BaseProvider):

    """Create portfolio test data

    """

    def __init__(self):

        columns = [
            ColumnMeta('PortfolioScope', DType.Text),
            ColumnMeta('BaseCurrency', DType.Text),
            ColumnMeta('PortfolioCode', DType.Text),
            ColumnMeta('PortfolioType', DType.Text),
            ColumnMeta('DisplayName', DType.Text),
            ColumnMeta('Description', DType.Text),
            ColumnMeta('Created', DType.DateTime),
            ColumnMeta('SubHoldingKeys', DType.Text),
        ]

        params = [
            ParamMeta('Scope', DType.Text, is_required=True),
        ]

        super().__init__(
            'Lab.TestData.Lusid.Portfolio',
            columns,
            params,
            description=self.__doc__
        )

    def get_data(
            self,
            data_filter: Optional[Dict[str, object]],
            limit: Union[int, None],
            **params
    ) -> DataFrame:

        if limit is None:
            raise ValueError("You must apply a limit to this table.")

        return DataFrame(
            {
                'PortfolioScope': params['Scope'],
                'BaseCurrency': 'GBP',
                'PortfolioCode': f'lumi-test-pf-{i}',
                'PortfolioType': 'Transaction',
                'DisplayName': f'lumi-test-pf-{i}',
                'Description': f'perf test portfolio',
                'Created': dt.datetime(2010, 1, 1),
                'SubHoldingKeys': '',
            }
            for i in range(limit)
        )


class CreateInstrumentTestData(BaseProvider):

    def __init__(self):

        columns = [
            ColumnMeta('DisplayName', DType.Text),
            ColumnMeta('ClientInternal', DType.Text),
            ColumnMeta('DomCcy', DType.Text),
        ]
        super().__init__(
            'Lab.TestData.Lusid.Instrument',
            columns,
            description=self.__doc__
        )

    def get_data(
            self,
            data_filter: Optional[Dict[str, object]],
            limit: Union[int, None],
            **params
    ) -> DataFrame:

        if limit is None:
            raise ValueError("You must apply a limit to this table.")

        return DataFrame(
            {
                'DisplayName': f'Test Instrument {i}',
                'ClientInternal': f'lumi-test-instrument-{i}',
                'DomCcy': 'USD',
            }
            for i in range(limit)
        )


class CreateTransactionTestData(BaseProvider):

    def __init__(self):

        columns = [
            ColumnMeta('PortfolioScope', DType.Text),
            ColumnMeta('PortfolioCode', DType.Text),
            ColumnMeta('TxnId', DType.Text),
            ColumnMeta('LusidInstrumentId', DType.Text),
            ColumnMeta('Type', DType.Text),
            ColumnMeta('Status', DType.Text),
            ColumnMeta('SettlementDate', DType.DateTime),
            ColumnMeta('TransactionDate', DType.DateTime),
            ColumnMeta('Units', DType.Int),
            ColumnMeta('SettlementCurrency', DType.Text),
            ColumnMeta('TransactionPrice', DType.Int),
        ]

        params = [
            ParamMeta('Scope', DType.Text, is_required=True),
            ParamMeta('NumPortfolios', DType.Int, is_required=True),
            ParamMeta('InstrumentsPerPortfolio', DType.Int, is_required=True),
            ParamMeta('TxnsPerInstrument', DType.Int, is_required=True),
        ]

        table_params = [TableParam("Luids")]

        super().__init__(
            'Lab.TestData.Lusid.Transaction',
            columns=columns,
            parameters=params,
            table_parameters=table_params,
        )

    def get_data(
            self,
            data_filter: Optional[Dict[str, object]],
            limit: Union[int, None],
            **params
    ) -> DataFrame:

        scope = params.get('Scope')
        n_pf = params.get('NumPortfolios')
        n_inst = params.get('InstrumentsPerPortfolio')
        n_txn_per_inst = params.get('TxnsPerInstrument')

        luids = params.get('Luids').LusidInstrumentId.tolist()

        def make_rows():
            for pf_i in range(n_pf):
                count = 0
                for in_i in range(n_inst):
                    for tx_i in range(n_txn_per_inst):
                        yield {
                            'PortfolioScope': scope,
                            'PortfolioCode': f'lumi-test-pf-{pf_i}',
                            'TxnId': f'lumi-test-trade-{count}',
                            'LusidInstrumentId': luids[in_i],
                            'Type': 'Buy',
                            'Status': 'Active',
                            'SettlementDate': dt.datetime(2010, 1, 2) + dt.timedelta(hours=tx_i),
                            'TransactionDate': dt.datetime(2010, 1, 2) + dt.timedelta(hours=tx_i),
                            'Units': 100 * (1 + tx_i % 10),
                            'SettlementCurrency': 'GBP',
                            'TransactionPrice': 100,
                        }
                        count += 1

        return DataFrame(make_rows())


class CreateHoldingTestData(BaseProvider):

    def __init__(self):

        columns = [
            ColumnMeta('PortfolioScope', DType.Text),
            ColumnMeta('PortfolioCode', DType.Text),
            ColumnMeta('LusidInstrumentId', DType.Text),
            ColumnMeta('HoldingType', DType.Text),
            ColumnMeta('Units', DType.Int),
            ColumnMeta('EffectiveAt', DType.DateTime),
            ColumnMeta('CostCurrency', DType.Text),
        ]
        params = [
            ParamMeta('Scope', DType.Text, is_required=True),
            ParamMeta('NumPortfolios', DType.Int, is_required=True),
            ParamMeta('InstrumentsPerPortfolio', DType.Int, is_required=True),
            ParamMeta('EffectiveAtsPerInstrument', DType.Int, is_required=True)
        ]
        table_params = [TableParam("Luids")]

        super().__init__(
            'Lab.TestData.Lusid.Holding',
            columns=columns,
            parameters=params,
            table_parameters=table_params,
        )

    def get_data(
            self,
            data_filter: Optional[Dict[str, object]],
            limit: Union[int, None],
            **params
    ) -> DataFrame:

        scope = params.get('Scope')
        luids = params.get('Luids').LusidInstrumentId.tolist()
        n_pf = params.get('NumPortfolios')
        n_inst = params.get('InstrumentsPerPortfolio')
        n_eff_at_per_inst = params.get('EffectiveAtsPerInstrument')

        def make_rows():
            for pf_i in range(n_pf):
                for in_i in range(n_inst):
                    for ea_i in range(n_eff_at_per_inst):
                        yield {
                            'PortfolioScope': scope,
                            'PortfolioCode': f'lumi-test-pf-{pf_i}',
                            'LusidInstrumentId': luids[in_i],
                            'HoldingType': 'Position',
                            'Units': 100 * (1 + ea_i % 10),
                            'EffectiveAt': dt.datetime(2010, 1, 1) + dt.timedelta(hours=ea_i),
                            'CostCurrency': 'GBP',
                        }

        return DataFrame(make_rows())
