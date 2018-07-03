# -*- coding: utf-8 -*-

from Tkinter import *
from chat import *
import PIL.Image
import thread
import tkMessageBox
from tkFileDialog import askopenfilename
import os


HOST = gethostname()
PORT = 9003
s = socket(AF_INET, SOCK_STREAM)

def onClick():
    messageText = messageFilter(textBox.get("0.0",END)) #filter

    if "/shrug" in messageText :
        messageText =  "¯\_(ツ)_/¯"
        s.send(messageText)

    elif "/creep" in messageText :
        messageText = "( ͡° ͜ʖ ͡°)"
        s.send(messageText) 
    elif "/smile" in messageText :
        messageText = "•ᴗ•"
        s.send(messageText) 
    elif "/what" in messageText :
        messageText = "ლ(ಠ_ಠლ)"
        s.send(messageText)
    
        
    else:
        s.send(messageText)

    displayLocalMessage(chatBox, messageText)
    chatBox.yview(END)
    textBox.delete("0.0",END) 
def onImageClick():
	#s.send("IMAGE")#do image stuff
       # settings.num=1
        
        tkMessageBox.showinfo(title="Image Transfer", message="Click OK to Select Image")
        Tk().withdraw() 
        try:
 
        	filename = askopenfilename(title="Browse image files",initialdir=os.getcwd())
    		myfile = open(filename, 'rb')
    		bytes = myfile.read()
    		size = len(bytes)
                #sock.sendall("SIZE %s" % size)
                message="SENDING"
    		s.sendall(bytes)
                
        finally:
    		myfile.close()
        displayLocalMessage(chatBox, message)
        chatBox.yview(END) 
        textBox.delete("0.0",END)

def onEnterButtonPressed(event):
    textBox.config(state=NORMAL)
    onClick()

def removeKeyboardFocus(event):
	textBox.config(state=DISABLED)

def ReceiveData():
    try:
        s.connect((HOST, PORT))
        getConnectionInfo(chatBox, '[ Connected! ]\n-------------------------------------')
    except:
        getConnectionInfo(chatBox, '[ Cannot connect ]')
        return

    while 1:
        try:
            data = s.recv(1024)
        except:
            getConnectionInfo(chatBox, '\n [ Your partner left.] \n')
            break
        if data != '':
            displayRemoteMessage(chatBox, data)

        else:
            getConnectionInfo(chatBox, '\n [ Your partner left. ] \n')
            break
    s.close()

#Base Window
base = Tk()
base.title("Pychat Client")
base.geometry("400x450")
base.resizable(width=FALSE, height=FALSE)
base.configure(bg="#716664")

#Chat
chatBox = Text(base, bd=0, bg="#689099", height="8", width="20", font="Helvetica",)
chatBox.insert(END, "Waiting for your partner to connect..\n")
chatBox.config(state=DISABLED)
sb = Scrollbar(base, command=chatBox.yview, bg = "#34495e")
chatBox['yscrollcommand'] = sb.set

#Send Button
sendButton = Button(base, font="Helvetica", text="SEND", width="50", height=5,
                    bd=0, bg="#BDE096", activebackground="#BDE096", justify="center",
                    command=onClick)
imageButton=Button(base, font="Helvetica", text="IMAGE", width="50", height=10,
                    bd=0, bg="#BDE096", activebackground="#BDE096", justify="center",
                    command=onImageClick)
#Text Input
textBox = Text(base, bd=0, bg="#F8B486",width="20", height="5", font="Helvetica")
textBox.bind("<Return>", removeKeyboardFocus)
textBox.bind("<KeyRelease-Return>", onEnterButtonPressed)

#Put everything on the window
sb.place(x=370,y=5, height=350)
chatBox.place(x=15,y=5, height=350, width=355)
sendButton.place(x=310, y=360, height=80, width=80)
imageButton.place(x=15, y=360, height=80, width=80)
textBox.place(x=95, y=360, height=80, width=215)

thread.start_new_thread(ReceiveData,())
base.mainloop()
