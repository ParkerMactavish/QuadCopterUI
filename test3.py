import tkinter as tk

from time import sleep

root=tk.Tk()

LStr1=tk.StringVar()
Label1=tk.Label(root, textvariable=LStr1)

Label1.pack()

x=1

while 1:
	x+=1
	x%=1000
	LStr1.set(str(x))
	print(LStr1.get())
	root.update()

