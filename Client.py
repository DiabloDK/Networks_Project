import socket
import threading

IP=socket.gethostbyname(socket.gethostname())
PORT=5566
ADDR=(IP,PORT)
FORMAT='utf-8'
DISCONNECT_MSG = '!DISCONNECT'
BUFFER_SIZE=2048


def main():
    client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect(ADDR)
    print(f"[CONNECTED] CLIENT CONNECTED TO SERVER AT {IP}:{PORT}")
    connected=True

    while connected:
        msg=input("> ")
        client.send(msg.encode(FORMAT))



if __name__ =="__main__":
    main()