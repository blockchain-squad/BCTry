import socket as socket;
import threading as thread;
import pickle as pickle;

def MinerPing():
    global MinerList;
    global connection_miner;
    while True:
        client,addr=connection_miner.accept();
        if client.recv(1024).decode('utf-8')=="10086":
            MinerList.append(addr);
            print(MinerList);
            client.send(pickle.dumps((addr, MinerList)));

def ClientPing():
    global ClientList;
    global MinerList;
    global connection_client;
    while True:
        client,addr=connection_client.accept();
        if client.recv(1024).decode('utf-8')=="10086":
            ClientList.append(addr);
            print(ClientList);
            client.send(pickle.dumps((addr, MinerList)));

def MinerPingProcess():
    global ClientList;
    global MinerList;
    while True:
        if len(MinerList)!= 0:
            for Addr in MinerList:
                PingSender = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
                try:
                    PingSender.connect((Addr[0], 3314));
                    PingSender.send(pickle.dumps(MinerList));
                    PingSender.close();
                    #print(MinerList);
                except socket.error:
                    MinerList.remove(Addr);
                    print(MinerList);

def ClientPingProcess():
    global ClientList;
    global MinerList;
    while True:
        if len(ClientList) != 0:
            for Addr in ClientList:
                PingSender = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
                try:
                    PingSender.connect((Addr[0], 3315));
                    PingSender.send(pickle.dumps(MinerList));
                    PingSender.close();
                    #print(ClientList);
                except socket.error:
                    ClientList.remove(Addr);
                    print(ClientList);

MinerList=[];
ClientList=[];
connection_miner =socket.socket(socket.AF_INET, socket.SOCK_STREAM);
connection_client=socket.socket(socket.AF_INET,socket.SOCK_STREAM);
connection_miner.bind((socket.gethostname(), 1080));
connection_client.bind((socket.gethostname(),1090));
connection_miner.listen();
connection_client.listen();
MinerPingThread=thread.Thread(target=MinerPing);
MinerPingThread.start();
ClientPingThread=thread.Thread(target=ClientPing);
ClientPingThread.start();
Miner=thread.Thread(target=MinerPingProcess);
Miner.start();
Client=thread.Thread(target=ClientPingProcess);
Client.start();

# def ListManageProcess(client:socket):
#     IPLogout=pickle.loads(client.recv(1024));
#     SocketList.remove(IPLogout);
