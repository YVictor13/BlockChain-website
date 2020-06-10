from random import choice
from math import ceil

# 设置椭圆曲线参数
import SM3

sm2_N = int('927394057A73B846D83012A8476D9302E65930CDB5ADC3749BEDAC7392027153', 16)
sm2_P = int('FFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF', 16)
sm2_G = '827836BADECA678A687C7D87CE97B67D8C8A68D686983BDC8638769CD6C9E9D987C6D6E8C68DE5C75DC5DE2C4DC25E4578E7A8B757A66BA8BA865D5B76DCE865'  # G点
sm2_a = int('ADE537DCEB3745957234AEEDBC6489506E6D8D9C0D7B634BA78495BDCE5374CD',16)
sm2_b = int('ABDCE75DBEA6283057DACEBADEC37496037153DBEDACBDE6384769705834624A',16)
sm2_a_3 = (sm2_a + 3) % sm2_P # 在使用倍点时，用到的中间值
Fp = 256

def kG(k, Point,length):  # kP运算
    Point = '%s%s' % (Point, '1')
    mask_str = '8' + '0'*(length-1)
    mask = int(mask_str, 16)
    Temp = Point
    flag = False

    for n in range(length * 4):
        if (flag):   # 倍点
            l = len(Temp)
            len_2 = 2 * length
            if l < length * 2:
                Temp = None
            else:
                x1 = int(Temp[0:length], 16)
                y1 = int(Temp[length:len_2], 16)
                if l == len_2:
                    z1 = 1
                else:
                    z1 = int(Temp[len_2:], 16)
                T6 = (z1 * z1) % sm2_P
                T2 = (y1 * y1) % sm2_P
                T3 = (x1 + T6) % sm2_P
                T4 = (x1 - T6) % sm2_P
                T1 = (T3 * T4) % sm2_P
                T3 = (y1 * z1) % sm2_P
                T4 = (T2 * 8) % sm2_P
                T5 = (x1 * T4) % sm2_P
                T1 = (T1 * 3) % sm2_P
                T6 = (T6 * T6) % sm2_P
                T6 = (sm2_a_3 * T6) % sm2_P
                T1 = (T1 + T6) % sm2_P
                z3 = (T3 + T3) % sm2_P
                T3 = (T1 * T1) % sm2_P
                T2 = (T2 * T4) % sm2_P
                x3 = (T3 - T5) % sm2_P
                if (T5 % 2) == 1:
                    T4 = (T5 + ((T5 + sm2_P) >> 1) - T3) % sm2_P
                else:
                    T4 = (T5 + (T5 >> 1) - T3) % sm2_P

                T1 = (T1 * T4) % sm2_P
                y3 = (T1 - T2) % sm2_P
                form = '%%0%dx' % length
                form = form * 3
                Temp = form % (x3, y3, z3)
        if (k & mask) != 0:
            if (flag):  # 点加函数，P2点为仿射坐标即z=1，P1为Jacobian加重射影坐标
                len_2 = 2 * length
                l1 = len(Temp)
                l2 = len(Point)
                if (l1 < len_2) or (l2 < len_2):
                    Temp = None
                else:
                    X1 = int(Temp[0:length], 16)
                    Y1 = int(Temp[length:len_2], 16)
                    if (l1 == len_2):
                        Z1 = 1
                    else:
                        Z1 = int(Temp[len_2:], 16)

                    x2 = int(Point[0:length], 16)
                    y2 = int(Point[length:len_2], 16)
                    T1 = (Z1 * Z1) % sm2_P
                    T2 = (y2 * Z1) % sm2_P
                    T3 = (x2 * T1) % sm2_P
                    T1 = (T1 * T2) % sm2_P
                    T2 = (T3 - X1) % sm2_P
                    T3 = (T3 + X1) % sm2_P
                    T4 = (T2 * T2) % sm2_P
                    T1 = (T1 - Y1) % sm2_P
                    Z3 = (Z1 * T2) % sm2_P
                    T2 = (T2 * T4) % sm2_P
                    T3 = (T3 * T4) % sm2_P
                    T5 = (T1 * T1) % sm2_P
                    T4 = (X1 * T4) % sm2_P
                    X3 = (T5 - T3) % sm2_P
                    T2 = (Y1 * T2) % sm2_P
                    T3 = (T4 - X3) % sm2_P
                    T1 = (T1 * T3) % sm2_P
                    Y3 = (T1 - T2) % sm2_P
                    form = '%%0%dx' % length
                    form = form * 3
                    Temp = form % (X3, Y3, Z3)
            else:
                flag = True
                Temp = Point
        k = k << 1
     # Jacobian加重射影坐标转换成仿射坐标
    len_2 = 2 * length
    x = int(Temp[0:length], 16)
    y = int(Temp[length:len_2], 16)
    z = int(Temp[len_2:], 16)
    z_inv = pow(z, sm2_P - 2, sm2_P)
    z_invSquar = (z_inv * z_inv) % sm2_P
    z_invQube = (z_invSquar * z_inv) % sm2_P
    x_new = (x * z_invSquar) % sm2_P
    y_new = (y * z_invQube) % sm2_P
    z_new = (z * z_inv) % sm2_P
    if z_new == 1:
        form = '%%0%dx' % length
        form = form * 2
        return form % (x_new, y_new)
    else:
        print ("Point is not infinit")
        return None

