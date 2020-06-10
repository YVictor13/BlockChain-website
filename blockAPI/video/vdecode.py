# coding=utf-8
import random

import cv2
import numpy as np

ALPHA = 5


class vdecode(object):
    def __init__(self):
        pass

    def decode(self, video, watervideo, res_path, alpha):
        ori_path = 'out1.png'
        img_path = 'out2.png'
        alpha = float(alpha)

        videocapture = cv2.VideoCapture(video)
        success, frame = videocapture.read()
        cv2.imwrite(ori_path, frame)

        videocapture = cv2.VideoCapture(watervideo)
        success, frame = videocapture.read()
        cv2.imwrite(img_path, frame)

        ori = cv2.imread(ori_path)
        img = cv2.imread(img_path)
        ori_f = np.fft.fft2(ori)
        img_f = np.fft.fft2(img)
        height, width = ori.shape[0], ori.shape[1]
        watermark = (ori_f - img_f) / alpha
        watermark = np.real(watermark)
        res = np.zeros(watermark.shape)
        random.seed(height + width)
        x = range(height // 2)
        y = range(width)
        random.shuffle(list(x))
        random.shuffle(list(y))
        for i in range(height // 2):
            for j in range(width):
                res[x[i]][y[j]] = watermark[i][j]
        cv2.imwrite(res_path, res, [int(cv2.IMWRITE_JPEG_QUALITY), 100])


if __name__ == '__main__':
    pass
