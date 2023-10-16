from typing import Optional, List

import cv2
import imagesize
import numpy


def get_image_size(image_path):
    """
    :param image_path: 图像路径
    :return: height, width
    """

    width, height = imagesize.get(image_path)

    if (height, width) == (-1, -1):
        image: numpy.ndarray = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        # 获取图像尺寸
        height, width = image.shape

    return height, width


def read_image(image_path, grey: bool = False, resize=None, rgb_mode: bool = True):
    """
    读取图像函数

    :param image_path: 图像路径
    :param grey: 是否将图像转换为灰度图像，默认为False
    :param resize: (h, w)，默认为None
    :param rgb_mode: 使用opencv读出的图像是BGR格式，是否将图像转换为RGB格式，默认为True
    :return: 读取到的图像数组
    """

    if grey:
        # 读取灰度图像
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    else:
        # 读取彩色图像
        image = cv2.imread(image_path)
        if rgb_mode:
            # 将BGR格式转换为RGB格式
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    if resize:
        image = cv2.resize(image, resize)

    return image


def read_images(image_paths: List[str], grey: bool = False, resize=None, rgb_mode: bool = True):
    image_list = []
    for image_path in image_paths:
        image = read_image(image_path, grey, resize, rgb_mode)
        image_list.append(image)

    return numpy.stack(image_list, axis=0)


def get_video_info(video_path):
    """
    获取帧速率、帧数、宽度和高度
    :param video_path: 视频文件地址
    :return: 帧数、宽度、高度和帧速率。如果视频文件无法打开，则返回None。
    """

    # 打开视频文件
    cap = cv2.VideoCapture(video_path)

    # 检查视频文件是否成功打开
    if not cap.isOpened():
        return None

    # 获取帧速率、帧数、宽度和高度
    frames_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))

    # 释放VideoCapture对象
    cap.release()

    # 返回帧数、宽度、高度和帧速率
    return frames_count, fps, height, width


def read_video(video_path, *,
               specific_frame: Optional[List[int]] = None,
               start: int = 0, stop: int = -1, step: int = 1,
               resize=None,
               rgb_mode=True):
    """
    这个函数可以读取视频文件，并返回指定范围内的帧。

    :param video_path: 视频文件路径
    :param specific_frame: 指定特定帧
    :param start: 要读取的起始帧索引，负数代表倒数（默认为 0）
    :param stop: 要读取的结束帧索引，负数代表倒数（默认为 -1，即读取到最后一帧）
    :param step: 读取帧的步长（默认为 1）
    :param resize: (h, w)，默认为None
    :param rgb_mode: 是否转化为RGB图像（默认为 True）
    :return: 读取成功返回一个代表对应帧所组成的numpy数组(h w c)，读取失败返回None
    """
    if specific_frame:
        print("Because the specific_frame has been specified, parameters start, stop and step are ignored.")

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        return None

    # 结束帧数不应超过总帧数
    frames_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    video = []
    if specific_frame:
        specific_frame = sorted(specific_frame)
        specific_frame.insert(0, 0)
        # for i in range(specific_frame[0]):
        #     print("ignore", i)
        #     cap.grab()

        for j in range(1, len(specific_frame)):
            for i in range(specific_frame[j] - specific_frame[j - 1]):
                ret = cap.grab()
            else:
                ret, frame = cap.read()
                if ret:
                    if rgb_mode:
                        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    if resize:
                        frame = cv2.resize(frame, resize)
                    video.append(frame)

            if not ret:
                break

    else:
        start = start % frames_count
        stop = stop % frames_count

        reverse_flag = False
        if start > stop:
            start, stop = sorted([start, stop])
            reverse_flag = not reverse_flag

        if step < 0:
            step = abs(step)
            reverse_flag = not reverse_flag

        print(start, stop, step, reverse_flag)
        # 按给定的范围读取视频帧
        for i in range(start):
            cap.grab()

        for i in range(stop - start + 1):
            # 只选取其中符合特定步长的帧
            if i % step == 0:
                ret, frame = cap.read()
                if ret:
                    if rgb_mode:
                        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    if resize:
                        frame = cv2.resize(frame, resize)
                    video.append(frame)
            else:
                ret = cap.grab()

            if not ret:
                break

        if reverse_flag:
            video = video[::-1]

    cap.release()

    return numpy.stack(video, axis=0)
