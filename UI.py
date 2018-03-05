from tkinter.ttk import Label, Button, Checkbutton, Entry, Radiobutton, Notebook, Frame
from tkinter import Tk, Canvas, messagebox, StringVar, IntVar
import tkinter as tk
import tkinter.ttk as ttk

import collections
import os.path

import socket
import time
import datetime

import threading
import os

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def Button_Trig_Send(Data, Msg):
	TmpThread=Button_Send_Data_Thread(Data, Msg)
	TmpThread.start()


def Send_Data(Data):
	global Address
	global Socket
	try:
		Socket.sendto(Data.encode(), Address)
		print(Data)
	except:
		print("Debug Send Data")


def Recieve_Data():
	global Address
	global Socket
	RecAddr=('', Address[1])
	data=b''
	try:
		Socket.bind(RecAddr)
	except:
		print("Debug Socket Bind")
	
	try:
		Socket.settimeout(3.0)
		data, (RecAddr, Address[1])=Socket.recvfrom(512)
	except:		
		print("Debug Recv Data")
	return data.decode()

	
		
def Open_Config(mode="r+"):
	if os.path.isfile("config.txt")==False:
		ConfigFile=open("config.txt", "w")
		return {"FileExist":False, "File":ConfigFile}
	elif mode == "r+":
		ConfigFile=open("config.txt", mode)
		return {"FileExist":True, "File":ConfigFile}
	elif mode == "w":
		ConfigFile=open("config.txt", mode)
		return {"FileExist":True, "File":ConfigFile}

		
class Connect_Wifi_Thread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
	def run(self):
		global Flag			
		if (os.system("netsh wlan connect \"Quadcopter\""))==1:
			messagebox.showwarning("Quadcopter", "Connection Error:\nCheck the connection between wi-fi \"Quadcopter\"")
		else:Flag["Connected"]=True	
			
		while Flag["Connected"]==False and Flag["UIActive"]==True:
			time.sleep(1)
			if (os.system("netsh wlan connect \"Quadcopter\""))==0:	
				messagebox.showinfo("Quadcopter", "Regain Connection with Quad Copter")
				Flag["Connected"]=True
		print("Exit Connecting Thread")
		
		
			
class Receive_Data_Thread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
	def run(self):
		global DataFile
		global UI1
		global Flag
		while Flag["UIActive"]:
			Data=Recieve_Data()
			if len(Data)>2:
				Data=Data[1:-1]
				Data.split(":")
				Flag["UDP"]=True
			else:Flag["UDP"]=False
			
			
			if len(Data)==len(UI1.DataPresDict):
				if Flag["DataPres"]!=UI1.RowCounter-1:
					TmpCnt=0
					for x in UI1.DataPresDict:
						UI1.DataPresDict[x][2][Flag["DataPres"]].set(Data[TmpCnt])
						TmpCnt+=1
						
					Flag["DataPres"]+=1
					
				else:
					TmpCnt=0
					for x in UI1.DataPresDict:
						for y in range(Flag["DataPres"]-2):
							UI1.DataPresDict[x][2][y].set(UI1.DataPresDict[x][2][y+1].get())
						UI1.DataPresDict[x][2][Flag["DataPres"]-1].set(Data[TmpCnt])
						TmpCnt+=1
			
			
			if Flag["Sync"]==False and len(Data)==11:				
				CheckButtonCount=0
				TmpStr=''
				for x in UI1.CheckButtonDict:
					if UI1.CheckButtonDict[x][1]==1:
						TmpStr+=Data[CheckButtonCount]+'\t'
					CheckButtonCount+=1
				TmpStr+='\n'
				DataFile.write(TmpStr)
		print("Exit Receiving Thread")
		
			
