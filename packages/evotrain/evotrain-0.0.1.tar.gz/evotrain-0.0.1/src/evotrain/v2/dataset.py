import random
import joblib
import numpy as np
import torch
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms

from evotrain.v2 import dataset_metadata
from evotrain.reader import ReaderV2


_CLASSES = [10, 20, 30, 40, 50, 60, 70, 80, 90, 95, 100]


def _transforms(augment=True):
    if augment:
        im_transforms = transforms.Compose([transforms.ToTensor(),
                                            transforms.RandomHorizontalFlip(
                                                0.5),
                                            transforms.RandomVerticalFlip(0.5)
                                            ])
    else:
        im_transforms = transforms.Compose([transforms.ToTensor(),])
    return im_transforms


class EvoTrainV1(Dataset):
    _dataset = "evotrain_v1"

    def __init__(
        self,
        image_paths,
        transforms,
        bands,
    ):
        self.image_paths = image_paths
        self.transforms = transforms
        self._mean = NORM_DICT[self._dataset]
        self._sd = NORM_DICT[self._dataset]
        self._bands = bands

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        image_path = self.image_paths[idx]

        image = np.squeeze(np.array([
            self._load_band(image_path, band)
            for band in self._bands
        ]))

        image = np.swapaxes(image, 0, 2).swapaxes(0, 1)
        assert not np.any(np.isnan(image))

        woco_im = np.squeeze(self.get_s2_band(image_path, 'worldcover_2021'))
        label = np.zeros(
            (len(self._classes), woco_im.shape[0], woco_im.shape[1]),
            dtype=np.float32
        )
        for ind, lab in enumerate(self._mapped_labels):
            label[ind, :, :] = (woco_im == lab)
        label = np.squeeze(label)
        if len(label.shape) == 3:
            label = np.swapaxes(label, 0, 2).swapaxes(0, 1)
            label = label.astype('int')

        assert not np.any(np.isnan(label))

        seed = np.random.randint(2147483647)
        if self.transforms is not None:
            random.seed(seed)
            torch.manual_seed(seed)
            image = self.transforms(image)
            random.seed(seed)
            torch.manual_seed(seed)
            label = self.transforms(label)

        return image, label

    def get_s2_band(self, path, band_name):
        arr, s2_band_names, _ = joblib.load(path)
        index = s2_band_names.index(band_name)
        data = np.squeeze(arr[index, :, :])
        data = data[np.newaxis, ...]
        return data

    def _load_band(self, data_array, band_name):
        x = self.get_s2_band(data_array, band_name)
        x = _sd_scaling(x, band_name, self._mean, self._sd)
        return x


class EvoTrainV2(Dataset):

    def __init__(
            self,
            root_path,
            patch_ids=None,
            data_augmentation=True,
            bands=None,
            scaling_quantiles=('0.01', '0.99')):

        self._root_path = root_path

        self._ids = (patch_ids if patch_ids is not None
                     else dataset_metadata.patch_ids())

        self._transforms = _transforms(data_augmentation)
        self._bands = bands if bands is not None else dataset_metadata.bands

        self.reader = ReaderV2(root_path)

        qmin, qmax = scaling_quantiles
        self._bands_qmin = np.array([dataset_metadata.band_stats(b, qmin)
                                     for b in self._bands])
        self._bands_qmax = np.array([dataset_metadata.band_stats(b, qmax)
                                     for b in self._bands])

    def __len__(self):
        return len(self._ids)

    def __getitem__(self, idx):

        location_id, year = self._ids[idx]
        darr = self.reader.read(location_id, year, self._bands)
        return darr

        # image = np.squeeze(np.array([
        #     self._load_band(image_path, band)
        #     for band in self._bands
        # ]))

        # image = np.swapaxes(image, 0, 2).swapaxes(0, 1)
        # assert not np.any(np.isnan(image))

        # woco_im = np.squeeze(self.get_s2_band(image_path, 'worldcover_2021'))
        # label = np.zeros(
        #     (len(self._mapped_labels), woco_im.shape[0], woco_im.shape[1]),
        #     dtype=np.float32
        # )
        # for ind, lab in enumerate(self._mapped_labels):
        #     label[ind, :, :] = (woco_im == lab)
        # label = np.squeeze(label)
        # if len(label.shape) == 3:
        #     label = np.swapaxes(label, 0, 2).swapaxes(0, 1)
        #     label = label.astype('int')

        # assert not np.any(np.isnan(label))

        # seed = np.random.randint(2147483647)
        # if self.transforms is not None:
        #     random.seed(seed)
        #     torch.manual_seed(seed)
        #     image = self.transforms(image)
        #     random.seed(seed)
        #     torch.manual_seed(seed)
        #     label = self.transforms(label)

        # return image, label

    def get_s2_band(self, path, band_name):
        arr, s2_band_names, _ = joblib.load(path)
        index = s2_band_names.index(band_name)
        data = np.squeeze(arr[index, :, :])
        data = data[np.newaxis, ...]
        return data

    def _load_band(self, data_array, band_name):
        x = self.get_s2_band(data_array, band_name)
        if self._scaling == 'power':
            x = _power_scaling(x, band_name)
        elif self._scaling == 'linear':
            x = _linear_scaling(x, band_name)
        else:
            x = _sd_scaling(x, band_name, S2_MEAN, S2_SD)
        return x


def _linear_scaling(x, band_name, _sensor_scaling, _range_dict, _clamp=True):

    if _sensor_scaling:
        x = x / _sensor_scaling

    vmin, vmax = _range_dict[band_name]

    if _clamp:
        x[x < vmin] = vmin
        x[x > vmax] = vmax

    x = (x - vmin) / (vmax - vmin)

    return x


def _power_scaling(x, band_name, _scalers):

    x = x / 10000.  # must be divided by 10000
    shape = x.shape
    x_scaled = (_scalers[band_name]
                .transform(x.flatten().reshape(-1, 1))
                .reshape(shape))

    return x_scaled


def _sd_scaling(x, band_name, _mean_dict, _sd_dict):
    bmean = _mean_dict[band_name]
    bsd = _sd_dict[band_name]

    x = (x - bmean)/bsd

    return x


def get_vi_band(ts, band_name, timestamp):
    dat = np.squeeze(ts[band_name].select_timestamps(timestamp).data)
    dat = dat[np.newaxis, ...]
    return dat
