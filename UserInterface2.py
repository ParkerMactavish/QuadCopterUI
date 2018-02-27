import tkinter.ttk as ttk			#ttk
import tkinter as tk				#tkinter
import collections					#ordered dictionary
from tkinter import messagebox		#messagebox
import os.path						#check file existance

import socket						#UDP connect
import time							#receiving delay
import datetime						#for test

import threading					#multi threading 
import os							#control command line

#define IP and Port
IP="192.168.1.1"
Port=239

#inside config and flag
UIActiveFlag=True
ButtonAllignment="center"
LabelAllignment="center"
EntryAllignment="center"
RadioButtonAllignment="center"
CheckButtonAllignment="center"


#wifi connection check
Win = tk.Tk()
if (os.system("netsh wlan connect \"Quadcopter\""))==1:
	messagebox.showwarning("Quadcopter", "Connection Error:\nCheck the connection between wi-fi \"Quadcopter\"")

Win.deiconify()
	
#Creating Notebook on Win
NoteBook=ttk.Notebook(Win)
NoteBook.pack()

#Creating Frames with the sequence of buttons, space, uppertable, lowertable, radiobutton, and URL
Tab1=ttk.Frame(NoteBook)
Tab2=ttk.Frame(NoteBook)
NoteBook.add(Tab1, text="Parameter")
NoteBook.add(Tab2, text="Data")
ConfigEntryFrame=ttk.Frame(Tab1, height=485)
DataPresentationFrame=ttk.Frame(Tab1, height=485)


ButtonFrame=ttk.Frame(ConfigEntryFrame, height=30)#frame for buttons
EmptyFrame1=ttk.Frame(ConfigEntryFrame, height=5)#frame for the space between buttons and cells
LabelFrame=ttk.Frame(ConfigEntryFrame, height=30)#frame for the labels
UpperFrameList = []#list of upper frames
for x in range(8):UpperFrameList.append(ttk.Frame(ConfigEntryFrame, height=30))
EmptyFrame2=ttk.Frame(ConfigEntryFrame, height=5)#frame for the space between upper and lower cells
LowerFrameList = []#list of lower frame
for x in range(5):LowerFrameList.append(ttk.Frame(ConfigEntryFrame, height=30))
RadioButtonFrame=ttk.Frame(ConfigEntryFrame, height=40)
CheckButtonFrame1=ttk.Frame(ConfigEntryFrame, height=40)
CheckButtonFrame2=ttk.Frame(ConfigEntryFrame, height=40)






UpperCellValues=[[1,1,0,0],[1,1,0,0],[1.5,1,0,0],[0, 0, 0, 0],[1.5,0,0,0.01], [1.5,0,0,0.01], [1.5,0,0,0.01], [0,0,0,0]]
LowerCellValues=[1000, -4, 8, 2.5, 70]
ThrottleSide=tk.StringVar()
ThrottleSide.set("L")
CheckButtonValueList=[]
for x in range(11):
	CheckButtonValueList.append(tk.IntVar())
	CheckButtonValueList[x].set(1)
	
ButtonList=[]#list for buttons
ButtonTexts=["LOCK", "UNLOCK", "SYNC", "ALTHOLD"]#texts for buttons
LabelList=[]#list for labels
LabelTexts=["PID", "P", "I", "I Limit", "D"]#texts for labels
UpperCells=collections.OrderedDict([("Attitude Roll",[]), ("Attitude Pitch",[]), ("Attitude Yaw",[]), ("Attitude Height", []),
                                    ("Rate Roll",[]), ("Rate Pitch",[]), ("Rate Yaw",[]), ("Rate Height",[])])#texts and entries for uppercells
LowerLabels=["Angular Velocity Limit","Roll Anfular Calbration","Pitch Angular Calbration","Stick Gain","Max Throttle Percentage(%)"]
LowerLabelList=[]
LowerCellList=[]
RadioButtonList=[]

CheckButtonList=[]
CheckButtonLabel=["pitch", "roll", "yaw", "atmosphere", "height", "throttle", "rot1", "rot2", "rot3", "rot4", "voltage"]

#Opening config file
FilExst=os.path.isfile("config.txt")
Buffer=False
TmpFile=None
if FilExst:
    TmpFile=open("config.txt", "r+")
    Buffer = TmpFile.readline()
	
if bool(Buffer):
    TmpFile.seek(0,0)
    for x in range(len(UpperCellValues)):
        for y in range(len(UpperCellValues[x])):
            UpperCellValues[x][y]=TmpFile.readline()

    for x in range(len(LowerCellValues)):
        LowerCellValues[x]=TmpFile.readline()

    TmpChar=TmpFile.readline()
    TmpChar=TmpChar[:-1]
    ThrottleSide.set(TmpChar)
	
    for x in range(11):
        TmpChar=TmpFile.readline()
        TmpChar=TmpChar[:-1]
        CheckButtonValueList[x].set(int(TmpChar))
        #if data exists, then get it from file

