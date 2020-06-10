# -*- coding: utf8 -*-

import sys
import cv2
import numpy as np
import qrcode
import random
import math
import os
import argparse

def main():
    usage = "Usage %prog [-o OririnImage] [-t target] host"
    parser = argparse.ArgumentParser()
    parser.add_argument('-o',dest = 'OririnImage',help = 'The Original carrier image')
    parser.add_argument('-f',dest = 'Flag',help = 'Select the form of watermark information: 0 for text and 1 for picture')
    parser.add_argument('-w',dest = 'WatterMark',help = 'The watermark information')
    parser.add_argument('-t',dest = 'Output',help = 'The target picture')
    parser.add_argument('-p',dest = 'Password',help = 'The password of your picture')
  
    results = parser.parse_args()
    print ('OririnImage = ',results.OririnImage)
    print ('Flag = ',results.Flag)
    print ('WatterMark =',results.WatterMark)
    print ('Output = ',results.Output)
    print ('Password = ',results.Password)

    password = 123456789
    alpha = 10
    # 参数1为原图
    OririnImage = results.OririnImage
    # 参数2为FLAG,flag=0 文字，flag=1图片
    pic_flag = results.Flag
    # 参数3为水印
    WatterMark = results.WatterMark
    # 参数4为输出
    Output = results.Output
    # 参数5为密码
    if results.Password is not None:
        password = int(results.Password.encode('ascii').hex())  #转换为16进制ASCII码
    if (pic_flag == '0'):
        encodeByTextQr(OririnImage, WatterMark, Output, password, alpha)
    elif (pic_flag == '1'):
        encodePIC(OririnImage, WatterMark, Output, password, alpha)


def encodeByTextQr(img_path, txt, out_path, password, alpha):
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
    out_img = encodeImg(img, wm, password, alpha)
    if not out_path.endswith(".png"):  #判断字符串是否以指定字符或子字符串结尾;
                                       #star默认为0，end默认为字符串的长度len(str)。
        out_path = out_path + ".png "
    #cv2.imwrite(out_path, out_img, [int(cv2.IMWRITE_PNG_COMPRESSION), 9])
    cv2.imencode('.png', out_img, [int(cv2.IMWRITE_PNG_COMPRESSION), 9])[1].tofile(out_path)
    
    return out_path


def encodeImg(im,mark, password, alpha):
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


def encodePIC(im_path,mark_path, res_path, password, alpha):
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
   main()
