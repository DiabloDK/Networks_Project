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
    msg=client.recv(BUFFER_SIZE).decode(FORMAT).strip().lower()
    print(msg)
    connected=True

    while connected:
        msg=client.recv(BUFFER_SIZE).decode(FORMAT)
        print(msg)
        if('FAILED' in msg):
            continue
        user_response=''
        while len(user_response)<1:
            user_response=input("> ")
        client.send(user_response.encode(FORMAT))
        if(msg==DISCONNECT_MSG):
            connected=False
    client.close()



if __name__ =="__main__":
    main()