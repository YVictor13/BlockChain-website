import time
import hashlib
import json
import random
import threading
from API.SM3 import *
from API.SM2 import *
import pymysql

conn = pymysql.connect(   #连接数据库
    host='localhost',
    user='root',
    password='9625',
    db='test',
    charset='utf8',
)
cur = conn.cursor()  #创建游标对象
#创建数据表，执行一次就行
try:
    create_sqli = "create table BlockChain (previous_hash varchar(64),username varchar(30),type varchar(15),msg varchar(30),hmsg varchar(64),time_stamp varchar(30),nonce int,hash varchar(64));"
    cur.execute(create_sqli)
except Exception as e:
    error = 'already have'

class MyThread(threading.Thread):  #方便线程返回数值
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

class Mine():  #挖矿
    def __init__(self,data):
        self.hash = []
        self.time = time.asctime(time.localtime(time.time()))
        self.diffculty = 2
        self.data = data + self.time
        self.timetable = []
        self.finish = 0

    def get_mine(self):  #加入挖矿
        target = '0'*self.diffculty
        num = 0
        hash1 = ''
        while (int(hash1[0:self.diffculty] != target)):  #满足时挖矿成功
            Da = 'ABDCE75DBEA62830CEBADEC37496037153DBEDACBDE6384769705834624A'
            Pa = kG(int(Da, 16), sm2_G, 64)
            hash1 = Encrypt(self.data, Pa, 64, 0)  #可以尝试多个mine
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
            t = MyThread(self.get_mine, args=(i, ))
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

class Block():  #块的基础

    def __init__(self,username, msg, previous_hash):  #需要作者信息，图片信息和前一个哈希值
        self.previous_hash = previous_hash  #前一个块的哈希
        self.msg = msg   #图片信息
        self.hmsg = Hash_sm3(self.msg)
        self.username = username   #用户名字
        self.type = "picture"
        self.time_stamp = ''   #时间戳
        self.nonce = random.randint(0,99)    #随机值
        self.hash = ''

    def get_data(self):  #计算哈希值
        data = self.previous_hash+self.msg+self.hmsg+self.username+self.type+str(self.nonce)
        m = Mine(data)
        self.hash = m.mine()
        self.time_stamp = m.get_time()
        info = [(self.previous_hash,self.username,self.type,self.msg,self.hmsg,self.time_stamp,1,self.hash)]
        insert_sqli = "insert into BlockChain values(%s, %s, %s, %s, %s, %s, %s, %s);"
        cur.executemany(insert_sqli, info)
        conn.commit()


class Chain():  #创建区块链，链起来

    def __init__(self):
        self.list = []  #链表
        self.diffculty = 2

    def block_dict(self, Block):  #获取block的字典，为了转换成json
        return Block.__dict__

    def add_block(self, block):  #添加区块，需要block
        block.get_data()
        self.list.append(block)

    def show(self):  #打印所有区块
        json_res = json.dumps(self.list, default=self.block_dict)
        with open("chain.txt", "w") as fp:
            fp.write(json_res)
        print(json_res)

    def Valid(self):  #验证
        for i in range(1, len(self.list)):  #遍历每一个区块
            current_block = self.list[i]
            previous_block = self.list[i - 1]
            if (current_block.previous_hash != previous_block.hash):
                print('Previous hash is not eaqual')
                return False   #判断存储的上一个hash和上一个hash
            print('All the blocks are correct')
            return True

if __name__ == '__main__':
    c = Chain()
    c.add_block(Block('tom','first','0'))
    c.add_block(Block('may','second', c.list[len(c.list)-1].hash))
    c.add_block(Block('may', 'second', c.list[len(c.list) - 1].hash))
    c.show()
    c.Valid()
