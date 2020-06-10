# -*- coding: utf8 -*-

import random
import cv2
import math
import numpy as np
from pyzbar.pyzbar import decode
import sys
from PIL import Image, ImageDraw, ImageFont
import os
import argparse


class pdecode(object):
    def __init__(self):
        pass

    def decoder(self, ori_path, wm_path, Watermark, password):
        alpha = 10
        password = int(password.encode('ascii').hex())
        ori = cv2.imdecode(np.fromfile(ori_path, dtype=np.uint8), -1)
        vm = cv2.imdecode(np.fromfile(wm_path, dtype=np.uint8), -1)

        watermark = Image.open(wm_path)
        h_o, w_o = ori.shape[0], ori.shape[1]
        h_v, w_v = vm.shape[0], vm.shape[1]
        if h_o > h_v or w_o > w_v:
            # 补宽度
            if w_o > w_v:
                w1 = w_o - w_v
                h1 = h_v
                # 裁图
                tmp1 = watermark.copy()
                box1 = (0, 0, w1, h1)
                cut1 = tmp1.crop(box1)  # 裁剪图片
                # 拼接
                im1 = Image.new('RGB', (w_o, h_v), (0, 0, 0))
                box1 = (0, 0, w_v, h_v)
                im1.paste(watermark, box1)
                box1 = (w_v, 0, w_o, h_v)
                im1.paste(cut1, box1)
                im1.save("im.png")
                watermark = im1
            # 补高度
            if h_o > h_v:
                w2 = w_o
                h2 = h_o - h_v
                # cut
                tmp2 = watermark.copy()
                box2 = (0, 0, w2, h2)
                cut2 = tmp2.crop((box2))
                # link
                im2 = Image.new('RGB', (w_o, h_o), (0, 0, 0))
                im2.paste(watermark, (0, 0))
                im2.paste(cut2, (0, h_v))
                im2.save("im.png")
                vm = cv2.imread("im.png", -1)

        out_tmp = next(self.decodeImg([ori], vm, password, Watermark, alpha))

        self.qrDecode(out_tmp, Watermark)

    def decodeImg(self, ori_imgs, img, password, res_path, alpha):
        for ori_img in ori_imgs:
            if ori_img.shape[0] != img.shape[0] or ori_img.shape[1] != img.shape[1]:
                yield None
            else:
                im_height, im_width, im_channel = np.shape(ori_img)
                ori_f = np.fft.fftshift(np.fft.fft2(ori_img))
                img_f = np.fft.fftshift(np.fft.fft2(img))

                watermark = np.abs((img_f - ori_f) / 5.5)
                res = np.zeros(watermark.shape)

                x, y = list(range(math.floor(im_height / 2))), list(range(math.floor(im_width / 2)))
                random.seed(password)
                random.shuffle(x)
                random.shuffle(y)

                for i in range(math.floor(im_height / 2)):
                    for j in range(math.floor(im_width / 2)):
                        res[x[i]][y[j]] = watermark[i][j]
                        res[im_height - i - 1][im_width - j - 1] = res[i][j]
                cv2.imencode('.png', res, [int(cv2.IMWRITE_PNG_COMPRESSION), 9])[1].tofile(res_path)
                yield res
        return

    def qrDecode(self, img, Watermark):

        im_gray = cv2.split(img)[2]  # split()颜色通道分离：B.G.R
        _, out_tmp = cv2.threshold(im_gray, 100, 255, cv2.THRESH_BINARY)
        # threshold 方法是通过遍历灰度图中点，将图像信息二值化
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 25))
        # 定义5*5的矩形结构元素
        closed = cv2.morphologyEx(out_tmp, cv2.MORPH_CLOSE, kernel)
        # 闭运算 先膨胀后腐蚀，用来连接被误分为许多小块的对象
        closed = cv2.erode(closed, None, iterations=4)  # 腐蚀 迭代4次
        closed = cv2.dilate(closed, None, iterations=4)  # 膨胀 迭代4次
        # 先腐蚀后膨胀，用于移除由图像噪音形成的斑点。
        closed = cv2.merge([closed, closed, closed])  # 通道合并
        gray = cv2.cvtColor(closed.astype('uint8'), cv2.COLOR_BGR2GRAY)  # BGR->灰度图
        _, closed = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)
        # 转换为二值图
        cnts, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        tmp = sorted(cnts, key=cv2.contourArea, reverse=True)
        # 排序 contourArea计算图像轮廓面积
        if len(tmp) == 0:
            return None
        c = tmp[0]
        rect = cv2.minAreaRect(c)
        # 返回（最小外接矩形的中心（x，y），（宽度，高度），旋转角度）
        box = np.int0(cv2.boxPoints(rect))
        # np.int0==np.int64
        # 通过函数 cv2.cv.BoxPoints() 获得矩形的4个顶点坐标
        # 返回形式[ [x0,y0], [x1,y1], [x2,y2], [x3,y3] ]
        Xs = [i[0] for i in box]
        Ys = [i[1] for i in box]
        x1 = min(Xs)
        x2 = max(Xs)
        y1 = min(Ys)
        y2 = max(Ys)
        crop_height = y2 - y1
        crop_width = x2 - x1
        cropImg = out_tmp[y1:y1 + crop_height, x1:x1 + crop_width]
        # 目标图像裁剪
        cropImg1 = cropImg
        cv2.imwrite('qrcode.png', cropImg1, [cv2.IMWRITE_PNG_COMPRESSION, 7])
        fout = open("information.txt", "w+", encoding="utf-8")

        im = cv2.imread('qrcode.png', -1)
        qr_data = decode(im)
        if qr_data:
            for txt in qr_data:
                data = txt.data.decode('utf-8')
                print(data)
                out = "文字解码成功,内容：" + data
                fout.write(out)
        else:
            fout.write("未成功识别文字内容")
            cv2.imwrite(Watermark, cropImg1, [cv2.IMWRITE_PNG_COMPRESSION, 7])


if __name__ == "__main__":
    pass