else:
    TmpFile = open("config.txt", "w")
    for x in range(len(UpperCellValues)):
        for y in range(len(UpperCellValues[x])):
            TmpFile.write(str(UpperCellValues[x][y])+"\n")

    for x in range(len(LowerCellValues)):
        TmpFile.write(str(LowerCellValues[x])+"\n")

    TmpFile.write(ThrottleSide.get()+"\n")

    for x in range(11):
        TmpFile.write(str(CheckButtonValueList[x].get())+"\n")
	
        #if there's no data, then store the defalt to file
TmpFile.close()




#Create a file for data
Time=datetime.datetime
file=open(str(Time.now().month).zfill(2)+"."+str(Time.now().day)+" "+str(Time.now().hour)+"-"+str(Time.now().minute)+"-"+str(Time.now().second)+".txt", "w")

TmpStr=""
for x in range(len(CheckButtonLabel)):
	if CheckButtonValueList[x].get()==1:
		TmpStr+=CheckButtonLabel[x]+","
		
TmpStr=TmpStr[:-1]
file.write(TmpStr)



#UDP sends data
def SendData(OriginalData=""):
	if len(OriginalData)==0:
		Data="@"
		for x in range(len(UpperCellValues)):
			for y in range(len(UpperCellValues[x])):
				Data+=str(UpperCellValues[x][y])
				Data=Data[:-1]
				Data+=":"
		Data=Data[:-1]
		Data+="#"
	else:
		Data=OriginalData
		
	DstAddr=(IP, Port)
	SendSocketUdp=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	try:
		SendSocketUdp.sendto(Data.encode(), DstAddr)
		print(Data)
	except:
		messagebox.showwarning("Quad Copter","Target IP not Available")

SendData()


#UDP send/receive thread
class RecvDataThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)        
        RecSocketUdp=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        HostAddr=('', Port)
        try:	
            RecSocketUdp.bind(HostAddr)
        except:
            messagebox.showwarning("Quadcopter", "Host Address not available")
    def run(self):
        while UIActiveFlag:
            try:
                recv_data()
            except:
                None
                print(1)		
            SendData("@2:0:0.00:0.00:0.0#")
            time.sleep(0.01)
			
#

def recv_data():
    print("In receiving thread")
    Addr=('', Port)
    data=b''
    data, (Addr, Port)=RecSocketUdp.recvfrom(512)
    if len(data) > 0:
        print(data)
        DevidedData=[]
		
	#print(time.ctime())


	
#Panel Appearance
Win.title("Quadcopter GUI")
Win.geometry("1200x485")
Win.resizable(0, 0)


#Styling
ttk.Style().configure("TButton", padding=5, background="#ccc",  anchor=ButtonAllignment)
ttk.Style().configure("TLabel", padding=3)
ttk.Style().configure("TEntry", padding=3)
ttk.Style().configure("TRadiobutton", padding=3, anchor=RadioButtonAllignment)
ttk.Style().configure("TCheckbutton", padding=3, anchor=CheckButtonAllignment)




#ButtonEvents
def get_value(entry):
    var = entry.get()
    return var

def Sync_Button():
    cnt=0
    TmpFile = open("config.txt", "w")
    for x in UpperCells:
        for y in range(1, len(UpperCells[x])):
            UpperCellValues[cnt][y-1]=get_value(UpperCells[x][y])
            TmpStr=str(UpperCellValues[cnt][y-1])
            if TmpStr[-1]=='\n':
                TmpStr=TmpStr[:len(TmpStr)-1]
            TmpFile.write(TmpStr+"\n")
        cnt+=1

    for x in range(len(LowerCellList)):
        LowerCellValues[x]=get_value(LowerCellList[x])
        TmpStr=str(LowerCellValues[x])
        if TmpStr[-1] == '\n':
            TmpStr = TmpStr[:len(TmpStr) - 1]
        TmpFile.write(TmpStr+"\n")

    TmpFile.write(ThrottleSide.get()+"\n")
	
    for x in range(11):
        TmpFile.write(str(CheckButtonValueList[x].get())+"\n")
	
    messagebox.showwarning("Quad Copter","Arguments have been saved")
	
    SendData()
	
    TmpFile.close()
	
	
	#Create a file for data when sychronizing
    global file
    file.close()
    Time=datetime.datetime
    file=open(str(Time.now().month).zfill(2)+"."+str(Time.now().day)+" "+str(Time.now().hour)+"-"+str(Time.now().minute)+"-"+str(Time.now().second)+".txt", "w")
	
    TmpStr=""
    for x in range(len(CheckButtonLabel)):
        if CheckButtonValueList[x].get()==1:
            TmpStr+=CheckButtonLabel[x]+","
    TmpStr=TmpStr[:-1]
    file.write(TmpStr)
	
	

