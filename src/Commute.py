'''
This module is meant to deal with the communication issues, such as Wi-Fi connecting, UDP data sending, receiving.

This module requires:
	-threading
	-os
	-messagebox from tkinter
	-time
	variable:
		globalFlag[WifiConnection, UIActive, SocketHandle], master

This module contains:
	-connectWifiThread
	function:
		__init__(globalFlag, master)
		--globalFlag is a dictionary allows every module to communicate, master is a tkinter object for messagebox
		--to construct this thread by adding the run function to thread
		run(globalFlag, master)
		--globalFlag and master are the same as the ones in __init__
		--to attempt to connect with the wifi AP called Quadcopter. If not connected, it would show warning.

--Edited on 18.06.03

'''

import threading
#to inheritance from threading

import os
#to do system call

from tkinter import messagebox
#to show warning or info

import time
#to rest for 1 second in the loop


##this function is to do an one-time attempt of sending data to the quadcopter
def Send_Data(address, data):#address is a tuple of ip address and port number, socketObject is a socket object with connection, data is the raw data needed to be sent
	socketObject=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)#First we create a socket
	try:
		socketObject.sendto(Data.encode(), address)
		#print(Data)#for debugging
	except:
		print("Debug Send Data")
	#Second we do an attempt to send data through the socket
	
	socketObject.close()
	#At last we close the socket and wait for others to use it

		
##this function is to do an one-time attempt of receiving data from the quadcopter
def Recieve_Data(address):#address is a tuple of ip address and port number, socketObject is a socket object with connection
	socketObject=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	#First we create a socket
	data=b''
	try:
		Socket.bind(RecAddr)
	except:
		print("Debug Socket Bind")
	
	try:
		Socket.settimeout(0.1)
		data, (RecAddr, Address[1])=Socket.recvfrom(512)
	except:		
		print("Debug Recv Data")
	return data.decode()		


class connectWifiThread(threading.Thread):
	def __init__(self, globalFlag, master):#globalFlag is a dictionary allows every module to communicate, master is a tkinter object for messagebox
		thread = threading.Thread(target=self.run, args=(globalFlag, master))
		thread.daemon = True# Daemonize thread
		thread.start()		# Start the execution
	def run(self, globalFlag, master):		
		if os.system("netsh wlan connect \"Quadcopter\"")==1:#give the first attempt to connect the wifi called Quadcopter
			messagebox.showwarning("Quadcopter", "Connection Error:\nCheck the connection between wi-fi \"Quadcopter\"")#Error message
			print(globalFlag["WifiConnection"], globalFlag["UIActive"])
		else:#Show that it is connect successful
			globalFlag["WifiConnection"]=True
			messagebox.showinfo("Quadcopter", "Regain Connection with Quad Copter")
			
		while globalFlag["WifiConnection"]==False and globalFlag["UIActive"]==True:#Keep trying while the master window is still alive
			time.sleep(1)
			if (os.system("netsh wlan connect \"Quadcopter\""))==0:	
				messagebox.showinfo("Quadcopter", "Regain Connection with Quad Copter")
				globalFlag["WifiConnection"]=True
		print("Exit Connecting Thread")
		

class throttleDataThread(threading.Thread):
	def __init__(self, globalFlag, master, address, UI):#globalFlag is a dictionary allows every module to communicate, master is a tkinter object for messagebox, address is a tuple of ip address and port number, socketObject is a socket object with connection, data is the raw data needed to be sent
		thread = threading.Thread(target=self.run, args=(globalFlag, master, address, UI))
		thread.daemon = True# Daemonize thread
		thread.start()		# Start the execution
		
	def run(self, globalFlag, master, address, UI):
		while Flag["UIActive"]:
			if Flag["SocketUsage"]=="Send Normal0" or Flag["SocketUsage"]=="Send Normal1":
				#First we generate the data to send
				data="@2"
				for x in UI.ControlPres:
					data+=':'+UI.ControlPres[x][0].get()
				data+='#'
				
				#Second we directly call the Send_Data function
				Send_Data(address, data)	

				#Determine who would be using the socket as following
				if Flag["UIButtoneTriggered"]==True: Flag["SocketUsage"]="Send Triggered"
				elif Flag["SocketUsage"]=="Send Normal0": Flag["SocketUsage"]="Send Normal1"
				else Flag["SocketUsage"]="Receive Normal"