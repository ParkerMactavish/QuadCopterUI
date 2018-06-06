from src.Commute import connectWifiThread
from tkinter import Tk

Flag={"WifiConnection": False, "UIActive":True, "SocketHandle":"Send Thread"}

master=Tk()
connectWifi=connectWifiThread(Flag, master)

master.mainloop()