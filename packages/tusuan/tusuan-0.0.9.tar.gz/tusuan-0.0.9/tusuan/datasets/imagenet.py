import glob
import pickle
from builtins import ValueError
from functools import lru_cache
from os.path import join
from typing import Tuple

import einops
import numpy
from torch.utils.data import dataset


def unpickle(file):
    with open(file, 'rb') as fo:
        obj = pickle.load(fo)
    return obj


def load_databatch(data_file, img_size=64):
    # data_file = os.path.join(data_folder, f'train_data_batch_{str(idn)}')
    d = unpickle(data_file)
    x = numpy.array(d['data'], dtype="float32")
    y = numpy.array(d['labels'], dtype="int32")
    # mean = numpy.array(d['mean'])

    # Labels are indexed from 1, shift it so that indexes start at 0
    y = y - 1

    x = einops.rearrange(x, "b (c h w) -> b c h w", h=img_size, w=img_size)
    # mean = einops.rearrange(mean, "(c h w) -> h w c", h=img_size, w=img_size)

    return dict(x=x, y=y)


class ImageNet64(dataset.Dataset):
    BLOCK_CACHE_SIZE = 2
    DATA_CACHE_SIZE = 100_000

    def __init__(self, root, train=True):
        """
        ImageNet64 的数据集，用于加载 64x64 像素的图像数据集。
        数据集被分成了 10 个文件（train_data_batch_1 至 train_data_batch_10），
        其中每个文件包含了相同数量的图像数据（128,116 或 128,123 张）。
        每个批次都保存在 pickle 文件中。该数据集支持使用索引直接访问单个图像和标签，
        并且使用缓存来尽可能快地访问已加载的数据块。
        :param root: train_data_batch_* 文件的父文件夹
        """
        super().__init__()
        self.root = root

        if train:
            if len(glob.glob(join(root, "train_data_batch_*"))) != 10:
                raise FileNotFoundError(f"train_data_batch "
                                        f"file count {len(glob.glob(join(root, 'train_data_batch_*')))} "
                                        f"is not equals to 10.")

            each_block_length = [128116, 128116, 128116, 128116, 128116,
                                 128116, 128116, 128116, 128116, 128123]

            # self.index_block_map = \
            #     [(i, (sum(each_block_length[:i - 1]), sum(each_block_length[:i]))) for i in range(1, 11)]
            self.index_block_map = \
                [(1, (0, 128116)), (2, (128116, 256232)), (3, (256232, 384348)), (4, (384348, 512464)),
                 (5, (512464, 640580)), (6, (640580, 768696)), (7, (768696, 896812)), (8, (896812, 1024928)),
                 (9, (1024928, 1153044)), (10, (1153044, 1281167))]

            # print(self.index_block_map)
            self.data_length = sum(each_block_length)

            self.get_data = self.get_data_train
        else:
            if len(glob.glob(join(root, "val_data"))) != 1:
                raise FileNotFoundError(f"val_data file not exists.")
            self.data_list = load_databatch(join(root, "val_data"))
            self.data_length = len(self.data_list["y"])

            self.get_data = self.get_data_val

    @lru_cache(BLOCK_CACHE_SIZE)
    def get_data_block(self, block_idn):
        # print(block_idn)
        return load_databatch(data_file=join(self.root, f'train_data_batch_{str(block_idn)}'))

    @lru_cache(DATA_CACHE_SIZE)
    def get_data_train(self, index):
        if index >= self.data_length or index < 0:
            raise IndexError(f"index {index} out of bounds for size [0, {self.data_length})")

        count_previous_blocks_length = 0
        for map_block_idn, map_interval in self.index_block_map:
            # print(map_block_idn)
            if map_interval[0] <= index < map_interval[1]:
                block_idn = map_block_idn
                break
            else:
                count_previous_blocks_length = map_interval[1]
        else:
            raise ValueError(f"没有找到{index}")

        data_block = self.get_data_block(block_idn)
        # print(block_idn, index - count_previous_blocks_length)
        return data_block["x"][index - count_previous_blocks_length], \
            data_block["y"][index - count_previous_blocks_length]

    def get_data_val(self, index):
        return self.data_list["x"][index], self.data_list["y"][index]

    def __getitem__(self, index) -> Tuple[numpy.ndarray, int]:
        return self.get_data(index)

    def __len__(self):
        return self.data_length
