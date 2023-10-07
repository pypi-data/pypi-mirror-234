from unittest.mock import patch

import pytest
import pandas as pd
from pandas.testing import assert_frame_equal

from evotrain.v2 import load, _data_paths

def test_load_valid_key():
    # Assuming that one of the keys is 'hists' and the corresponding
    # Parquet file contains a DataFrame with some known content.
    expected_df = pd.DataFrame({"column1": [1, 2, 3], "column2": [4, 5, 6]})
    with patch("pandas.read_parquet", return_value=expected_df):
        result_df = load("hists")
        assert_frame_equal(result_df, expected_df)

def test_load_invalid_key():
    with pytest.raises(ValueError, match=r"Unrecognized metadata table key invalid_key. Should be one of \('locs', 'hists', 'norm', 'size'\)"):
        load("invalid_key")

def test_file_exists():
    for key, path in _data_paths.items():
        assert path.exists(), f"File for key {key} does not exist at {path}"