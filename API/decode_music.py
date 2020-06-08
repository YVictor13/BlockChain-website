import wave         
import struct
import sys

def recover_lsb_watermark(watermarked_filepath):
    # Simply collect the LSB from each sample
    watermarked_audio = wave.open(watermarked_filepath, 'rb') 
    
    (nchannels, sampwidth, framerate, nframes, comptype, compname) = watermarked_audio.getparams()
    frames = watermarked_audio.readframes (nframes * nchannels)
    samples = struct.unpack_from ("%dh" % nframes * nchannels, frames)
    
  
    watermark_bytes = 0
    for (sample,i) in zip(samples[0:32], range(0,32)):
        watermark_bytes = watermark_bytes + ( (sample & 1) * (2 ** i))
    
       
    watermark_data = []
    
    for n in range(0, watermark_bytes):
        watermark_byte_samples = samples[32 + (n * 8) : 32+((n+1) * 8)]
        watermark_byte = 0
        for (sample, i) in zip(watermark_byte_samples, range(0,8)):
            watermark_byte = watermark_byte + ( (sample & 1) * (2**i) )
        watermark_data.append(watermark_byte)
    data1 = []
    for data in watermark_data:
        data1.append(chr(data))
    print("The watermark is: ")
    print("".join(data1))
    return data1

if __name__ == "__main__":
    output = "w.wav"
    if len(sys.argv) > 1:
        output = sys.argv[1]
    recover_lsb_watermark(output)
