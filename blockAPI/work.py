from blockAPI.music.mdecode import mdecode
from blockAPI.music.mencode import mencode
from blockAPI.picture.pdecode import pdecode
from blockAPI.picture.pencode import pencode
from blockAPI.video.vdecode import vdecode
from blockAPI.video.vencode import vencode
import warnings
warnings.filterwarnings("ignore", category=FutureWarning, module="sklearn", lineno=1978)


class work(object):
    def __init__(self):
        self.mdecode = mdecode()
        self.mencode = mencode()
        self.pdecode = pdecode()
        self.pencode = pencode()
        self.vdecode = vdecode()
        self.vencode = vencode()

    # 音频去水印函数
    # 参数：含水印音频路径watermarked_filepath 水印输出路径res_path
    def dmusic(self, watermarked_filepath, res_path):
        self.mdecode.recover_lsb_watermark(watermarked_filepath, res_path)

    # 音频加水印函数
    # 参数：原始音频路径music_path，文本水印watermark_data，添加水印后音频保存路径res_path
    def emusic(self, music_path, watermark_data, res_path):
        self.mencode.lsb_watermark(music_path, watermark_data, res_path)

    # 图片去水印函数
    # 参数 原图片路径img_path，含水印图片路径wm_path，水印输出路径res_path，密码password
    def dpicture(self, img_path, wm_path, res_path, password):
        self.pdecode.decoder(img_path, wm_path, res_path, password)

    # 图片加水印函数
    # 参数：原图片路径img_path，文本水印/图片水印文件路径WatterMark，添加水印后图片保存路径res_path，密码password，水印方式pic_flag(0为文本水印，1为图片水印)
    def epicture(self, img_path, WatterMark, res_path, password, pic_flag):
        self.pencode.encoder(img_path, WatterMark, res_path, password, pic_flag)

    # 视频去水印函数
    # 参数：原始视频路径video_path 含水印视频路径watervideo_path 水印图片保存位置res_path 水印强度alpha
    def dvideo(self, video_path, watervideo_path, res_path, alpha):
        self.vdecode.decode(video_path, watervideo_path, res_path, alpha)

    # 视频加水印函数
    # 参数：原始视频路径video_path 图片水印路径vm_path 添加水印后视频输出位置res_path 水印强度alpha
    def evideo(self, video_path, vm_path, res_path, alpha):
        self.vencode.main(video_path, vm_path, res_path, alpha)


if __name__ == '__main__':
    w = work()
    img_path = r'D:\project\Python\Demo\upload\2020061008251423.png'
    watterMark = r'E:\project\Python\Demo\blockAPI\video\watermark.png'
    res_path = r'E:\project\Python\Demo\upload'
    password = '12345'
    pic_flag = 1
    w.epicture(img_path, watterMark, res_path, password, pic_flag)
