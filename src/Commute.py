import threading
#to inheritance from threading

import os
#to do system call

class Connect_Wifi_Thread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
	def run(self, globalFlag):		
		if (os.system("netsh wlan connect \"Quadcopter\""))==1:#give the first attempt to connect the wifi called Quadcopter
			messagebox.showwarning("Quadcopter", "Connection Error:\nCheck the connection between wi-fi \"Quadcopter\"")#Error message
		else:#Show that it is connect successful
			Flag["Connected"]=True
			messagebox.showinfo("Quadcopter", "Regain Connection with Quad Copter")
			
		while Flag["Connected"]==False and Flag["UIActive"]==True:
			time.sleep(1)
			if (os.system("netsh wlan connect \"Quadcopter\""))==0:	
				messagebox.showinfo("Quadcopter", "Regain Connection with Quad Copter")
				Flag["Connected"]=True
		print("Exit Connecting Thread")