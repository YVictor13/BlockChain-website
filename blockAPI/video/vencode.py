# coding=utf-8
import os
import random

import cv2
import numpy as np
from statsmodels.sandbox.tsa.try_arma_more import wm

ALPHA = 5


class vencode(object):
    def __init__(self):
        pass

    def main(self, video, vm, res, alpha):
        alpha = float(alpha)
        videocapture = cv2.VideoCapture(video)
        frames_num = videocapture.get(7)
        width = videocapture.get(3)
        height = videocapture.get(4)
        size = (int(width), int(height))
        fps = videocapture.get(5)
        success, frame = videocapture.read()
        path1 = 'out.png'
        cv2.imwrite(path1, frame)
        self.encode(path1, wm, res, alpha)
        i = 2
        while success:
            path = 'work\\image' + str(i) + '.png'

            cv2.imwrite(path, frame)
            i = i + 1
            success, frame = videocapture.read()

        im_list = os.listdir('work')
        im_list.sort(key=lambda x: int(x.replace("image", "").split('.')[0]))
        videoWriter = cv2.VideoWriter("2.avi", cv2.VideoWriter_fourcc(*'XVID'), int(fps), size)
        for i in im_list:
            im_name = os.path.join('work\\' + i)
            frame = cv2.imdecode(np.fromfile(im_name, dtype=np.uint8), -1)
            videoWriter.write(frame)
        videoWriter.release()

    def encode(self, img_path, wm_path, res_path, alpha):
        img = cv2.imread(img_path)
        img_f = np.fft.fft2(img)
        height, width, channel = np.shape(img)
        watermark = cv2.imread(wm_path)
        wm_height, wm_width = watermark.shape[0], watermark.shape[1]
        x, y = range(height // 2), range(width)
        random.seed(height + width)
        random.shuffle(list(x))
        random.shuffle(list(y))
        tmp = np.zeros(img.shape)
        for i in range(height // 2):
            for j in range(width):
                if x[i] < wm_height and y[j] < wm_width:
                    tmp[i][j] = watermark[x[i]][y[j]]
                    tmp[height - 1 - i][width - 1 - j] = tmp[i][j]
        res_f = img_f + alpha * tmp
        res = np.fft.ifft2(res_f)
        res = np.real(res)
        cv2.imwrite(res_path, res, [int(cv2.IMWRITE_JPEG_QUALITY), 100])


if __name__ == '__main__':
    pass
