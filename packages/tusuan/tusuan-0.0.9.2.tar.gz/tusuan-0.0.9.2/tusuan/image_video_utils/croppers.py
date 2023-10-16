import numpy


def crop_image(image: numpy.ndarray,
               x1: int, y1: int, x2: int, y2: int,
               h_axis: int = 0, w_axis: int = 1) -> numpy.ndarray:
    """
    可对图像(h w [c])进行截取，返回截取后的数组。
    :param image: numpy.array, 输入图像或视频的帧。
    :param x1: int, 左上角 x 坐标。
    :param y1: int, 左上角 y 坐标。
    :param x2: int, 右下角 x 坐标。
    :param y2: int, 右下角 y 坐标。
    :param h_axis: int, 数组中表示高度（height）的轴。
    :param w_axis: int, 数组中表示宽度（width）的轴。

    :return cropped_image: numpy.array, 截取后的二维或三维数组。
    """
    # 检查 h_axis 和 w_axis 是否超出数组维度
    if h_axis >= image.ndim or w_axis >= image.ndim:
        raise ValueError(f"h_axis:{h_axis} >= ndim:{image.ndim} or w_axis:{w_axis} >= ndim:{image.ndim}")

    # 修正 x1, y1, x2, y2，使得坐标表示从左到右，从上到下
    x1, x2 = sorted([x1, x2])
    y1, y2 = sorted([y1, y2])

    # 创建用于截取数组的切片
    slices = [slice(None, None, None) for _ in range(image.ndim)]
    slices[h_axis] = slice(y1, y2)
    slices[w_axis] = slice(x1, x2)

    # 截取图片
    cropped_image = image[tuple(slices)]

    return cropped_image


def crop_video(video: numpy.ndarray, x1: int, y1: int, x2: int, y2: int, h_axis: int = 1,
               w_axis: int = 2) -> numpy.ndarray:
    """
    对视频(f h w [c])中的每一帧进行截取，返回截取后的视频。
    实际上是将视频看成一个多维图像，直接采用`crop_image`函数对多维图像进行切割。

    :param video: numpy.array, 输入视频。
    :param x1: int, 左上角 x 坐标。
    :param y1: int, 左上角 y 坐标。
    :param x2: int, 右下角 x 坐标。
    :param y2: int, 右下角 y 坐标。
    :param h_axis: int, 数组中表示高度（height）的轴。
    :param w_axis: int, 数组中表示宽度（width）的轴。
    :return cropped_video: numpy.array, 截取后的视频。
    """

    return crop_image(video, x1, y1, x2, y2, h_axis, w_axis)
