import cv2
import numpy


def select_image_range(image):
    # 定义变量和鼠标回调函数
    ix, iy = -1, -1
    on_drawing = False
    roi = None

    # 创建临时图像并复制原图
    temp_image = image.copy()
    winname = 'image'

    def mouse_callback(event, x, y, flags, param):
        nonlocal ix, iy, on_drawing, roi, temp_image
        # 如果鼠标左键按下，则开始绘制ROI框架
        if event == cv2.EVENT_LBUTTONDOWN:
            on_drawing = True
            ix, iy = x, y
        # 绘制ROI框架
        elif on_drawing and event == cv2.EVENT_MOUSEMOVE:
            mask = cv2.rectangle(numpy.zeros_like(temp_image), (ix, iy), (x, y), (0, 255, 0), 1)
            cv2.imshow(winname, temp_image | mask)
        # 鼠标左键释放，绘制ROI框架并提取ROI
        elif event == cv2.EVENT_LBUTTONUP:
            on_drawing = False
            # cv2.rectangle(temp_image, (ix, iy), (x, y), (0, 255, 0), 2)
            roi = ix, iy, x, y
            print(roi)

    # 创建窗口并绑定鼠标回调函数
    cv2.namedWindow(winname)
    cv2.setMouseCallback(winname, mouse_callback)
    # 显示截图

    cv2.imshow(winname, temp_image)
    if cv2.waitKey(0) == 13:  # 按下回车键结束循环
        # 销毁所有窗口
        cv2.destroyAllWindows()
        return roi
