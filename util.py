# -*-coding:utf-8-*-
import datetime
import time
import hashlib
import random
import threading
import pymysql
from SM2 import *
from SM3 import *


class Pic_str:
    def create_uuid(self):  # 生成唯一的图片的名称字符串，防止图片显示时的重名问题
        nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S");  # 生成当前时间
        randomNum = random.randint(0, 100);  # 生成的随机整数n，其中0<=n<=100
        if randomNum <= 10:
            randomNum = str(0) + str(randomNum);
        uniqueNum = str(nowTime) + str(randomNum);
        return uniqueNum;


conn = pymysql.connect(  # 连接数据库!!!!!!!根据个人数据库调整
    host='localhost',
    user='root',
    password='123456',
    db='block',
    charset='utf8',
)
cur = conn.cursor()  # 创建游标对象
# 创建数据表
try:
    create_sqli = "create table BlockChain (previous_hash varchar(64),username varchar(30),type varchar(15),msg varchar(30),hmsg varchar(64),time_stamp varchar(30),nonce int,hash varchar(64),filename varchar(64));"
    cur.execute(create_sqli)
except Exception as e:
    error = 'already have'


class MyThread(threading.Thread):  # 方便线程返回数值，参数：函数、元祖；返回：函数执行结果
    def __init__(self, func, args=()):
        super(MyThread, self).__init__()
        self.func = func
        self.args = args
        self.result = 0

    def run(self):
        self.result = self.func()

    def get_result(self):
        try:
            return self.result
        except Exception:
            return None


class Mine():  # 挖矿，参数：交易值data 返回：工作量、hash值
    def __init__(self, data):
        self.hash = []
        self.time = time.asctime(time.localtime(time.time()))
        self.diffculty = 2
        self.data = data + self.time
        self.timetable = []
        self.finish = 0

    def get_mine(self):  # 加入挖矿
        target = '0' * self.diffculty
        num = 0
        hash1 = ''
        while (int(hash1[0:self.diffculty] != target)):  # 满足时挖矿成功
            Da = 'ABDCE75DBEA62830CEBADEC37496037153DBEDACBDE6384769705834624A'
            Pa = kG(int(Da, 16), sm2_G, 64)
            hash1 = Encrypt(self.data, Pa, 64, 0)  # 可以尝试多个mine
            num += 1
            hash256 = hashlib.sha256()  # 赋值加密函数
            hash256.update(hash1.encode('gb2312'))  # 加密
            hash1 = (hash256.hexdigest())
        self.hash.append(hash1)
        self.timetable.append(self.time)
        return num

    def mine(self):
        li = []
        for i in range(2):
            t = MyThread(self.get_mine, args=(i,))
            li.append(t)
            t.start()
        num = 0
        i = 0
        for t in li:
            t.join()
            n = t.get_result()
            if n > num:
                num = n
                self.finish = i
            i += 1
        return self.hash[self.finish]

    def get_time(self):
        return self.timetable[self.finish]


class Block():  # 块的基础#参数：作者信息，图片信息、类型、前一个哈希值

    def __init__(self, username, msg, type, previous_hash, filename):
        self.previous_hash = previous_hash  # 前一个块的哈希
        self.msg = msg  # 图片信息
        self.hmsg = Hash_sm3(self.msg)
        self.username = username  # 用户名字
        self.type = type
        self.time_stamp = ''  # 时间戳
        self.nonce = random.randint(0, 99)  # 随机值
        self.hash = ''
        self.filename = filename

    def get_data(self):  # 计算哈希值
        data = self.previous_hash + self.msg + self.hmsg + self.username + self.type + str(self.nonce) + self.filename
        m = Mine(data)
        self.hash = m.mine()
        self.time_stamp = m.get_time()
        info = [(self.previous_hash, self.username, self.type, self.msg, self.hmsg, self.time_stamp, 1, self.hash,
                 self.filename)]
        insert_sqli = "insert into BlockChain values(%s, %s, %s, %s, %s, %s, %s, %s,%s);"
        cur.executemany(insert_sqli, info)
        conn.commit()


class Chain():  # 创建区块链，链起来，参数：区块

    def __init__(self):
        self.list = []  # 链表
        self.diffculty = 2

    def block_dict(self, Block):  # 获取block的字典，为了转换成json
        return Block.__dict__

    def add_block(self, block):  # 添加区块，需要block
        block.get_data()
        self.list.append(block)
