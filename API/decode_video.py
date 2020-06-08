# coding=utf-8
import cv2
import numpy as np
import random
import os
from argparse import ArgumentParser
ALPHA = 5


def build_parser():
    parser = ArgumentParser()
    parser.add_argument('--video', dest='video', required=True)
    parser.add_argument('--watervideo', dest='watervideo', required=True)
    parser.add_argument('--result', dest='res', required=True)
    parser.add_argument('--alpha', dest='alpha', default=ALPHA)
    return parser


def main():
    parser = build_parser()
    options = parser.parse_args()
    video = options.video
    watervideo = options.watervideo
    res = options.res
    alpha = float(options.alpha)
    if not os.path.isfile(video):
        parser.error("original image %s does not exist." % ori)
    if not os.path.isfile(watervideo):
        parser.error("image %s does not exist." % img)
    path1 = 'C:\\Users\\dell\\Desktop\\out1.png'
    path2 = 'C:\\Users\\dell\\Desktop\\out2.png'
    videocapture = cv2.VideoCapture(video)
    success,frame = videocapture.read()
    cv2.imwrite(path1,frame)

    videocapture = cv2.VideoCapture(watervideo)
    success,frame = videocapture.read()
    cv2.imwrite(path2,frame)
    decode(path1, path2, res, alpha)


def decode(ori_path, img_path, res_path, alpha):
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
    main()