def Encrypt(Mi,PA,length,Hexstr = 0):# 加密函数，Mi消息，PA公钥
    if Hexstr:
        msg = Mi # 输入消息为16进制字符串
    else:
        msg = Mi.encode('utf-8')
        msg = msg.hex() # 转化为16进制字符串

    letter = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
    k = ''
    for i in range(length):
        a = choice(letter)
        k = k + a

    C1 = kG(int(k,16),sm2_G,length)
    xy = kG(int(k,16),PA,length)
    x2 = xy[0:length]
    y2 = xy[length:2*length]
    ml = len(msg)

    # xy为16进制表示的比特串（str），ml/2为密钥长度（单位byte）
    klen = int(ml/2)
    ct = 0x00000001
    rcnt = ceil(klen / 32)

    # 16进制字符串转换成byte数组
    mml = len(xy)
    temp = xy
    if mml % 2 != 0:
        temp = '0' + temp
    mml = int(mml / 2)
    msg_byte = []
    for i in range(mml):
        msg_byte.append(int(temp[i * 2:i * 2 + 2], 16))
    Zin = msg_byte

    Ha = ""
    for i in range(rcnt):
        # 16进制字符串转换成byte数组
        temp = '%08x' % ct
        mml = len(temp)
        if mml % 2 != 0:
            temp = '0' + temp
        mml = int(mml / 2)
        msg_byte = []
        for i in range(mml):
            msg_byte.append(int(temp[i * 2:i * 2 + 2], 16))
        tbyte = msg_byte
        temp_msg = Zin + tbyte
        Ha = Ha + SM3.hash_msg(temp_msg)
        ct += 1
    t = Ha[0: klen * 2]

    if int(t,16)==0:
        return None
    else:
        form = '%%0%dx' % ml
        C2 = form % (int(msg,16) ^ int(t,16))
        C3 = SM3.Hash_sm3('%s%s%s' % (x2, msg, y2), 1)
        return '%s%s%s' % (C1,C3,C2)

def Decrypt(Mii,DA,length):# 解密函数，Mii密文（16进制字符串），DA私钥
    len_2 = 2 * length
    len_3 = len_2 + 64
    C1 = Mii[0:len_2]
    C3 = Mii[len_2:len_3]
    C2 = Mii[len_3:]
    xy = kG(int(DA,16),C1,length)
    x2 = xy[0:length]
    y2 = xy[length:len_2]
    cl = len(C2)
    # xy为16进制表示的比特串（str），cl/2为密钥长度（单位byte）
    klen = int(cl/2)
    ct = 0x00000001
    rcnt = ceil(klen / 32)

    # 16进制字符串转换成byte数组
    mml = len(xy)
    temp = xy
    if mml % 2 != 0:
        temp = '0' + temp
    mml = int(mml / 2)
    msg_byte = []
    for i in range(mml):
        msg_byte.append(int(temp[i * 2:i * 2 + 2], 16))
    Zin = msg_byte

    Ha = ""
    for i in range(rcnt):
        # 16进制字符串转换成byte数组
        temp = '%08x' % ct
        mml = len(temp)
        if mml % 2 != 0:
            temp = '0' + temp
        mml = int(mml / 2)
        msg_byte = []
        for i in range(mml):
            msg_byte.append(int(temp[i * 2:i * 2 + 2], 16))
        tbyte = msg_byte

        temp_msg = Zin + tbyte
        msg = Zin + tbyte
        Ha = Ha + SM3.hash_msg(msg)
        ct += 1
    t = Ha[0: klen * 2]

    if int(t,16) == 0:
        return None
    else:
        form = '%%0%dx' % cl
        M = form % (int(C2,16) ^ int(t,16))
        u = SM3.Hash_sm3('%s%s%s' % (x2, M, y2), 1)
        if  (u == C3):
            return M
        else:
            return None

if __name__ == '__main__':

    length = int(Fp / 4)
    Da = 'ABDCE75DBEA6283057DACEBADEC37496037153DBEDACBDE6384769705834624A'
    Pa = kG(int(Da, 16), sm2_G,length)

    Mi = "hiddenmark"
    print('Mi = %s' % Mi)

    Mii = Encrypt(Mi,Pa,length,0)
    print('Mii = %s' % Mii)

    print('Decrypt:')
    m = Decrypt(Mii,Da,length)
    M = bytes.fromhex(m)
    print(M.decode())
