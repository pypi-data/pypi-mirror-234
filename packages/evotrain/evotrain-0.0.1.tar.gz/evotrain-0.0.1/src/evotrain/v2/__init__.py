import random
from pathlib import Path
from importlib.resources import files

import pandas as pd
from evotrain.reader import ReaderV2


_ROOT_PATH = Path("/vitodata/vegteam/projects/evoland/training/evotrain_v2/")

_SUPPORTED_DATA = ('locs', 'hists', 'norm', 'size')

_data_paths = {k: files("evotrain.v2.data.statistics").joinpath(
    f"evotrain_v2_{k}.parquet") for k in ('hists', 'norm', 'size')}
_data_paths['locs'] = files("evotrain.v2.data").joinpath(
    "locations.parquet")


def _load(key: str, columns=None):
    """_summary_

    Args:
        key (str): one of 'locs', 'hists', 'norm', 'size'
    """
    if key not in _SUPPORTED_DATA:
        raise ValueError(f"Unrecognized metadata table key {key}. "
                         f"Should be one of {_SUPPORTED_DATA}")

    return pd.read_parquet(_data_paths[key], columns=columns)


class _Stats:

    def __init__(self) -> None:
        self._hists = None
        self._norm = None
        self._locs = None
        self._bands = None
        self._location_ids = None
        self.years = (2018, 2019, 2020, 2021, 2022)

    @property
    def hists(self):
        if self._hists is not None:
            self._hists = _load('hists')
        return self._hists

    @property
    def norm(self):
        if self._norm is None:
            self._norm = _load('norm')
        return self._norm

    @property
    def locs(self):
        if self._locs is None:
            self._locs = _load('locs')
        return self._locs

    @property
    def location_ids(self):
        if self._location_ids is None:
            self._location_ids = _load('locs', columns=['location_id'])[
                'location_id'].astype("string[pyarrow]")
        return self._location_ids

    def location_ids_shuffled(self, n=None, fraction=1, random_state=0):
        loc_ids = self.location_ids.sample(n=n,
                                           frac=fraction,
                                           random_state=random_state)

        return loc_ids

    @property
    def bands(self):
        if self._bands is None:
            self._bands = list(self.norm.columns)
        return self._bands

    def band_stats(self, band: str, stats_index: str):
        """Return stats value for band.

        Args:
            stats_index (str): stats should be a str among
            {self.norm.index.values.tolist()}

            band (str): stat should be a str among
            {self.norm.columns.values.tolist()}

        Returns:
            float: value of the request statistic
        """
        return self.norm.loc[stats_index, band]

    @staticmethod
    def reader(root_path: str):
        return ReaderV2(root_path)

    def patch_ids(self, location_ids=None, years=None,
                  fraction=1, shuffle_random_state=None):

        if location_ids is None:
            location_ids = self.location_ids

        if years is None:
            years = self.years

        patch_ids = [(loc_id, year)
                     for loc_id in location_ids
                     for year in years]

        if shuffle_random_state is not None:
            random.seed(shuffle_random_state)
            random.shuffle(patch_ids)

        # Select a fraction of the list
        num_elements = int(fraction * len(patch_ids))
        patch_ids_fraction = patch_ids[:num_elements]

        return patch_ids_fraction


dataset_metadata = _Stats()
