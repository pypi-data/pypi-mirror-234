import argparse
import pytest

import src.main.main as main


@pytest.mark.skip
def test_generate_all_test_charts():
    """Generate a complete set of charts from tests/resources/test_data.xlsx"""
    args = argparse.Namespace(input_dir='tests/resources/',
                              ignore_bars=False,
                              ignore_pies=False)

    main.main(args)
