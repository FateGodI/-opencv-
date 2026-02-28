# -opencv-
QR Code Scanner OpenCV Version

Chinese：

二维码扫描器 opencv版本
该扫描器使用python编写 使用前请安装前置

pip install opencv-python pillow requests numpy

OpenCV 的二维码检测器在复杂背景或小二维码下可能不如 ZBar 灵敏，但足以应对大多数场景。

这个较为精简如果需要处理复杂场景，也可以尝试安装 pyzbar 的纯 Python 替代品，如 qreader（基于 YOLO 和 OpenCV），当然，其配置更复杂。

English:

QR Code Scanner (OpenCV Version)
This scanner is written in Python. Please install the prerequisites before use:

pip install opencv-python pillow requests numpy

OpenCV's QR code detector may be less sensitive than ZBar in complex backgrounds or with small QR codes, but it suffices for most scenarios.

This implementation is relatively lightweight. For handling complex scenarios, you may also consider installing pure Python alternatives to pyzbar, such as qreader (based on YOLO and OpenCV). However, its configuration is more complex.

Translated with DeepL.com (free version)
