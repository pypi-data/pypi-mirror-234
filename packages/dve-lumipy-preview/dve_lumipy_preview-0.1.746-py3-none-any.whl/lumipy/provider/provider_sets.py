from lumipy.provider.common import available
from lumipy.provider.implementation.lusid_test_data import *
from lumipy.test.provider.int_test_providers import *


def demo_set():
    csvs = ['iris', 'mpg', 'penguins', 'planets', 'taxis', 'tips', 'titanic']
    base_path = 'https://raw.githubusercontent.com/mwaskom/seaborn-data/master'
    return [lp.PandasProvider(f'{base_path}/{n}.csv', n, 'demo') for n in csvs]


def int_test():
    return [
        ParameterAndLimitTestProvider(), IntSerialisationBugProvider(), TableParameterTestProvider(),
        PandasFilteringTestProvider(1989), FilteringTestProvider(), ColumnValidationTestProvider(),
        TaskCancelledTestProvider(), TestLogAndErrorLines(), NothingProvider(),
        UnicodeProvider(1989),
    ]


def lusid_data_gen():
    return [CreateInstrumentTestData(), CreatePortfolioTestData(), CreateHoldingTestData(), CreateTransactionTestData()]


def world_bank():
    return [lp.WorldBankDataSources(), lp.WorldBankEconomies(), lp.WorldBankSeriesMetadata(), lp.WorldBankSeriesData()]


def yfinance():
    return [lp.YFinanceProvider()]


def portfolio_opt():
    return [lp.YFinanceProvider(), lp.QuadraticProgram()]


provider_sets = {'int_test': int_test(), 'lusid_data_gen': lusid_data_gen(), 'demo': demo_set()}

if available('yfinance'):
    provider_sets['yfinance'] = yfinance()

if available('cvxopt', 'yfinance'):
    provider_sets['portfolio_opt'] = portfolio_opt()

if available('wbgapi'):
    provider_sets['world_bank'] = world_bank()
