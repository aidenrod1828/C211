from curses import window
import socket
from threading import Thread
from tkinter import *
from tkinter import ttk
import ftplib
from ftplib import FTP
import os
import time
import ntpath 

from tkinter import filedialog
from pathlib import Path

from playsound import playsound
import pygame
from pygame import mixer


IP_ADDRESS = '127.0.0.1'
PORT = 8050
SERVER = None
BUFFER_SIZE = 4096
song_counter=0
song_selected=""

name = None
listbox =  None
textarea= None
infoLabel = None
text_message = None
filePathLabel = None

def setup():
    global SERVER
    global PORT
    global IP_ADDRESS

    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.connect((IP_ADDRESS, PORT))

    musicWindow()
setup()

def musicWindow():
    window=Tk()
    window.title('Music Window')
    window.geometry("300x300")
    window.configure(bg='LightSkyBlue')

    selectlabel = Label(window, text= "Select Song", bg='LightSkyBlue', font = ("Calibri",8))
    selectlabel.place(x=2, y=1)

    listbox = Listbox(window,height = 10,width = 39,activestyle = 'dotbox', bg='LightSkyBlue', borderwidth=2,  font = ("Calibri",10))
    listbox.place(x=10, y=18)

    scrollbar1 = Scrollbar(listbox)
    scrollbar1.place(relheight = 1,relx = 1)
    scrollbar1.config(command = listbox.yview)

    PlayButton=Button(window, text="Play", width=10, bd=1,bg='SkyBlue', font = ("Calibri",10))
    PlayButton.place(x=30,y=200)

    Stop=Button(window, text="Play", width=10, bd=1,bg='SkyBlue', font = ("Calibri",10))
    Stop.place(x=200,y=200)

    Upload=Button(window, text="Upload", width=10, bd=1,bg='SkyBlue', font = ("Calibri",10))
    Upload.place(x=10,y=250)
    
    Download=Button(window, text="Download", width=10, bd=1,bg='SkyBlue', font = ("Calibri",10))
    Download.place(x=200,y=250)

    infoLabel = Label(window, text= "", fg="blue", font = ("Calibri", 8))
    infoLabel.place(x=4, y=280)

    ResumeButton=Button(window, text="Resume", width=10, bd=1,bg='SkyBlue', font = ("Calibri",10))
    ResumeButton.place(x=30,y=200)

    PauseButton=Button(window, text="Pause", width=10, bd=1,bg='SkyBlue', font = ("Calibri",10))
    PauseButton.place(x=30,y=200)

    window.mainloop()

for file in os.listdir('shared_files'):
    filename = os.fsdecode(file)
    listbox.insert(song_counter, filename)
    song_counter = song_counter + 1

def play():
    global song_selected
    song_selected=listbox.get(ANCHOR)

    pygame
    mixer.init()
    mixer.music.load('shared_files/'+song_selected)
    mixer.music.play()
    if(song_selected !=""):
        infoLabel.configure(text="Now Playing: " + song_selected)
    else:
        infoLabel.configure(text="")

def stop():
    global song_selected
    pygame
    mixer.init()
    mixer.music.load('shared_files/'+song_selected)
    mixer.music.pause()
    infoLabel.configure(text="") 

def resume():
    global song_selected
    mixer.init()
    mixer.music.load('shared_files/'+song_selected)
    mixer.music.play()

def pause():
    global song_selected
    pygame
    mixer.init()
    mixer.music.load('shared_files/'+song_selected)
    mixer.music.pause()

def browseFiles():
    global listbox
    global song_counter
    global filePathLabel

    try:
        filename=filedialog.askopenfilename()
        HOSTNAME="127.0.0.1"
        USERNAME="lftpd"
        PASSWORD="lftpd"

        ftp_server=FTP(HOSTNAME, USERNAME, PASSWORD)
        ftp_server.encoding = "utf-8"
        ftp_server.cwd('shared_files')
        fname=ntpath.basename(filename)
        with open(filename, 'rb') as file:
            ftp_server.storbinary(f"STOR {fname}", file)
        ftp_server.dir()
        ftp_server.quit()
        
    except FileNotFoundError:
        print("Cancel Button Pressed")