from pathlib import Path
from unittest.mock import patch

import numpy as np
import pytest
import xarray as xr

from evotrain.reader import (_v1_jlib_to_xarray, slash_tile,
                             ReaderV1, ReaderV2, _v1_band_to_v2_band)


def test_v1_jlib_to_xarray():
    mock_array = np.array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])
    mock_bands = ['band1', 'band2']
    mock_attrs = {'bounds': [0, 0, 2, 2]}

    with patch('joblib.load', return_value=(mock_array, mock_bands, mock_attrs)):
        result = _v1_jlib_to_xarray('dummy_path')

    expected_data = xr.DataArray(
        mock_array,
        coords={
            'band': mock_bands,
            'y': [1.5, 0.5],
            'x': [0.5, 1.5]
        },
        dims=['band', 'y', 'x']
    )

    assert result.equals(expected_data)


def test_slash_tile():
    assert slash_tile("12345") == "12/3/45"

    with pytest.raises(ValueError, match=r"tile should be a str of len 5, not 1234"):
        slash_tile("1234")


def test_v1_band_to_v2_band():
    bands_v1 = {
        'B02-p50-10m': 's2-B02-p50',
        'B03-p50-10m': 's2-B03-p50',
        'B04-p50-10m': 's2-B04-p50',
        'B08-p50-10m': 's2-B08-p50',
        'B11-p50-20m': 's2-B11-p50',
        'B12-p50-20m': 's2-B12-p50',
        'ndvi-p10-10m': 's2-ndvi-p10',
        'ndvi-p50-10m': 's2-ndvi-p50',
        'ndvi-p90-10m': 's2-ndvi-p90',
        'VH-p10-20m': 's1-VH-p10',
        'VH-p50-20m': 's1-VH-p50',
        'VV-p50-20m': 's1-VV-p50',
        'vh_vv-p50-20m': 's1-vh_vv-p50',
        'DEM-alt-20m': 'cop-DEM-alt',
        'lat': 'lat',
        'lon': 'lon',
    }

    for band_v1, expected_band_v2 in bands_v1.items():
        result_band_v2 = _v1_band_to_v2_band(band_v1)
        assert result_band_v2 == expected_band_v2, f"For band {band_v1}, expected {expected_band_v2} but got {result_band_v2}"


def test_reader_v1_read():
    mock_root_path = Path("/mock/root/path")
    reader_v1 = ReaderV1(mock_root_path)

    mock_data_array = xr.DataArray(np.array([[[1, 2], [3, 4]]]))

    with patch.object(reader_v1, '_patch_path', return_value=mock_root_path / "mock_path.jlib") as mock_patch_path, \
            patch("evotrain.reader._v1_jlib_to_xarray", return_value=mock_data_array) as mock_v1_jlib_to_xarray:

        result = reader_v1.read("12345_location")

    mock_patch_path.assert_called_once_with("12345_location", 2021)
    mock_v1_jlib_to_xarray.assert_called_once_with(
        mock_root_path / "mock_path.jlib")
    assert result.equals(mock_data_array)


def test_reader_v2_read():
    mock_root_path = Path("/mock/root/path")
    reader_v2 = ReaderV2(mock_root_path)

    mock_data_array = xr.DataArray(np.array([[[1, 2], [3, 4]]]))

    with patch.object(reader_v2, '_patch_path', return_value=mock_root_path / "mock_path.tif") as mock_patch_path, \
            patch("xarray.open_dataarray", return_value=mock_data_array) as mock_open_dataarray:

        result = reader_v2.read("12345_location", 2022)

    mock_patch_path.assert_called_once_with("12345_location", 2022)
    mock_open_dataarray.assert_called_once_with(
        mock_root_path / "mock_path.tif")
    assert result.equals(mock_data_array)
