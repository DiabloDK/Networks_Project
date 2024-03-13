import socket
import threading
import os

MUSIC_FOLDER = 'Music'
IP=socket.gethostbyname(socket.gethostname())
PORT=5566
ADDR=(IP,PORT)
FORMAT='utf-8'
DISCONNECT_MSG = '!DISCONNECT'
BUFFER_SIZE=4096

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
        msg=conn.recv(BUFFER_SIZE).decode(FORMAT).lower()
        if(msg=="register"):
            if register(conn):
                continue
        elif(msg=="login"):
            if login(conn):
                conn.send("[SERVER] LOGIN SUCCESS".encode(FORMAT))
                inside_functions(conn)

            else:
                conn.send("[SERVER] LOGIN FAILED".encode(FORMAT))
        elif(msg.upper()==DISCONNECT_MSG):
            connected=False
        else:
            continue

    conn.close()

def music_Stream(conn):
    music_files = os.listdir(MUSIC_FOLDER)
    music_list = '\n'.join([f"{index+1}. {file}" for index, file in enumerate(music_files)])
    conn.send(music_list.encode(FORMAT))
    client_choice = conn.recv(BUFFER_SIZE).decode(FORMAT)
    print(client_choice,type(client_choice))
    if client_choice.isdigit() and int(client_choice) <= len(music_files):
        # conn.send("Valid choice".encode(FORMAT))
        chosen_index = int(client_choice) - 1
        chosen_file = music_files[chosen_index]
        file_path = os.path.join(MUSIC_FOLDER, chosen_file)
        print("HOLA")
        with open(file_path, 'rb') as file:
            while True:
                chunk = file.read(BUFFER_SIZE)
                if not chunk:
                    break
                conn.send(chunk)
    else:
        conn.send("Invalid choice".encode(FORMAT))


def inside_functions(conn):
    conn.send("[SERVER]CHOOSE YOUR ENTERTAINMENT\n1.MUSIC STREAMING\n".encode(FORMAT))
    choice=conn.recv(BUFFER_SIZE).decode()
    if(choice=='1'):
        music_Stream(conn)

    

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