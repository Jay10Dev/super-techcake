
from Tkinter import *
from chat import *
from Tkinter import *
from chat import *
import PIL.Image
import thread
import tkMessageBox
from tkFileDialog import askopenfilename
import os
import re

s = socket(AF_INET, SOCK_STREAM)
HOST = gethostname()
PORT = 9003
conn = ''
s.bind((HOST, PORT))
imgcounter=1
basename="image%s.png"
regex=re.compile(r"[a-zA-Z0-9_]")

def onClick():
    messageText = messageFilter(textBox.get("0.0",END)) #filter
    if "/img" in messageText :
        conn.sendall("Your partner is sending an image... /img")#do image stuff
        tkMessageBox.showinfo(title="Image Transfer", message="Click OK to Select Image")
        Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
        filename = askopenfilename(title="Browse image files",initialdir=os.getcwd()) # show an "Open" dialog box and return the path to the selected file
         
        img=PIL.Image.open(filename)
        img.show()
        conn.sendall("Received ?")
        displayLocalMessage(chatBox, messageText) #display local
        chatBox.yview(END) #auto-scroll
        textBox.delete("0.0",END) #clear the input box
    else:    
    	conn.sendall(messageText) #send over socket
        displayLocalMessage(chatBox, messageText) #display local
        chatBox.yview(END) #auto-scroll
        textBox.delete("0.0",END) #clear the input box
def onEnterButtonPressed(event):
    textBox.config(state=NORMAL)
    onClick()

def removeKeyboardFocus(event):
	textBox.config(state=DISABLED)

def openConnection():
    s.listen(2) #Listen for 1 other person
    global conn
    conn, addr = s.accept()
    getConnectionInfo(chatBox, 'Connected with: ' + str(addr) + '\n-------------------------------------')

    while 1:
	try:
            data = conn.recv(40960000) #Get data from clients
            if re.match(regex,data):
	    	displayRemoteMessage(chatBox, data)
            else:
            	
           

            	global imgcounter
            	myfile = open(basename % imgcounter, 'wb')

            
            	if not data:
            		myfile.close()
                	data="Not received"
                	break
                myfile.write(data)
                data="received"
                displayRemoteMessage(chatBox, data)
            
                    
        
        

        except:
        	getConnectionInfo(chatBox, '\n [ Your partner has disconnected ]\n [ Waiting for him to connect..] \n  ')
                openConnection()
        imgcounter+=1
         #Display on Remote Windows
        
    conn.close()

#Base Window
base = Tk()
base.title("Pychat Host")
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

#Text Input
textBox = Text(base, bd=0, bg="#F8B486",width="29", height="5", font="Helvetica")
textBox.bind("<Return>", removeKeyboardFocus)
textBox.bind("<KeyRelease-Return>", onEnterButtonPressed)

#Put everything on the window
sb.place(x=370,y=5, height=350)
chatBox.place(x=15,y=5, height=350, width=355)
sendButton.place(x=255, y=360, height=80, width=130)
textBox.place(x=15, y=360, height=80, width=250)

thread.start_new_thread(openConnection,()) # try listening again upon fail

base.mainloop() #Start the GUI Thread
