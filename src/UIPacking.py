'''
This module is meant to define the packing of the UI, and the actions of the buttons.
--Last Edited on 18.06.03
'''
##COULD possibly be replaced by some other form of User Interface##

from tkinter.ttk import Label, Button, Checkbutton, Entry, Radiobutton, Notebook, Frame
#the basic components of the user interface
#ttk is more gorgeous

from tkinter import Tk, Canvas, messagebox, StringVar, IntVar
#the basic components of the user interface
#these are what ttk doesn't have

import tkinter as tk
#call tkinter as tk for short

import tkinter.ttk as ttk
#call tkinter.ttk as ttk for short

from matplotlib.figure import Figure
##NOT sure its use, probably the figure drawing

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
##NOT sure its use, probably the figure drawing

import src.DataAccess as DA
#call file writing and file reading

##main part
class UI:
	#Constant for Allignment, Span, and File Name
	#Allignment for all kinds of widgets
	Allignment={"Button": "center", "Label": "center", "Entry": "center", "RadioButton": "center", "CheckButton": "center"}
	
	#Span for different rows of widgets
	Span={"topButton":6, "upperLabel":6, "upperCellLabel":6, "upperCellEntry":6, "lowerCellLabel":15, "lowerCellEntry":15, "throttleRadioButton":10, "checkButton":5}
	
	#Configuration File Name
	configFileName=".\\data\\Config.txt"
	
	
	
	
	
	
	#Container for UI
	##rank one
	NoteBook=0			#To store the two tabs
	
	
	
	##rank two 
	ConfigTab=0			#To store the config buttons, labels and entries
	ControlTab=0		#To store the control canvases and feedback
	
	
	
	##rank three
	#Creating Dict for buttons on the top
	##key Button for the later defined button object
	##key Event for the corresponding function of the button
	ButtonDict=\
	{
	"Lock":{"Button":0, "Event":0}, 
	"Unlock":{"Button":0, "Event":0}, 
	"Sync":{"Button":0, "Event":0}, 
	"Hold Altitude":{"Button":0, "Event":0}, 
	"Release Altitude":{"Button":0, "Event":0}\
	}
	
	#Creating Dict for labels on the top-PID, P, I, I Limit and D
	##value for the later defined label objects 
	UpperLabelDict={"PID":0, "P":0, "I":0, "I Limit":0, "D":0}
		
	#Creating Dict for labels and entries in the upper half of config tab-[Attitude Roll, Attitude Pitch, Attitude Yaw, Attitude Height, Rate Roll, Rate Pitch, Roll Yaw, Roll Height]
	##key Label for the later defined label in the front of the row
	##key Entries for the later defined entries in the row
	##key Values for values in the entries
	UpperCells=\
	{
		"Attitude Roll":{"Label":0, "Entries":[], "Values":["1", "1", "0", "0"]},
		"Attitude Pitch":{"Label":0, "Entries":[], "Values":["1", "1", "0", "0"]},
		"Attitude Yaw":{"Label":0, "Entries":[], "Values":["1.5", "1", "0", "0"]},
		"Attitude Height":{"Label":0, "Entries":[], "Values":["1", "0", "0", "0"]},
		"Rate Roll":{"Label":0, "Entries":[], "Values":["1.5", "0", "0", "0"]},
		"Rate Pitch":{"Label":0, "Entries":[], "Values":["1.5", "0", "0", "0.01"]},
		"Rate Yaw":{"Label":0, "Entries":[], "Values":["1.5", "0", "0", "0.01"]},
		"Rate Height":{"Label":0, "Entries":[], "Values":["1", "0", "0", "0"]}\
	}
	
	#Creating Dict for labels and entries in the lower half of config tab-[Angular Velocity, Roll Angular Calibration, Pitch Angular Calibration, Stick Gain, Max Throttle Percentage]
	##key Label for the later defined label in the front of the row
	##key Entry for the later defined entry in the row
	##key Value for value in the entry
	LowerCells=\
	{
		"Angular Velocity":{"Label":0, "Entry":0, "Value":"1000"},
		"Roll Angular Calibration":{"Label":0, "Entry":0, "Value":"-4"},
		"Pitch Angular Calibration":{"Label":0, "Entry":0, "Value":"8"},
		"Stick Gain":{"Label":0, "Entry":0, "Value":"2.5"},
		"Max Throttle Percentage":{"Label":0, "Entry":0, "Value":"70"},\
	}
	
	#Creating Dict for labels and entries in the lower half of config tab-[Label, Value, RadioButton]
	##key Label for the later defined label in the front of the row
	##key Value for the later defined string variable for the radio button
	##key RadioButton for the later defined radio button in the row
	ThrottleRow={"Label":0, "Value":0, "RadioButton":{"L":0, "R":0}}
	
	#Creating Dict for int variables, buffer values, and check buttons and in the lower half of config tab-[IntVar, BufferValue, CheckButton]
	##key IntVar for the later defined int variable for the check button
	##key BufferValue for the later defined buffer integer for the int variable
	##key RadioButton for the later defined radio button in the row
	CheckButtonDict=\
	{
		"Pitch":{"IntVar":0, "BufferValue":0, "CheckButton":0},
		"Roll":{"IntVar":0, "BufferValue":0, "CheckButton":0},
		"Yaw":{"IntVar":0, "BufferValue":0, "CheckButton":0},
		"Air Pressure":{"IntVar":0, "BufferValue":0, "CheckButton":0},
		"Height":{"IntVar":0, "BufferValue":0, "CheckButton":0},
		"Throttle":{"IntVar":0, "BufferValue":0, "CheckButton":0},
		"Rotation 1":{"IntVar":0, "BufferValue":0, "CheckButton":0},
		"Rotation 2":{"IntVar":0, "BufferValue":0, "CheckButton":0},
		"Rotation 3":{"IntVar":0, "BufferValue":0, "CheckButton":0},
		"Rotation 4":{"IntVar":0, "BufferValue":0, "CheckButton":0},
		"Voltage":{"IntVar":0, "BufferValue":0, "CheckButton":0},\
	}
	
	
	
	
	def __init__(self, master):
		#Initializing StringVar and IntVar in ThrottleRow and CheckButtonDict	
		self.ThrottleRow["Value"]=StringVar(master, "L")
		for x in self.CheckButtonDict:
			self.CheckButtonDict[x]["IntVar"]=IntVar(master, 0)
			
		
		#Checking if ConfigFile exists. 
		#	if so, read the stored config
		#	else, create a config file
		if DA.open_File(self.configFileName, "read")["FileExist"]==True:
			self.read_File(DA.open_File(self.configFileName, "read")["File"])
		else:
			self.create_File(DA.open_File(self.configFileName, "write")["File"])
		
		#Panel Appearance
		master.title("Quadcopter GUI")
		master.grid_rowconfigure(0, weight=1)
		master.grid_columnconfigure(0, weight=1)

		#Styling
		ttk.Style().configure("TButton", padding=5, background="#ccc", anchor=self.Allignment["Button"])
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
		
		
		
		#Linking Events with ButtonDict contents
		self.ButtonDict["Lock"]["Event"]=self.lock_Button
		self.ButtonDict["Unlock"]["Event"]=self.unlock_Button
		self.ButtonDict["Sync"]["Event"]=self.sync_Button
		self.ButtonDict["Hold Altitude"]["Event"]=self.holdalt_Button
		self.ButtonDict["Release Altitude"]["Event"]=self.unholdalt_Button
		
		#Creating Buttons on the top and putting them into the ButtonDict
		rowCounter=0
		columnCounter=0
		for x in self.ButtonDict:
			self.ButtonDict[x]["Button"]=Button(self.ConfigTab, text=x, style="TButton", command=self.ButtonDict[x]["Event"])
			self.ButtonDict[x]["Button"].grid(row=rowCounter, column=columnCounter*self.Span["topButton"], columnspan=self.Span["topButton"], sticky="NEWS")
			columnCounter+=1
		rowCounter+=1
		
		
		
		#Creating Labels on the top and putting them into the UpperLabelDict
		columnCounter=0
		for x in self.UpperLabelDict:
			self.UpperLabelDict[x]=Label(self.ConfigTab, text=x, style="TLabel", relief="groove", anchor=self.Allignment["Label"])
			self.UpperLabelDict[x].grid(row=rowCounter, column=columnCounter*self.Span["upperLabel"], columnspan=self.Span["upperLabel"], sticky="NEWS")
			columnCounter+=1
		rowCounter+=1
		
		
		#Creating Labels and Entries on the upper half and putting them into the UpperCells		
		for x in self.UpperCells:
			columnCounter=0
			#Labels
			self.UpperCells[x]["Label"]=Label(self.ConfigTab, text=x, style="TLabel", relief="groove", anchor=self.Allignment["Label"])
			self.UpperCells[x]["Label"].grid(row=rowCounter, column=columnCounter*self.Span["upperCellLabel"], columnspan=self.Span["upperCellLabel"], sticky="NEWS")
			columnCounter=1
			#Entries
			for y in range(len(self.UpperLabelDict)-1):
				self.UpperCells[x]["Entries"].append(Entry(self.ConfigTab, style="TEntry", justify=self.Allignment["Entry"]))
				self.UpperCells[x]["Entries"][y].insert("end", self.UpperCells[x]["Values"][y])
				self.UpperCells[x]["Entries"][y].grid(row=rowCounter, column=columnCounter*self.Span["upperCellEntry"], columnspan=self.Span["upperCellEntry"], sticky="NEWS")
				columnCounter+=1
			rowCounter+=1
		

		#Creating Labels and Entries on the lower half and putting them into the LowerCells	
		for x in self.LowerCells:
			self.LowerCells[x]["Label"]=Label(self.ConfigTab, text=x, style="TLabel", relief="groove", anchor=self.Allignment["Label"])
			self.LowerCells[x]["Entry"]=Entry(self.ConfigTab, style="TEntry", justify=self.Allignment["Entry"])
			self.LowerCells[x]["Label"].grid(row=rowCounter, column=0, columnspan=self.Span["lowerCellLabel"], sticky="NEWS")
			self.LowerCells[x]["Entry"].insert("end", self.LowerCells[x]["Value"])
			self.LowerCells[x]["Entry"].grid(row=rowCounter, column=self.Span["lowerCellLabel"], columnspan=self.Span["lowerCellEntry"], sticky="NEWS")
			rowCounter+=1
		
		
		#Creating Radio Button for the throttle row and putting them into the ThrottleRow
		self.ThrottleRow["Label"]=Label(self.ConfigTab, text="Throttle Side", style="TLabel", relief="groove", anchor=self.Allignment["Label"])
		self.ThrottleRow["RadioButton"]["L"]=Radiobutton(self.ConfigTab, text="Left", style="TRadiobutton", variable=self.ThrottleRow["Value"], value="L", command=self.set_Throttle_Left)
		self.ThrottleRow["RadioButton"]["R"]=Radiobutton(self.ConfigTab, text="Right", style="TRadiobutton", variable=self.ThrottleRow["Value"], value="R", command=self.set_Throttle_Right)
		#if the Value stores "L" then invoke the radio button on the left side. if "R" then otherwise
		if "L" ==self.ThrottleRow["Value"].get():self.ThrottleRow["RadioButton"]["L"].invoke()
		else:self.ThrottleRow["RadioButton"]["R"].invoke()
		self.ThrottleRow["Label"].grid(row=rowCounter, column=0, columnspan=self.Span["throttleRadioButton"], sticky="NEWS")
		self.ThrottleRow["RadioButton"]["L"].grid(row=rowCounter, column=self.Span["throttleRadioButton"], columnspan=self.Span["throttleRadioButton"], sticky="NEWS")
		self.ThrottleRow["RadioButton"]["R"].grid(row=rowCounter, column=2*self.Span["throttleRadioButton"], columnspan=self.Span["throttleRadioButton"], sticky="NEWS")
		rowCounter+=1
		
		#Creating Check Buttons for the data output and putting them into the CheckButtonDict
		columnCounter=0
		nextRow=False
		for x in self.CheckButtonDict:
			self.CheckButtonDict[x]["CheckButton"]=Checkbutton(self.ConfigTab, text=x, variable=self.CheckButtonDict[x]["IntVar"], onvalue=1, offvalue=0)
			if not nextRow:
				self.CheckButtonDict[x]["CheckButton"].grid(row=rowCounter, column=columnCounter*self.Span["checkButton"], columnspan=self.Span["checkButton"], sticky="NEWS")
			else:			
				self.CheckButtonDict[x]["CheckButton"].grid(row=rowCounter, column=columnCounter*self.Span["checkButton"], columnspan=self.Span["checkButton"], sticky="W")
			columnCounter+=1
			if columnCounter==6:
				nextRow=True
				rowCounter+=1
				columnCounter=0
		rowCounter+=1
		
		
		
	def read_File(self, file):
		#Reading for upper cells
		for x in self.UpperCells:
			for y in range(len(self.UpperCells[x]["Values"])):
				TmpStr=file.readline()
				self.UpperCells[x]["Values"][y]=TmpStr[:-1]
				
		#Reading for lower cells
		for x in self.LowerCells:
			TmpStr=file.readline()
			self.LowerCells[x]["Value"]=TmpStr[:-1]
		
		#Reading for throttle row
		TmpStr=file.readline()
		self.ThrottleRow["Value"].set(TmpStr[:-1])
		
		#Reading for check buttons
		for x in self.CheckButtonDict:
			TmpStr=file.readline()
			self.CheckButtonDict[x]["IntVar"].set(int(TmpStr[:-1]))
			self.CheckButtonDict[x]["BufferValue"]=self.CheckButtonDict[x]["IntVar"].get()
		
	
	def save_File(self, file):
		#Saving upper cells
		for x in self.UpperCells:
			for y in range(len(self.UpperCells[x]["Values"])):
				self.UpperCells[x]["Values"][y]=self.UpperCells[x]["Entries"][y].get()
				file.write(self.UpperCells[x]["Values"][y]+'\n')
		
		#Saving lower cells
		for x in self.LowerDict:
			self.LowerDict[x]["Value"]=self.LowerDict[x]["Entry"].get()
			ConfigFile.write(self.LowerDict[x]["Value"]+'\n')
		
		#Saving throttle row
		ConfigFile.write(self.ThrottleRow["Value"].get()+'\n')
		
		#Saving check buttons
		for x in self.CheckButtonDict:
			ConfigFile.write(str(self.CheckButtonDict[x]["CheckButton"].get())+'\n')
			self.CheckButtonDict[x]["BufferValue"]=self.CheckButtonDict[x]["CheckButton"].get()
	
	def create_File(self, file):
		#Writing upper cells
		for x in self.UpperCells:
			for y in range(len(self.UpperCells[x]["Values"])):
				file.write(self.UpperCells[x]["Values"][y]+'\n')
				
		#Writing lower cells
		for x in self.LowerCells:
			file.write(self.LowerCells[x]["Value"]+'\n')
		
		#Writing throttle radio button
		file.write(self.ThrottleRow["Value"].get()+'\n')
		
		#Writing check buttons and sync the buffer value with int variable
		for x in self.CheckButtonDict:
			file.write(str(self.CheckButtonDict[x]["IntVar"].get())+'\n')
			self.CheckButtonDict[x]["BufferValue"]=self.CheckButtonDict[x]["IntVar"].get()
	
	
	def lock_Button(self):
		pass
	def unlock_Button(self):
		pass
	def sync_Button(self):
		pass
	def holdalt_Button(self):
		pass
	def unholdalt_Button(self):
		pass
		
	def set_Throttle_Left(self):
		pass
	
	def set_Throttle_Right(self):
		pass
		
