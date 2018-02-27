import hashlib as hasher;
import time as date;
import rsa as key;
import random as RandomNum;
import uuid as id;
import socket as socket;
import threading as threader;
import pickle as pickle;
import Register_Local;

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


class Block(object):
    def __init__(self,preBlockHash):
        self.data=[];
        self.timeStamp=date.ctime(date.time());
        self.preBlockHash=preBlockHash;
        self.Nonce = 0;
        self.hasher=hasher.sha256();
        self.hasher.update((str(self.timeStamp)+
            str(self.preBlockHash)).encode('utf-8'))
        self.hash = self.hasher.hexdigest();



    def rehash(self):
        self.hasher.update(str(self.data[len(self.data)-1]).encode('utf-8'));
        self.hash=self.hasher.hexdigest();

    def mining(self):
        return hasher.sha256((str(self.hash) + str(self.timeStamp) + str(self.preBlockHash)+ str(self.Nonce)).encode('utf-8')).hexdigest();

    def updateTrade(self,curTrade):
        self.data.append(curTrade);


def TradeProcess():
    # print('Accept new connection from %s:%s...' % addr);
    # sock.send(b'Connection Confirmed...');
    while True:
        date.sleep(1);
        global MainChain;
        global TRADE_BUFFER;
        if len(TRADE_BUFFER)!=0 and PauseFlag:
            newTrade = TRADE_BUFFER[0];
            TRADE_BUFFER.pop(0);
            if verifyTRADE(newTrade):
                #sock.send(b'Trade Confirmed!');
                MainChain[len(MainChain) - 1].updateTrade(newTrade);
                MainChain[len(MainChain) - 1].rehash();
                #print("New Trade:%s pays %s %d coins at %s" % (newTrade.source.name, newTrade.to.name, newTrade.amount, newTrade.timeStamp));

def MiningProcess():
    global MainChain;
    global SocketList;
    global TradeThread;
    global PauseFlag;
    while True:
        curHash = MainChain[len(MainChain) - 1].hash;
        while True:
            cnt = 0;
            while cnt < Difficulty:
                if curHash[cnt] != '0':
                    break;
                else:
                    cnt += 1;
            if cnt != Difficulty or MainChain[len(MainChain) - 1].Nonce==0:
                MainChain[len(MainChain) - 1].Nonce += 1;
                curHash = MainChain[len(MainChain) - 1].mining();
            else:
                PauseFlag=False;
                curBlock=MainChain[len(MainChain)-1];
                curBlock.hasher=0;
                for addr in SocketList:
                    socketMine = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
                    socketMine.connect((addr[0],1111));
                    socketMine.send(pickle.dumps(curBlock));
                    socketMine.close();
                PauseFlag=True;
                break;

def BroadcastListener(recev:socket,addr):
    global MainChain;
    global PublicIP;
    data=b"";
    while True:
        package = recev.recv(4096);
        if not package:break;
        data+=package;
    NewBlock = pickle.loads(data);
    if verifyPOW(NewBlock) and ((NewBlock.preBlockHash == MainChain[len(MainChain) - 2].hash and len(MainChain) > 0) or (len(MainChain) == 1)):
        if addr[0]==PublicIP[0]:
            print("You Have Mined A New Block!");
        else:
            print("Received New Block from %s:%s and Verified!"%addr);
        print("Previous Block Hash:%s" % NewBlock.preBlockHash);
        print("Current Block Hash:%s" % NewBlock.hash);
        print("PoW:%d" % NewBlock.Nonce);
        print("PoW Hash:%s"%hasher.sha256((str(NewBlock.hash) + str(NewBlock.timeStamp) + str(NewBlock.preBlockHash)+ str(NewBlock.Nonce)).encode('utf-8')).hexdigest());
        for t in NewBlock.data:
            print("New Trade:%s pays %s %d coins at %s" % (t.source.name, t.to.name, t.amount, t.timeStamp));
        print("======================================================================");
        MainChain[len(MainChain)-1]=NewBlock;
        for t in NewBlock.data:
            try:
                TRADE_BUFFER.remove(t);
            except:
                continue;
        MainChain.append(Block(NewBlock.hash));
    else:
        print("Received Unauthorized Block!");


def BroadcastListeningProcess():
    listener=socket.socket(socket.AF_INET,socket.SOCK_STREAM);
    listener.bind((socket.gethostname(),1111));
    listener.listen();
    global SocketList;
    while True:
        recev,addr=listener.accept();
        cnt=0;
        while cnt<len(SocketList):
            if SocketList[cnt][0]==addr[0]:
                break;
            else:
                cnt+=1;
        if cnt==len(SocketList):
            continue;
        newListener=threader.Thread(target=BroadcastListener,args=(recev,addr));
        newListener.start();

def verifyPOW(self):
    result=hasher.sha256((str(self.hash) + str(self.timeStamp) + str(self.preBlockHash)+ str(self.Nonce)).encode('utf-8')).hexdigest();
    cnt = 0;
    while cnt < Difficulty:
        if result[cnt] != '0':
            break;
        else:
            cnt += 1;
    if cnt!=Difficulty:
        return False;
    else:
        return True;

def verifyTRADE(self):
    global MainChain;
    if key.decrypt(self.signature,self.source.PK) == str(self.ID).encode('utf-8'):
        return True;
    else:
        return False;

def renewSocketList():
    global SocketList;
    PingListener=socket.socket(socket.AF_INET,socket.SOCK_STREAM);
    PingListener.bind((socket.gethostname(),3314));
    PingListener.listen();
    while True:
        PingPackage,addr=PingListener.accept();
        SocketList=pickle.loads(PingPackage.recv(102400));

if __name__=="__main__":
    n = 0;
    Account = [];
    while n < 10:
        Account.append(account("No." + str(n)));
        n += 1;
    TRADE_BUFFER=[];
    MainChain = [];
    PauseFlag=True;
    PublicIP,SocketList=Register_Local.MinerRegister();
    Genesis = Block(0);
    MainChain.append(Genesis);
    print("Start at:%s" % str(Genesis.timeStamp));
    Difficulty = 6;
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);
    s.bind((socket.gethostname(),22));
    s.listen(5);
    # print('Waiting for connection...');
    mining = threader.Thread(target=MiningProcess,args=());
    mining.start();
    listening=threader.Thread(target=BroadcastListeningProcess);
    listening.start();
    renew = threader.Thread(target=renewSocketList);
    renew.start();
    TradeThread=threader.Thread(target=TradeProcess);
    TradeThread.start();
    while True:
        sock, addr = s.accept();
        if pickle.loads(sock.recv(2048)) == "10086":
            try:
                sock.send(pickle.dumps(","));
                buffer = sock.recv(2048);
                newTrade=pickle.loads(buffer);
                TRADE_BUFFER.append(pickle.loads(buffer));
            except socket.error:
                print("Break detected!");

