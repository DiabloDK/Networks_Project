import socket
import threading

IP=socket.gethostbyname(socket.gethostname())
PORT=5566
ADDR=(IP,PORT)
FORMAT='utf-8'
DISCONNECT_MSG = '!DISCONNECT'
BUFFER_SIZE=2048

def handle_client(conn,addr):
    print(f"[NEW CONNECTION] {addr} connected")
    connected=True
    while connected:
        cmd=conn.recv(BUFFER_SIZE).decode(FORMAT)
        print(cmd)
    conn.close()


def main():
    print('[STARTING SERVER] THE SERVER IS STARTING---')
    server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f"[LISTENING] SERVER LISTENING ON {IP}:{PORT}")
    while True:
        conn,addr=server.accept()
        thread=threading.Thread(target=handle_client,args=(conn,addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS]{threading.activeCount()-1}")

if __name__ =="__main__":
    main()