class Button_Send_Data_Thread(threading.Thread):
	def __init__(self, Data, Msg):
		threading.Thread.__init__(self)
		self.Data=Data
		self.TmpTime=time.monotonic()
		self.ContinueFlag=True
		self.Msg=Msg
		
	def run(self):
		self.TimeOutDuration=3
		while self.ContinueFlag and time.monotonic()-self.TmpTime<self.TimeOutDuration:
			for x in range(len(self.Data)):
				Send_Data(self.Data[x])
			self.Ack=Recieve_Data()
			print(self.Ack)
			if self.Ack=="@2@":self.ContinueFlag=False
		
		if self.ContinueFlag:messagebox.showwarning("Quadcopter", "Timed Out, Check UDP Connection")
		else: messagebox.showinfo("Quadcopter", self.Msg)
		
	

class UI:
	def __init__(self, master):		
		self.Allignment={"Button": "center", "Label": "center", "Entry": "center", "RadioButton": "center", "CheckButton": "center"}
		
		#Panel Appearance
		master.title("Quadcopter GUI")
		master.grid_rowconfigure(0, weight=1)
		master.grid_columnconfigure(0, weight=1)
		
		global DataFile
		
		#Styling
		ttk.Style().configure("TButton", padding=5, background="#ccc",  anchor=self.Allignment["Button"])
		ttk.Style().configure("TLabel", padding=3)
		ttk.Style().configure("TEntry", padding=3)
		ttk.Style().configure("TRadiobutton", padding=3, anchor=self.Allignment["RadioButton"])
		ttk.Style().configure("TCheckbutton", padding=3, anchor=self.Allignment["CheckButton"])


		#Creating Notebook on master
		self.NoteBook=Notebook(master)
		self.NoteBook.grid(sticky="NEWS")

		#Creating Frames on Tabs
		self.ConfigTab=Frame(self.NoteBook)
		self.ControlTab=Frame(self.NoteBook)
		self.NoteBook.add(self.ConfigTab, text="Configs")
		self.NoteBook.add(self.ControlTab, text="Controls")



		#Creating List from widgets
		self.ButtonDict=collections.OrderedDict([("Lock", [self.Lock_Button]), ("Unlock", [self.Unlock_Button]), ("Sync", [self.Sync_Button]), ("HoldAlt", [self.HoldAlt_Button]), ("UnholdAlt", [self.UnholdAlt_Button])])#first for functions, second for buttons

		
		
		self.UpperLabelDict=collections.OrderedDict([("PID", []), ("P", []), ("I", []), ("I Limit", []), ("D", [])])#first for widget

		
		
		self.UpperCells=collections.OrderedDict([("Attitude Roll",[[], ["1", "1", "0", "0"]]), ("Attitude Pitch",[[], ["1", "1", "0", "0"]]), ("Attitude Yaw",[[], ["1.5", "1", "0", "0"]]), ("Attitude Height", [[], ["1", "0", "0", "0"]]), ("Rate Roll",[[], ["1.5", "0", "0", "0"]]), ("Rate Pitch",[[], ["1.5", "0", "0", "0.01"]]), ("Rate Yaw",[[], ["1.5", "0", "0", "0.01"]]), ("Rate Height",[[], ["1", "0", "0", "0"]])])#first list for entries, second list for values

		
		
		self.LowerDict=collections.OrderedDict([("Angular Velocity Limit", [[], "1000"]), ("Roll Angular Calibration", [[], "-4"]), ("Pitch Angular Calibration", [[], "8"]), ("Stick Gain", [[], "2.5"]), ("Max Throttle Percentage", [[], "70"])])#first list for labels and entries, second value for values

		
		
		self.ThrottleRow=[]#first for StrVar, second for widgets
		self.ThrottleRow.append(StringVar())
		self.ThrottleRow[0].set("L")

		
		
		self.CheckButtonDict=collections.OrderedDict([("pitch", []), ("roll", []), ("yaw", []), ("atm", []), ("height", []), ("throt", []), ("rot1", []), ("rot2", []), ("rot3", []), ("rot4", []), ("volt", [])])
		#first for int var, second for buffer int, third for check button
		for x in self.CheckButtonDict:
			self.CheckButtonDict[x].append(IntVar())
			self.CheckButtonDict[x][0].set(0)
			self.CheckButtonDict[x].append(self.CheckButtonDict[x][0].get())
		

		if(Open_Config()["FileExist"]):
			self.Read_File(Open_Config()["File"])		
		else:
			self.Save_File(Open_Config()["File"])
		
		for x in self.Get_Items():
			DataFile.write(x+"\t")
		
		
		
		
		self.DataPresDict=collections.OrderedDict([("pitch", [[], [], []]), ("roll", [[], [], []]), ("yaw", [[], [], []]), ("atm", [[], [], []]), ("height", [[], [], []]), ("throt", [[], [], []]), ("rot1", [[], [], []]), ("rot2", [[], [], []]), ("rot3", [[], [], []]), ("rot4", [[], [], []]), ("volt", [[], [], []])])
		#first for label, second for following labels third for int var
		
		for x in self.DataPresDict:
			for y in range(18):
				self.DataPresDict[x][2].append(IntVar(0))
					
		
		self.ThrottleCanvas=Canvas(self.ControlTab, width=200, height=500, relief="groove", bg="#fff", bd=3)
		self.ThrottleCanvas.bind('<B1-Motion>', self.Get_Throttle)
		self.ThrottleCanvas.bind('<ButtonRelease-1>', self.Reset_Throttle)
		self.ThrottleCanvas.bind('<Key>', self.Get_Direction)
		self.ThrottleBall=self.ThrottleCanvas.create_oval(50, 400, 150, 500, fill="blue", tag='Ball')
		self.ThrottleCanvas.grid(column=0, row=0, columnspan=2)
		self.ThrottleBallPos={'Origin':[100, 450], 'Current':[100, 450]}
		
		
		
		self.DataCanvasBuffer=[[], [], [], [], [], [], [], [], [], [], [], []]
		
		
		self.DataFigure=Figure(figsize=(11, 5), dpi=100)
		for x in range(len(self.DataCanvasBuffer)-1):
			self.DataFigure.add_subplot(111).plot(self.DataCanvasBuffer[0], self.DataCanvasBuffer[x+1])
			
		self.DataCanvas = FigureCanvasTkAgg(self.DataFigure, self.ControlTab)
		self.DataCanvas.show()
		self.DataCanvas.get_tk_widget().grid(column=2, row=0, rowspan=5)
		
		
		
		self.ControlPres={"Throttle":[], "Roll":[], "Pitch":[], "Yaw":[]}
		RowCounter=1
		for x in self.ControlPres:
			self.ControlPres[x].append(StringVar())
			self.ControlPres[x][0].set("0")
			self.ControlPres[x].append(Label(self.ControlTab, text=x, style="TLabel", relief="groove", anchor=self.Allignment["Label"], width=16))
			self.ControlPres[x][1].grid(column=0, row=RowCounter)
			self.ControlPres[x].append(Label(self.ControlTab, textvariable=self.ControlPres[x][0], style="TLabel", relief="groove", anchor=self.Allignment["Label"], width=16))
			self.ControlPres[x][2].grid(column=1, row=RowCounter)
			RowCounter+=1
			
			
		for x in range(3):self.ControlTab.grid_columnconfigure(x, weight=1)
		for x in range(5):self.ControlTab.grid_rowconfigure(x, weight=1)
			
		
		
		
		#Widgets and Griding
		self.ColumnCounter=0
		#Buttons
		for x in self.ButtonDict:
			self.ButtonDict[x].append(Button(self.ConfigTab, text=x, style="TButton", command=self.ButtonDict[x][0]))
			self.ButtonDict[x][1].grid(row=0, column=self.ColumnCounter*6, columnspan=6, sticky="NEWS")
			self.ColumnCounter+=1

			
			

		self.ColumnCounter=0
		#Upper Labels
		for x in self.UpperLabelDict:
			self.UpperLabelDict[x].append(Label(self.ConfigTab, text=x, style="TLabel", relief="groove", anchor=self.Allignment["Label"]))
			self.UpperLabelDict[x][0].grid(row=1, column=self.ColumnCounter*6, columnspan=6, sticky="NEWS")
			self.ColumnCounter+=1


			
			
		self.RowCounter=2
		#Upper Cells
		for x in self.UpperCells:
			self.ColumnCounter=0
			self.UpperCells[x][0].append(Label(self.ConfigTab, text=x, style="TLabel", relief="groove", anchor=self.Allignment["Label"]))
			self.UpperCells[x][0][0].grid(row=self.RowCounter, column=self.ColumnCounter*6, columnspan=6, sticky="NEWS")
			self.ColumnCounter+=1
			for y in range(4):
				self.UpperCells[x][0].append(Entry(self.ConfigTab, style="TEntry", justify=self.Allignment["Entry"]))
				self.UpperCells[x][0][y+1].insert("end", self.UpperCells[x][1][y])
				self.UpperCells[x][0][y+1].grid(row=self.RowCounter, column=self.ColumnCounter*6, columnspan=6, sticky="NEWS")
				self.ColumnCounter+=1
			self.RowCounter+=1

			
			
		#Lower Cells
		for x in self.LowerDict:
			self.LowerDict[x][0].append(Label(self.ConfigTab, text=x, style="TLabel", relief="groove", anchor=self.Allignment["Label"]))
			self.LowerDict[x][0].append(Entry(self.ConfigTab, style="TEntry", justify=self.Allignment["Entry"]))
			self.LowerDict[x][0][0].grid(row=self.RowCounter, column=0, columnspan=15, sticky="NEWS")
			self.LowerDict[x][0][1].insert("end", self.LowerDict[x][1])
			self.LowerDict[x][0][1].grid(row=self.RowCounter, column=15, columnspan=15, sticky="NEWS")
			self.RowCounter+=1


			
			
		#Radio Button
		self.ThrottleRow.append(Label(self.ConfigTab, text="Throttle Side", style="TLabel", relief="groove", anchor=self.Allignment["Label"]))
		self.ThrottleRow.append(Radiobutton(self.ConfigTab, text="Left", style="TRadiobutton", variable=self.ThrottleRow[0], value="L"))
		self.ThrottleRow.append(Radiobutton(self.ConfigTab, text="Right", style="TRadiobutton", variable=self.ThrottleRow[0], value="R"))
		if "L" ==self.ThrottleRow[0].get():self.ThrottleRow[2].invoke()
		else:self.ThrottleRow[3].invoke()
		self.ThrottleRow[1].grid(row=self.RowCounter, column=0, columnspan=10, sticky="NEWS")
		self.ThrottleRow[2].grid(row=self.RowCounter, column=10, columnspan=10, sticky="NEWS")
		self.ThrottleRow[3].grid(row=self.RowCounter, column=20, columnspan=10, sticky="NEWS")
		self.RowCounter+=1

		
		
		#Check Buttons
		self.CheckButtonCount=0
		for x in self.CheckButtonDict:
			self.CheckButtonDict[x].append(Checkbutton(self.ConfigTab, text=x, variable=self.CheckButtonDict[x][0], onvalue=1, offvalue=0))
			if self.CheckButtonCount<6:
				self.CheckButtonDict[x][2].grid(row=self.RowCounter, column=self.CheckButtonCount*5, columnspan=5, sticky="NEWS")
			else:			
				self.CheckButtonDict[x][2].grid(row=self.RowCounter+1, column=(self.CheckButtonCount-6)*5, columnspan=5, sticky="NEWS")
			self.CheckButtonCount+=1
			
		self.RowCounter+=2	
		
		
		#Data Presenting Labels
		self.ColumnCounter=30
		for x in self.DataPresDict:
			self.DataPresDict[x][0].append(Label(self.ConfigTab, text=x, style="TLabel", relief="groove", anchor=self.Allignment["Label"], width=7))
			self.DataPresDict[x][0][0].grid(row=0, column=self.ColumnCounter, columnspan=1, sticky="NEWS")			
			for y in range(self.RowCounter-1):
				self.DataPresDict[x][1].append(Label(self.ConfigTab, textvariable=self.DataPresDict[x][2][y], style="TLabel", relief="groove", anchor=self.Allignment["Label"], width=7))
				self.DataPresDict[x][1][y].grid(row=y+1, column=self.ColumnCounter, columnspan=1, sticky="NEWS")
			self.ColumnCounter+=1
		
		
		for x in range(self.ColumnCounter):self.ConfigTab.grid_columnconfigure(x, weight=1)
		for x in range(self.RowCounter):self.ConfigTab.grid_rowconfigure(x, weight=1)
		

	def Lock_Button(self):
		global Flag
		if Flag["Connected"]==False:
			messagebox.showwarning("Quadcopter", "Check Wifi Connection.")
		elif Flag["UDP"]==False:
			messagebox.showwarning("Quadcopter", "Check UDP Transmission")
		else:Button_Trig_Send(["@1:0#"], "Quad Copter Locked")
		
		
	def Unlock_Button(self):
		global Flag
		if Flag["Connected"]==False:
			messagebox.showwarning("Quadcopter", "Check Wifi Connection.")
		elif Flag["UDP"]==False:
			messagebox.showwarning("Quadcopter", "Check UDP Transmission")
		else:Button_Trig_Send(["@1:1#"], "Quad Copter Unlocked")
	
	
	def Sync_Button(self):
		global Flag
		global DataFile
		Data=self.Save_File(Open_Config("w")["File"])
		
		
		Flag["Sync"]=True
		DataFile.close()
		DataFile=open(str(Time.now().month).zfill(2)+"."+str(Time.now().day).zfill(2)+" "+str(Time.now().hour).zfill(2)+"-"+str(Time.now().minute).zfill(2)+"-"+str(Time.now().second).zfill(2)+".txt", "w")
		for x in self.Get_Items():
			DataFile.write(x+"\t")
			
		
		Flag["Sync"]=False
		if Flag["Connected"]==False:
			messagebox.showwarning("Quadcopter", "Check Wifi Connection.")
		elif Flag["UDP"]==False:
			messagebox.showwarning("Quadcopter", "Check UDP Transmission")
		else:Button_Trig_Send(Data, "Config Synchronized")
	
	def HoldAlt_Button(self):
		global Flag
		if Flag["Connected"]==False:
			messagebox.showwarning("Quadcopter", "Check Wifi Connection.")
		elif Flag["UDP"]==False:
			messagebox.showwarning("Quadcopter", "Check UDP Transmission")
		else:Button_Trig_Send(["@1:2#"], "Altitude Held")
		
		
	def UnholdAlt_Button(self):
		global Flag
		if Flag["Connected"]==False:
			messagebox.showwarning("Quadcopter", "Check Wifi Connection.")
		elif Flag["UDP"]==False:
			messagebox.showwarning("Quadcopter", "Check UDP Transmission")
		else:Button_Trig_Send(["@1:3#"], "Altitude Hold Released")
		
	
	def Read_File(self, ConfigFile):		
		for x in self.UpperCells:
			for y in range(len(self.UpperCells[x][1])):
				TmpStr=ConfigFile.readline()
				self.UpperCells[x][1][y]=TmpStr[:-1]
				
		for x in self.LowerDict:
			TmpStr=ConfigFile.readline()
			self.LowerDict[x][1]=TmpStr[:-1]
			
		TmpStr=ConfigFile.readline()
		self.ThrottleRow[0].set(TmpStr[:-1])
			
		for x in self.CheckButtonDict:
			TmpStr=ConfigFile.readline()
			self.CheckButtonDict[x][0].set(int(TmpStr[:-1]))
			self.CheckButtonDict[x][1]=self.CheckButtonDict[x][0].get()
			
			
	def Save_File(self, ConfigFile):
		TmpStrList=["@6:", "@4:"]
		for x in self.UpperCells:
			for y in range(len(self.UpperCells[x][1])):
				self.UpperCells[x][1][y]=self.UpperCells[x][0][y+1].get()
				ConfigFile.write(self.UpperCells[x][1][y]+'\n')
				TmpStrList[0]+=self.UpperCells[x][1][y]+":"
		TmpStrList[0]=TmpStrList[0][:-1]
		TmpStrList[0]+="#"
		
		
		TmpCnt=0
		for x in self.LowerDict:
			self.LowerDict[x][1]=self.LowerDict[x][0][1].get()
			ConfigFile.write(self.LowerDict[x][1]+'\n')
			if TmpCnt<len(self.LowerDict)-2:
				TmpStrList[1]+=self.LowerDict[x][1]+":"
				TmpCnt+=1
		TmpStrList[1]=TmpStrList[1][:-1]
		TmpStrList[1]+="#"
				
			
		ConfigFile.write(self.ThrottleRow[0].get()+'\n')
			
		for x in self.CheckButtonDict:
			ConfigFile.write(str(self.CheckButtonDict[x][0].get())+'\n')
			self.CheckButtonDict[x][1]=self.CheckButtonDict[x][0].get()
			
		return TmpStrList
		
		
	def Get_Items(self):
		Items=[]
		for x in self.CheckButtonDict:
			if(self.CheckButtonDict[x][1]==1):
				Items.append(x)
		return Items
		
	def Get_Throttle(self, event):
		if event.x>=0 and event.x<=self.ThrottleCanvas.winfo_width() and event.y >=0 and event.y<=self.ThrottleCanvas.winfo_height():
			Diff=[event.x-self.ThrottleBallPos['Current'][0], event.y-self.ThrottleBallPos['Current'][1]]
			self.ThrottleCanvas.move(self.ThrottleBall, Diff[0], Diff[1])
			self.ThrottleBallPos['Current']=[event.x, event.y]
			
		else:
			Diff=[self.ThrottleBallPos['Origin'][0]-self.ThrottleBallPos['Current'][0], self.ThrottleBallPos['Origin'][1]-self.ThrottleBallPos['Current'][1]]
			self.ThrottleCanvas.move(self.ThrottleBall, Diff[0], Diff[1])
			self.ThrottleBallPos['Current']=self.ThrottleBallPos['Origin']
		print(self.ThrottleBallPos, Diff)
	
	def Reset_Throttle(self, event):
		Diff=[self.ThrottleBallPos['Origin'][0]-self.ThrottleBallPos['Current'][0], self.ThrottleBallPos['Origin'][1]-self.ThrottleBallPos['Current'][1]]
		self.ThrottleCanvas.move(self.ThrottleBall, Diff[0], Diff[1])
		self.ThrottleBallPos['Current']=self.ThrottleBallPos['Origin']
		
	def Get_Direction(self, event):
		if event.keycode==38 or event.char=='w':
			print("Forward")
		elif event.keycode==40 or event.char=='s':
			print("Backward")
		elif event.keycode==37 or event.char=='a':
			self.ControlPres
		elif event.keycode==39 or event.char=='d':
			print("Right")	
			
		

Flag={"Sync": False, "UIActive": True, "Connected": False, "UDP":False, "DataPres":0}

Address=("192.168.1.1", 239)
Socket=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

Time=datetime.datetime
DataFile=open(str(Time.now().month).zfill(2)+"."+str(Time.now().day).zfill(2)+" "+str(Time.now().hour).zfill(2)+"-"+str(Time.now().minute).zfill(2)+"-"+str(Time.now().second).zfill(2)+".txt", "w")

root=Tk()

ConnectionThread=Connect_Wifi_Thread()
#ConnectionThread.start()

RcvDataThread=Receive_Data_Thread()
#RcvDataThread.start()

root.deiconify()
UI1=UI(root)
root.mainloop()
Flag["UIActive"]=False