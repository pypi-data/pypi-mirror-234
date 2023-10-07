from typing import List

from pathlib import Path
import joblib
import numpy as np
import xarray as xr
from evotrain.geotiff import load_features_geotiff


def _v1_band_to_v2_band(band: str):
    if '0m' in band:
        band = band.replace('-10m', '')
        band = band.replace('-20m', '')

        if band.startswith('B') or band.startswith('ndvi'):
            band = 's2-' + band
        elif band.startswith('V') or band.startswith('vh'):
            band = 's1-' + band
        elif band.startswith('DEM'):
            band = 'cop-' + band

    return band


def _v1_jlib_to_xarray(fn, v2_names=True):
    # Load data
    arr, bands, attr = joblib.load(fn)
    if v2_names:
        bands = [_v1_band_to_v2_band(b) for b in bands]

    # Derive pixel dimensions
    x_pixel_size = (attr['bounds'][2] - attr['bounds'][0]) / arr.shape[2]
    y_pixel_size = (attr['bounds'][3] - attr['bounds'][1]) / arr.shape[1]

    # Compute coordinates, shifting by half a pixel to get the center coords
    x_coords = np.arange(attr['bounds'][0] +
                         x_pixel_size/2, attr['bounds'][2], x_pixel_size)
    y_coords = np.arange(attr['bounds'][3] -
                         y_pixel_size/2, attr['bounds'][1], -y_pixel_size)

    # Create the DataArray
    data_array = xr.DataArray(
        arr,
        coords={
            'band': bands,
            'y': y_coords,
            'x': x_coords
        },
        dims=['band', 'y', 'x']
    )

    data_array.attrs = attr

    return data_array


def slash_tile(tile: str):

    if len(tile) != 5:
        raise ValueError(f"tile should be a str of len 5, not {tile}")

    return f"{tile[:2]}/{tile[2]}/{tile[3:]}"


class BaseReader:

    def __init__(self, root_path) -> None:
        self._root_path = root_path

    def _patch_path(self, location_id: str, year: int) -> Path:
        tile = location_id.split('_')[0]
        basename = self._patch_basename(location_id, year)
        return (self._root_path / 'features' / f'{year}' /
                slash_tile(tile) / basename)


class ReaderV1(BaseReader):

    def _patch_basename(self, location_id: str, year=None) -> str:
        return f"evoland_v1_{location_id}.jlib"

    def read(self, location_id: str,
             bands: List = None, v2_band_names=True) -> xr.DataArray:
        year = 2021
        path = self._patch_path(location_id, year)
        da = _v1_jlib_to_xarray(path, v2_names=v2_band_names)
        if bands is not None:
            da = da.sel(band=bands)
        return da


class ReaderV2(BaseReader):

    def _patch_basename(self, location_id: str, year: int, bands: List) -> str:
        return f"evotrain_v2_{year}_{location_id}.tif"

    def read(self, location_id: str, year: int,
             bands: List = None, **kwargs) -> xr.DataArray:
        path = self._patch_path(location_id, year)
        da = load_features_geotiff(path, bands)
        if bands is not None:
            da = da.sel(band=bands)
        return da


class ReaderV2TS(BaseReader):

    def _patch_basename(self, location_id: str, year: int) -> str:
        return f"evotrain_v2_{year}_{location_id}.tif"

    def read(self, location_id: str, year: int,
             bands: List = None, **kwargs) -> xr.DataArray:
        path = self._patch_path(location_id, year)
        with xr.open_dataarray(path, **kwargs) as da:
            if bands is not None:
                da = da.sel(band=bands)
            return da.load()
