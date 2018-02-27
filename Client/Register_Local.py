import socket as socket;
import pickle as pickle;

def MinerRegister():
    connection=socket.socket(socket.AF_INET,socket.SOCK_STREAM);
    # new = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
    connection.connect(('120.77.171.176',1080));
    connection.send("10086".encode('utf-8'));
    # connection.send(pickle.dumps((True,connection.getsockname())));
    PublicIP,SocketList=pickle.loads(connection.recv(102400));
    connection.close();
    return PublicIP,SocketList;

def ClientRegister():
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
    # new = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
    connection.connect(('120.77.171.176', 1090));
    connection.send("10086".encode('utf-8'));
    # connection.send(pickle.dumps((True,connection.getsockname())));
    PublicIP, SocketList = pickle.loads(connection.recv(102400));
    connection.close();
    return PublicIP, SocketList;