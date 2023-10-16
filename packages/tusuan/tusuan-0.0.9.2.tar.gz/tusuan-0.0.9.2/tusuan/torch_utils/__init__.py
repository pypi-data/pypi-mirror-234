import os
import random

import numpy
import torch
from torch.utils.data import Dataset


class ListDataset(Dataset):
    def __init__(self, data_list):
        self.data_list = data_list

    def __len__(self):
        return len(self.data_list)

    def __getitem__(self, index):
        return self.data_list[index]


def print_support_devices():
    result = dict()
    for has_x in filter(lambda x: str.startswith(x, "has_"), dir(torch)):
        method = getattr(torch, has_x)
        print(has_x, method)
        result[has_x[4:]] = method


def seed_everything(seed=42):
    random.seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)
    numpy.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
