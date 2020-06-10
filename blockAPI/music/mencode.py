import wave         
import struct
import sys
from pydub.audio_segment import AudioSegment

# cover_filepath is the path to a host WAV audio file 
class mencode(object):
    def __init__(self):
        pass
    def lsb_watermark(self,cover_filepath, watermark_data, watermarked_output_path):
        
        watermark_str = str(watermark_data)
        watermark = struct.unpack("%dB" % len(watermark_str), watermark_str.encode())
        #将字符串转变为元组
        watermark_size = len(watermark)
        watermark_bits = self.watermark_to_bits((watermark_size,), 32)
        watermark_bits.extend(self.watermark_to_bits(watermark))
        #在water_bits后面再加一个新列表
        cover_audio = wave.open(cover_filepath, 'rb') 
        #调用wave.open打开wav文件，使用"rb"(二进制模式)打开文件
        (nchannels, sampwidth, framerate, nframes, comptype, compname) = cover_audio.getparams()
        #返回声道，采样宽度，帧速率，帧数，唯一标识，无损
        frames = cover_audio.readframes (nframes * nchannels)
        #读取声音数据，传递读取长度，返回二进制数据  （频率*采样点个数=时长）
        samples = struct.unpack_from ("%dh" % nframes * nchannels, frames)

        if len(samples) < len(watermark_bits):
            raise OverflowError("The watermark data provided is too big to fit into the cover audio! Tried to fit %d bits into %d bits of space." % (len(watermark_bits), len(samples))) 
        
        print ("Watermarking %s (%d samples) with %d bits of information." % (cover_filepath, len(samples), len(watermark_bits)))
        
        encoded_samples = []
        
        watermark_position = 0
        n = 0
        for sample in samples:
            encoded_sample = sample
            
            if watermark_position < len(watermark_bits):
                encode_bit = watermark_bits[watermark_position]
                if encode_bit == 1:
                    encoded_sample = sample | encode_bit
                else:
                    encoded_sample = sample
                    if sample & 1 != 0:
                        encoded_sample = sample - 1
                        
                watermark_position = watermark_position + 1
                
            encoded_samples.append(encoded_sample)
                
        encoded_audio = wave.open(watermarked_output_path, 'wb')
        encoded_audio.setparams( (nchannels, sampwidth, framerate, nframes, comptype, compname) )
        #设置参数
        encoded_audio.writeframes(struct.pack("%dh" % len(encoded_samples), *encoded_samples))
        #写入output路径
        
    def watermark_to_bits(self,watermark, nbits=8):
        watermark_bits = []
        for byte in watermark:
            for i in range(0,nbits):
                watermark_bits.append( (byte & (2 ** i)) >> i )
        return watermark_bits
        
    
if __name__ == "__main__":
    cover_audio = "ori.wav"
    output = "w.wav"
    source = sys.argv[2]
    sound = AudioSegment.from_mp3(source)
    sound.export(cover_audio, format = 'wav')
    if len(sys.argv) > 1:
        message = sys.argv[1]
        if len(sys.argv) > 3:
            output = sys.argv[3]
  
    # lsb_watermark(cover_audio, message, output)
    
    #print(recover_lsb_watermark(output))
