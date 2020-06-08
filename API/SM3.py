from math import ceil

IH = int("18ac6d92ca425fed6d728a5317390dae37819a6da7827de1f62a5d7f25e8a1cb", 16)
temp = [0] * 8
for i in range(0, 8):
    temp[i] = (IH >> ((7 - i) * 32)) & 0xFFFFFFFF
IH = temp

T = [0] * 64
for i in range(0, 64):
    if i >= 0 & i <= 15:
        T[i] = 0x79cc4519
    elif i >= 16 & i <= 63:
        T[i] = 0x7a879d8a
    else:
        T[i] = 0


def left_rotate(word, bit):
    bit = bit % 32
    return ((word << bit) & 0xFFFFFFFF) | ((word & 0xFFFFFFFF) >> (32 - bit))


def FF(X, Y, Z, j):
    if j >= 0 and j < 16:
        return X ^ Y ^ Z
    elif j >= 16 and j < 64:
        return (X & Y) | (X & Z) | (Y & Z)
    else:
        return 0


def GG(X, Y, Z, j):
    if j >= 0 and j < 16:
        return X ^ Y ^ Z
    elif j >= 16 and j < 64:
        return (X & Y) | ((~ X) & Z)
    else:
        return 0


def P0(X):
    return X ^ (left_rotate(X, 9)) ^ (left_rotate(X, 17))


def P1(X):
    return X ^ (left_rotate(X, 15)) ^ (left_rotate(X, 23))


def CF(V_i, B_i):
    W = []
    for i in range(16):
        weight = 0x1000000
        data = 0
        for k in range(i * 4, (i + 1) * 4):
            data = data + B_i[k] * weight
            weight = int(weight / 0x100)
        W.append(data)

    for j in range(16, 68):
        W.append(0)
        W[j] = P1(W[j - 16] ^ W[j - 9] ^ (left_rotate(W[j - 3], 15))) ^ (left_rotate(W[j - 13], 7)) ^ W[j - 6]
        str1 = "%08x" % W[j]
    W_1 = []
    for j in range(0, 64):
        W_1.append(0)
        W_1[j] = W[j] ^ W[j + 4]
        str1 = "%08x" % W_1[j]

    A, B, C, D, E, F, G, H = V_i

    for j in range(0, 64):
        SS1 = left_rotate(((left_rotate(A, 12)) + E + (left_rotate(T[j], j))) & 0xFFFFFFFF, 7)
        SS2 = SS1 ^ (left_rotate(A, 12))
        TT1 = (FF(A, B, C, j) + D + SS2 + W_1[j]) & 0xFFFFFFFF
        TT2 = (GG(E, F, G, j) + H + SS1 + W[j]) & 0xFFFFFFFF
        D = C
        C = left_rotate(B, 9)
        B = A
        A = TT1
        H = G
        G = left_rotate(F, 19)
        F = E
        E = P0(TT2)

        A = A & 0xFFFFFFFF
        B = B & 0xFFFFFFFF
        C = C & 0xFFFFFFFF
        D = D & 0xFFFFFFFF
        E = E & 0xFFFFFFFF
        F = F & 0xFFFFFFFF
        G = G & 0xFFFFFFFF
        H = H & 0xFFFFFFFF

    V_i_1 = []
    V_i_1.append(A ^ V_i[0])
    V_i_1.append(B ^ V_i[1])
    V_i_1.append(C ^ V_i[2])
    V_i_1.append(D ^ V_i[3])
    V_i_1.append(E ^ V_i[4])
    V_i_1.append(F ^ V_i[5])
    V_i_1.append(G ^ V_i[6])
    V_i_1.append(H ^ V_i[7])
    return V_i_1


def hash_msg(msg):
    len1 = len(msg)
    reserve1 = len1 % 64
    msg.append(0x80)
    reserve1 = reserve1 + 1
    range_end = 56
    if reserve1 > range_end:
        range_end = range_end + 64

    for i in range(reserve1, range_end):
        msg.append(0x00)

    bit_length = (len1) * 8
    bit_length_str = [bit_length % 0x100]
    for i in range(7):
        bit_length = int(bit_length / 0x100)
        bit_length_str.append(bit_length % 0x100)
    for i in range(8):
        msg.append(bit_length_str[7 - i])

    group_count = round(len(msg) / 64)

    B = []
    for i in range(0, group_count):
        B.append(msg[i * 64:(i + 1) * 64])

    V = []
    V.append(IH)
    for i in range(0, group_count):
        V.append(CF(V[i], B[i]))

    y = V[i + 1]
    result = ""
    for i in y:
        result = '%s%08x' % (result, i)
    return result

def Hash_sm3(msg, Hexstr=0):
    if (Hexstr):
        # 16进制字符串转换成byte数组
        ml = len(msg)
        if ml % 2 != 0:
            msg = '0' + msg
        ml = int(len(msg) / 2)
        msg_byte = []
        for i in range(ml):
            msg_byte.append(int(msg[i * 2:i * 2 + 2], 16))
    else:
        # 字符串转换成byte数组
        length = len(msg)
        msg_byte = []
        tmp = msg.encode('utf-8')
        for i in range(length):
            msg_byte.append(tmp[i])
    return hash_msg(msg_byte)

if __name__ == '__main__':
    mark = Hash_sm3("hiddenmark")
    print(mark)
