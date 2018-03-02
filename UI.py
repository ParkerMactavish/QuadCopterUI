from tkinter.ttk import Label, Button, Checkbutton, Entry, Radiobutton, Notebook, Frame
from tkinter import Tk, Canvas, messagebox
import tkinter as tk
import tkinter.ttk as ttk

import collections
import os.path

import socket
import time
import datetime

import threading
import os

Flag={("Sync", False), ("UIActive", True), ("Connected", False)}

Address=("192.168.1.1", 239)

class UI:
	def __init__(self, master):
		self.Allignment={"Button": "center", "Label": "center", "Entry": "center", "RadioButton": "center", "CheckButton": "center"}
		
		UpperCellValues=[[1,1,0,0],[1,1,0,0],[1.5,1,0,0],[0, 0, 0, 0],[1.5,0,0,0.01], [1.5,0,0,0.01], [1.5,0,0,0.01], [0,0,0,0]]
		LowerCellValues=[1000, -4, 8, 2.5, 70]
		self.ThrottleSide=tk.StringVar()
		self.ThrottleSide.set("L")
		CheckButtonValueList=[]
		CheckButtonValueBuf=[]

		#Panel Appearance
		master.title("Quadcopter GUI")
		master.grid_rowconfigure(0, weight=1)
		master.grid_columnconfigure(0, weight=1)
		
		
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
		self.ConfigTab.grid_columnconfigure(0, weight=1)
		self.ControlTab=Frame(self.NoteBook)
		self.NoteBook.add(self.ConfigTab, text="Configs")
		self.NoteBook.add(self.ControlTab, text="Controls")
		
		
		
		#Creating List from widges
		self.ButtonDict=collections.OrderedDict([("Lock", [self.Lock_Button]), ("Unlock", [self.Unlock_Button]), ("Sync", [self.Sync_Button]), ("HoldAlt", [self.HoldAlt_Button]), ("UnholdAlt", [self.UnholdAlt_Button])])#first for functions, second for buttons
		
		self.UpperLabelDict=collections.OrderedDict([("PID", []), ("P", []), ("I", []), ("I Limit", []), ("D", [])])#first for widget
		
		self.UpperCells=collections.OrderedDict([("Attitude Roll",[[], [1, 1, 0, 0]]), ("Attitude Pitch",[[], [1, 1, 0, 0]]), ("Attitude Yaw",[[], [1.5, 1, 0, 0]]), ("Attitude Height", [[], [1, 0, 0, 0]]), ("Rate Roll",[[], [1.5, 0, 0, 0]]), ("Rate Pitch",[[], [1.5, 0, 0, 0.01]]), ("Rate Yaw",[[], [1.5, 0, 0, 0.01]]), ("Rate Height",[[], [1, 0, 0, 0]])])#first list for entries, second list for values
		
		self.LowerDict=collections.OrderedDict([("Angular Velocity Limit", [[], 1000]), ("Roll Angular Calibration", [[], -4]), ("Pitch Angular Calibration", [[], 8]), ("Stick Gain", [[], 2.5]), ("Max Throttle Percentage", [[], 70])])#first list for labels and entries, second value for values
		
		self.RadioButtonRow=[]
		
		self.CheckButtonDict=collections.OrderedDict([("pitch", []), ("roll", []), ("yaw", []), ("atm", []), ("height", []), ("throt", []), ("rot1", []), ("rot2", []), ("rot3", []), ("rot4", []), ("volt", [])])
		#first for check button, second for int var, third for buffer int
		
		self.DataPresDict=collections.OrderedDict([("pitch", [[], [], [], []]), ("roll", [[], [], [], []]), ("yaw", [[], [], [], []]), ("atm", [[], [], [], []]), ("height", [[], [], [], []]), ("throt", [[], [], [], []]), ("rot1", [[], [], [], []]), ("rot2", [[], [], [], []]), ("rot3", [[], [], [], []]), ("rot4", [[], [], [], []]), ("volt", [[], [], [], []])])
		#first for label, second for following labels third for int var, fourth for buffer int
		
		ColumnCounter=0
		#Buttons
		for x in self.ButtonDict:
			self.ButtonDict[x].append(Button(self.ConfigTab, text=x, style="TButton", command=self.ButtonDict[x][0]))
			self.ButtonDict[x][1].grid(row=0, column=ColumnCounter*2, columnspan=2, sticky="NEWS")
			ColumnCounter+=1
		
		
		ColumnCounter=0
		#Upper Labels
		for x in self.UpperLabelDict:
			self.UpperLabelDict[x].append(Label(self.ConfigTab, text=x, style="TLabel", relief="groove", anchor=self.Allignment["Label"]))
			self.UpperLabelDict[x][0].grid(row=1, column=ColumnCounter*2, columnspan=2, sticky="NEWS")
			ColumnCounter+=1
			
		
		RowCounter=2
		#Upper Cells
		for x in self.UpperCells:
			ColumnCounter=0
			self.UpperCells[x][0].append(Label(self.ConfigTab, text=x, style="TLabel", relief="groove", anchor=self.Allignment["Label"]))
			self.UpperCells[x][0][0].grid(row=RowCounter, column=ColumnCounter*2, columnspan=2, sticky="NEWS")
			ColumnCounter+=1
			for y in range(4):
				self.UpperCells[x][0].append(Entry(self.ConfigTab, style="TEntry", justify=self.self.Allignment["Entry"]))
				self.UpperCells[x][0][y+1].insert("end", self.UpperCells[x][1][y])
				self.UpperCells[x][0][y+1].grid(row=RowCounter, column=ColumnCounter*2, columnspan=2, sticky="NEWS")
				ColumnCounter+=1
			RowCounter+=1
		
		

	def Lock_Button(self):
		pass
	def Unlock_Button(self):
		pass
	def Sync_Button(self):
		pass
	def HoldAlt_Button(self):
		pass
	def UnholdAlt_Button(self):
		pass

		

root=Tk()
UI1=UI(root)
root.mainloop()
		
		
		