from matplotlib import style
from matplotlib.testing.decorators import cleanup, image_comparison
from pandas import DataFrame

from src.main.bars import stacked_bar


@cleanup(style=['classic', '_classic_test_patch'])
@image_comparison(baseline_images=None,
                  extensions=['png'],
                  savefig_kwarg={'bbox_inches': 'tight', 'dpi': 300},)
def test_stacked_bar(bars_tuple: tuple[str, DataFrame],
                     format_dataframe: DataFrame,
                     baseline_images: list[str]) -> None:
    """
    Generate and test a stacked bar.

    The image_comparison decorator will call savefig() and compare against a
    baseline image. Setting the baseline_images argument to None causes the
    comparison to be made aginst a list of files (in our case a singleton list)
    to compare against.

    The bars_tuple and baseline_images arguments are parametrized in test
    generation, so individual tests will be generated and excecuted, with
    different values for these parameters, for each sheet in the test data.
    """
    style.use('default')
    format_series = format_dataframe.loc[bars_tuple[0]]
    stacked_bar(bars_tuple[1], format_series)
