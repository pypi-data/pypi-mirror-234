from typing import List

import matplotlib.pyplot as plt
import numpy
from fastcore.basics import flatten
from matplotlib.axes import Axes
from matplotlib.figure import Figure


def show_multi_images_in_matplotlib(images: List[numpy.array], subtitles=None, col_num=3, title=None, show=False):
    col_num = min(len(images), col_num)
    images_count = len(images)

    if not subtitles:
        subtitles = [None] * images_count

    if images_count > len(subtitles):
        subtitles.extend([None] * (images_count - len(subtitles)))

    subtitles = subtitles[:images_count]

    row_num = -(-images_count // col_num)  # -a//b表示将a除以b并向下取整，最后将结果取反，即可得到向上取整的效果
    fig, axs = plt.subplots(nrows=row_num, ncols=col_num, squeeze=False)  # type: Figure, Axes
    fig.suptitle(title)
    fig.set_size_inches(4 * col_num, 3.5 * row_num)

    axs_list = list(flatten(axs))
    for ax, img, subtitle in zip(axs_list[:images_count], images, subtitles):  # type: Axes
        ax.set_title(subtitle)
        ax.imshow(img)

    for ax in axs_list[images_count:]:
        ax.axis('off')

    fig.tight_layout()

    if show:
        plt.show()

    return fig
