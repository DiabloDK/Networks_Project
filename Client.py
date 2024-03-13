import socket
import pyaudio
import sys
import pyaudio
import tkinter as tk
from tkinter import messagebox

IP=socket.gethostbyname(socket.gethostname())
PORT=5566
ADDR=(IP,PORT)
FORMAT='utf-8'
DISCONNECT_MSG = '!DISCONNECT'
BUFFER_SIZE=4096
MUSIC_FORMAT=pyaudio.paInt16
CHANNELS = 2
RATE = 44100

class MusicPlayer:
    def __init__(self,client) -> None:
        self.client=client
        self.paused=False
        self.p = pyaudio.PyAudio()
        self.stream = None

    def play_music(self):
        try:
            if not self.client:
                messagebox.showerror("Error", "Not connected to the server.")
                return

            #self.client.send(str(file_index).encode(FORMAT))

            # response = self.client.recv(BUFFER_SIZE).decode(FORMAT)
            # if response == "Invalid choice":
            #     messagebox.showerror("Error", "Invalid choice. Please select a valid index.")
            #     return

            self.paused = False

            if self.stream:
                self.stream.stop_stream()
                self.stream.close()

            self.stream = self.p.open(format=MUSIC_FORMAT,
                                      channels=CHANNELS,
                                      rate=RATE,
                                      output=True)

            while True:
                if self.paused:
                    continue

                data = self.client.recv(BUFFER_SIZE)
                if not data:
                    break
                self.stream.write(data)

            self.stream.stop_stream()
            self.stream.close()
            self.p.terminate()

            messagebox.showinfo("Playback Complete", "Audio playback completed successfully.")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def pause_music(self):
        self.paused = True

    def resume_music(self):
        self.paused = False
        
    




def music_Stream(client):
    musicList=client.recv(BUFFER_SIZE).decode(FORMAT)
    print(musicList)
    choice=input('> ')
    client.send(choice.encode())
    player = MusicPlayer(client)

    window = tk.Tk()
    window.title("Client")
    window.geometry("300x200")
    window.resizable(False, False)
    play_button = tk.Button(window, text="Play Music", command=lambda: player.play_music())
    play_button.pack(pady=10)

    pause_button = tk.Button(window, text="Pause Music", command=player.pause_music)
    pause_button.pack(pady=10)

    resume_button = tk.Button(window, text="Resume Music", command=player.resume_music)
    resume_button.pack(pady=10)

    window.mainloop()
    sys.exit(1)


def functionalities(client):
    msg=client.recv(BUFFER_SIZE).decode(FORMAT)
    print(msg)
    user_response=input("> ")
    client.send(user_response.encode(FORMAT))
    if(user_response=='1'):
        music_Stream(client)

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
        if('LOGIN SUCCESS' in msg):
            functionalities(client)

        if('FAILED' in msg or 'ALREADY' in msg or 'SUCCESS' in msg):
            continue
        user_response=''
        while len(user_response)<1:
            user_response=input("> ")
        client.send(user_response.encode(FORMAT))
        if(user_response==DISCONNECT_MSG):
            connected=False
    client.close()



if __name__ =="__main__":
    main()