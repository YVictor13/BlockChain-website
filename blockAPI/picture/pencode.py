# -*- coding: utf8 -*-

import sys
import cv2
import numpy as np
import qrcode
import random
import math
import os
import argparse
class pencode(object):
    def __init__(self):
        pass
    def encoder(self,OririnImage, WatterMark, Output, password, pic_flag):
        if (pic_flag == '0'):
            encodeByTextQr(OririnImage, WatterMark, Output, password)
        elif (pic_flag == '1'):
            encodePIC(OririnImage, WatterMark, Output, password)


    def encodeByTextQr(self,img_path, txt, out_path, password):
        alpha=10
        password = int(password.encode('ascii').hex())  #转换为16进制ASCII码
        img = cv2.imdecode(np.fromfile(img_path, dtype=np.uint8), -1)
        im_height ,im_width ,im_channel = img.shape
        QR_size = math.ceil(min(im_height,im_width) / 150)
        qr = qrcode.QRCode(box_size=QR_size, border=4)
        
        qr.add_data(txt)
        qr.make(fit = True)
        
        wm = qr.make_image()
        wm.save('qrcode.png')
        (wm_w, wm_h) = wm.size  #图像的尺寸，按照像素数计算，它的返回值为宽度和高度的二元组（width, height）
        wm = list(wm.getdata())
        wm = np.array(wm)
        #创建数组
        wm = wm.reshape((wm_h, wm_w))
        #给数组一个新的形状而不改变其数据 宽*高的二维数组
        out_img = self.encodeImg(img, wm, password, alpha)
        if not out_path.endswith(".png"):  #判断字符串是否以指定字符或子字符串结尾;
                                           #star默认为0，end默认为字符串的长度len(str)。
            out_path = out_path + ".png "
        #cv2.imwrite(out_path, out_img, [int(cv2.IMWRITE_PNG_COMPRESSION), 9])
        cv2.imencode('.png', out_img, [int(cv2.IMWRITE_PNG_COMPRESSION), 9])[1].tofile(out_path)
        
        return out_path


    def encodeImg(self,im,mark, password,alpha):
        im_height, im_width, im_channel = np.shape(im)
        mark_height, mark_width = mark.shape[0], mark.shape[1]
        im_f = np.fft.fftshift(np.fft.fft2(im))   #对原图进行FFT后将图像低频移到中心位置
        
        x, y = list(range(math.floor(im_height / 2))), list(range(math.floor(im_width/2)))
        random.seed(password)
        random.shuffle(x) #用于将一个列表中的元素打乱
        random.shuffle(y)
        tmp = np.zeros(im.shape)
        for i in range(math.floor(im_height / 2)):
            for j in range(math.floor(im_width/2)):
                if x[i] < mark_height and y[j] < mark_width:
                    tmp[i][j] = mark[x[i]][y[j]]
                    tmp[im_height - 1 - i][im_width - 1 - j] = tmp[i][j]
        res_f = im_f + alpha * tmp
        res = np.fft.ifftshift(res_f)   # 将高频低频位置移动回去 逆变换
        res = np.fft.ifft2(res) 
        res = np.real(res)

        return res


    def encodePIC(self,im_path,mark_path, res_path, password):
        alpha=10
        password = int(password.encode('ascii').hex())  #转换为16进制ASCII码
        im = cv2.imdecode(np.fromfile(im_path, dtype=np.uint8), -1)
        mark = cv2.imdecode(np.fromfile(mark_path, dtype=np.uint8), -1)
        im_height, im_width, im_channel = np.shape(im)
        mark_height, mark_width = mark.shape[0], mark.shape[1]
        im_f = np.fft.fftshift(np.fft.fft2(im))
        
        x, y = list(range(math.floor(im_height / 2))), list(range(math.floor(im_width/2)))
        random.seed(password)
        random.shuffle(x)
        random.shuffle(y)
        tmp = np.zeros(im.shape)
        for i in range(math.floor(im_height / 2)):
            for j in range(math.floor(im_width/2)):
                if x[i] < mark_height and y[j] < mark_width:
                    tmp[i][j] = mark[x[i]][y[j]]
                    tmp[im_height - 1 - i][im_width - 1 - j] = tmp[i][j]
        res_f = im_f + alpha * tmp
        res = np.fft.ifftshift(res_f)   # 将高频低频位置移动回去 逆变换
        res = np.fft.ifft2(res) 
        res = np.real(res)
        cv2.imencode('.png', res, [int(cv2.IMWRITE_PNG_COMPRESSION), 9])[1].tofile(res_path)

if __name__ == "__main__":
    pass