import hashlib as hasher;
import time as date;
import rsa as key;
import random as RandomNum;
import uuid as id;
import socket as socket;
# import os;
# import multiprocessing as processer;
import threading as threader;
import pickle as pickle;
import Register_Local;
#import pickle as Serialization;

class account(object):
    def __init__(self,name):
        self.name=name;
        self.pswd=hasher.sha256(str(self.name).encode('utf-8')).hexdigest();
        (self.SK,self.PK)=key.newkeys(512);
        self.address=id.uuid4();

class Trade(object):
    def __init__(self,source:account,to,amount):
        self.source=source;
        self.to=to;
        self.amount=amount;
        self.timeStamp=date.ctime(date.time());
        self.ID=id.uuid1();
        self.signature=key.encrypt(str(self.ID).encode('utf-8'),source.SK);


# def TradeProcess():
#     global MainChain;
#     while True:
#         Frequence = RandomNum.randint(0, 3);
#         From = RandomNum.randint(0, 9);
#         To = RandomNum.randint(0, 9);
#         date.sleep(Frequence);
#         newTrade = Trade(Account[From], Account[To], RandomNum.randint(0, 999));
#         #lock.acquire();
#         MainChain[len(MainChain) - 1].updateTrade(newTrade);
#         MainChain[len(MainChain) - 1].rehash();
#         #lock.release();
#         print("%s pays %s %d coins at %s" % (newTrade.source.name, newTrade.to.name, newTrade.amount, newTrade.timeStamp));

def TradeRequest():
    global s;
    while True:
        Frequence = RandomNum.randint(1, 5);
        From = RandomNum.randint(0, 9);
        To = RandomNum.randint(0, 9);
        date.sleep(Frequence);
        newTrade = Trade(Account[From], Account[To], RandomNum.randint(0, 999));
        try:
            for TargetMiner in MinerList:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
                s.connect((TargetMiner[0], 22));
                s.send(pickle.dumps("10086"));
                if pickle.loads(s.recv(1024))==",":
                    s.send(pickle.dumps(newTrade));
                    s.close();
            print("New Trade Request:%s pays %s %d coins at %s" % (newTrade.source.name, newTrade.to.name, newTrade.amount, newTrade.timeStamp));
        except socket.error:
            print("Break Detected!");

def UpdateList():
    global MinerList;
    PingListener = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
    PingListener.bind((socket.gethostname(), 3315));
    PingListener.listen();
    while True:
        PingPackage, addr = PingListener.accept();
        data=b"";
        while True:
            package=PingPackage.recv(4096);
            if not package: break;
            data+=package;
        MinerList = pickle.loads(data);
        print(MinerList);

MinerList=[];
PublicIP,MinerList=Register_Local.ClientRegister();
Update=threader.Thread(target=UpdateList);
Update.start();
# print(s.recv(1024).decode('utf-8'));
n = 0;
Account = [];
while n < 10:
    Account.append(account("No." + str(n)));
    n += 1;
mainThread=threader.Thread(target=TradeRequest);
mainThread.start();