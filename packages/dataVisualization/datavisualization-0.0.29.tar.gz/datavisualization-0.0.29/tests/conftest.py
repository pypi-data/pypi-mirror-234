import pandas as pd
import pytest

from pathlib import Path


_test_file = Path('tests/resources/test_data.xlsx')
_input_dfs: dict[str, pd.DataFrame] = pd.read_excel(_test_file, sheet_name=None)


def pytest_addoption(parser):
    parser.addoption(
        '--quick',
        help='Skip most bars tests to decrease the test suite running time',
        action='store_true')


def _filter_dfs(input_dfs: dict[str,
                        pd.DataFrame]) -> tuple[dict[str, pd.DataFrame], ...]:
    """
    Separate bars and pies DataFrames.
    """
    bars_dfs = {}
    pies_dfs = {}

    for k, v in input_dfs.items():
        if k in ['Format']:
            continue
        # FIXME: rudimentary way to distinguish bars from pies
        if k in input_dfs['Format']['Sheet No.'].map(str).values:
            bars_dfs[k] = v
        else:
            pies_dfs[k] = v
    return bars_dfs, pies_dfs


def pytest_generate_tests(metafunc):
    """
    Hook that checks the fixture names of test functions, distinguishes bars
    tests from pies tests, and parametrizes the tests with the corresponding
    input data (so a bars test will be generated for each input sheet with bars
    data).
    """
    bars_dfs, pies_dfs = _filter_dfs(_input_dfs)
    if metafunc.config.getoption('quick'):
        bars_dfs = {k: v for (k, v) in bars_dfs.items() if 'Social' in str(k)}
    if 'bars_tuple' in metafunc.fixturenames:
        bars_baselines = list(map(lambda k: [str(k) + '.png'],
                                  bars_dfs.keys()))
        metafunc.parametrize(['bars_tuple', 'baseline_images'],
                             list(zip(bars_dfs.items(), bars_baselines)),
                             ids=bars_dfs.keys())
    if 'pies_tuple' in metafunc.fixturenames:
        pies_baselines = list(map(lambda k: [str(k) + '.png'],
                                  pies_dfs.keys()))
        metafunc.parametrize(['pies_tuple', 'baseline_images'],
                             list(zip(pies_dfs.items(), pies_baselines)),
                             ids=pies_dfs.keys())


@pytest.fixture
def format_dataframe():
    """
    This fixture makes the format sheet dataframe available to each test case.
    """
    format_df: pd.DataFrame = _input_dfs['Format'].set_index('Sheet No.')
    format_df.index = format_df.index.map(str)
    return format_df
