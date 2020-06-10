# coding=utf-8
import cv2
import numpy as np
import random
import os
from argparse import ArgumentParser
ALPHA = 5


def build_parser():
    parser = ArgumentParser()
    parser.add_argument('--video', dest='vid', required=True)
    parser.add_argument('--watermark', dest='wm', required=True)
    parser.add_argument('--result', dest='res', required=True)
    parser.add_argument('--alpha', dest='alpha', default=ALPHA)
    return parser


def main():
    parser = build_parser()
    options = parser.parse_args()
    video = options.vid
    wm = options.wm
    res = options.res
    alpha = float(options.alpha)
    if not os.path.isfile(video):
        parser.error("image %s does not exist." % video)
    if not os.path.isfile(wm):
        parser.error("watermark %s does not exist." % wm)

    videocapture = cv2.VideoCapture(video)
    frames_num=videocapture.get(7)
    width = videocapture.get(3)
    height = videocapture.get(4)
    size = (int(width),int(height))
    fps = videocapture.get(5)
    success,frame = videocapture.read()
    path1 = 'C:\\Users\\dell\\Desktop\\out.png'
    cv2.imwrite(path1,frame)
    encode(path1, wm, res, alpha)
    i=2
    while success:
        path = 'C:\\Users\\dell\\Desktop\\work\\image' +str(i)+'.png'
      
        cv2.imwrite(path, frame) 
        i = i+1
        success,frame = videocapture.read()
        
    im_list = os.listdir('C:\\Users\\dell\\Desktop\\work')
    im_list.sort(key=lambda x: int(x.replace("image","").split('.')[0]))
    #img = Image.open(os.path.join(im_dir,im_list[0]))
    videoWriter = cv2.VideoWriter("C:\\Users\\dell\\Desktop\\2.avi",cv2.VideoWriter_fourcc(*'XVID'),int(fps),size)
    for i in im_list:
        im_name = os.path.join('C:\\Users\\dell\\Desktop\\work\\'+i)
        frame = cv2.imdecode(np.fromfile(im_name, dtype=np.uint8), -1)
        #filename ='C:\\Users\\dell\\Desktop\\work\\image'+str(i)+'.png'
        videoWriter.write(frame)
    videoWriter.release()


def encode(img_path, wm_path, res_path, alpha):
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
    main()