def Lock_Button():
    SendData("@1:0#")
    messagebox.showwarning("Quadcopter", "Quadcopter Locked")

def Unlock_Button():
    SendData("@1:1#")
    messagebox.showwarning("Quadcopter", "Quadcopter Unlocked")

def AltHold_Button():
    return 0
ButtonEvents=[Lock_Button, Unlock_Button, Sync_Button, AltHold_Button]



#Buttons
for x in range(len(ButtonTexts)):
    ButtonList.append((ttk.Button(ButtonFrame, text=ButtonTexts[x], style="TButton", width=19, command=ButtonEvents[x])))

#First row for labels
for x in range(len(LabelTexts)):
    LabelList.append((ttk.Label(LabelFrame, text=LabelTexts[x], style="TLabel", width=16, relief="groove",
    anchor=LabelAllignment)))

#all UpperCells
cnt=0
for x in UpperCells:
    UpperCells[x].append((ttk.Label(UpperFrameList[cnt], text=x, style="TLabel", width=16, relief="groove", anchor=LabelAllignment)))
    for y in range(len(LabelTexts)-1):
        UpperCells[x].append(ttk.Entry(UpperFrameList[cnt], style="TEntry", width=16, justify=EntryAllignment))
        UpperCells[x][y+1].insert("end", UpperCellValues[cnt][y])
    cnt += 1

#all LowerCells
for x in range(len(LowerLabels)):
    LowerLabelList.append(ttk.Label(LowerFrameList[x], text=LowerLabels[x], style="TLabel", width=42, relief="groove", anchor=LabelAllignment))
    LowerCellList.append(ttk.Entry(LowerFrameList[x], style="TEntry", width=42, justify=EntryAllignment))
    LowerCellList[x].insert("end", LowerCellValues[x])

#radio button for throttle side
RadioButtonList.append(ttk.Label(RadioButtonFrame, text="Throttle Side", style="TLabel", width=42, relief="groove", anchor=LabelAllignment))
RadioButtonList.append(ttk.Radiobutton(RadioButtonFrame,style="TRadiobutton", text="Left", variable=ThrottleSide, value="L", width=18))
RadioButtonList.append(ttk.Radiobutton(RadioButtonFrame,style="TRadiobutton", text="Right", variable=ThrottleSide, value="R",width=18))
if "L" == ThrottleSide.get(): RadioButtonList[1].invoke()
else:RadioButtonList[2].invoke()

#check button for data retrieving
for x in range(11):
    if x<5:
	    CheckButtonList.append(ttk.Checkbutton(CheckButtonFrame1, text=CheckButtonLabel[x], variable=CheckButtonValueList[x], onvalue=1, offvalue=0, width=10))
    else:
        CheckButtonList.append(ttk.Checkbutton(CheckButtonFrame2, text=CheckButtonLabel[x], variable=CheckButtonValueList[x], onvalue=1, offvalue=0, width=10))
	
		
#Packing Stage
ConfigEntryFrame.pack(side="left")
ButtonFrame.pack()
EmptyFrame1.pack()
LabelFrame.pack()
for i in range(len(UpperFrameList)): UpperFrameList[i].pack()#packing upper frames

for x in range(len(LowerFrameList)):LowerFrameList[x].pack()#pakcing lower frames

RadioButtonFrame.pack()


for x in range(len(ButtonList)): ButtonList[x].pack(side="left")#packing buttons

for x in range(len(LabelList)): LabelList[x].pack(side="left")#packing labels

for x in UpperCells:
    for y in range(len(UpperCells[x])):
        UpperCells[x][y].pack(side="left")#packing UpperCells

for x in range(len(LowerFrameList)):
    LowerLabelList[x].pack(side="left")
    LowerCellList[x].pack(side="left")

for x in range(len(RadioButtonList)):
    RadioButtonList[x].pack(side="left")
	
CheckButtonFrame1.pack()
CheckButtonFrame2.pack()
for x in range(len(CheckButtonLabel)):
	CheckButtonList[x].pack(side="left")

# create a new thread
thread1=RecvDataThread()
# start a new thread
thread1.daemon=True
thread1.start()
Win.mainloop()
UIActiveFlag=False
thread1.join()


