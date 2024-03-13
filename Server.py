import socket
import json
import threading

IP=socket.gethostbyname(socket.gethostname())
PORT=5566
ADDR=(IP,PORT)
FORMAT='utf-8'
DISCONNECT_MSG = '!DISCONNECT'
BUFFER_SIZE=2048

USER_DATABASE_FILE = 'user_database.txt'


def read_user_database():
    user_database={}
    with open(USER_DATABASE_FILE, 'r') as file:
        for line in file.readlines():
            username, password = line.strip().split(':')
            user_database[username] = password
    return user_database


def write_user_database(user_database):
    with open(USER_DATABASE_FILE, 'w') as file:
        for username, password in user_database.items():
            file.write(f"{username}:{password}\n")


def authenticate(username,password):
    user_database=read_user_database()
    if username in user_database:
        if password==user_database[username]:
            return True
    return False

def login(conn):
    conn.send("[SERVER] LOGIN AS : ".encode(FORMAT))
    username=conn.recv(BUFFER_SIZE).decode(FORMAT).strip()
    conn.send("[SERVER] PASSWORD : ".encode(FORMAT))
    password=conn.recv(BUFFER_SIZE).decode(FORMAT).strip()
    if authenticate(username,password):
        return True
    return False
    




def register(conn):
    conn.send("[SERVER] ENTER USERNAME : ".encode(FORMAT))
    username=conn.recv(BUFFER_SIZE).decode(FORMAT)
    user_database=read_user_database()
    if username in user_database:
        conn.send("[SERVER] USERNAME ALREADY EXISTS".encode(FORMAT))
        return False
    conn.send("[SERVER] ENTER PASSWORD : ".encode(FORMAT))
    password=conn.recv(BUFFER_SIZE).decode(FORMAT).strip()
    user_database[username]=password
    conn.send(f"[RESGISTERED] NEW USER \"{username}\" IS SUCCESSFULLY REGISTERED".encode(FORMAT))
    write_user_database(user_database)
    return True

def handle_client(conn,addr):
    print(f"[NEW CONNECTION] {addr} connected")
    connected=True
    msg="\t\t\t===MULTIMEDIA SERVER==="
    conn.send(msg.encode(FORMAT))
    while connected:
        conn.send("[SERVER] LOGIN/REGISTER : ".encode(FORMAT))
        msg=conn.recv(BUFFER_SIZE).decode(FORMAT)
        print(msg)
        if(msg=="register"):
            if register(conn):
                continue
        elif(msg=="login"):
            if login(conn):
                connected=False
            else:
                conn.send("[SERVER] LOGIN FAILED".encode(FORMAT))
        elif(msg==DISCONNECT_MSG):
            connected=False
        else:
            continue
    print(msg)
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