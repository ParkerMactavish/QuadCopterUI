from tkinter import *

root = Tk()

def key(event):
	print(event.keycode)
	print ("pressed", event.char)

def callback(event):
	global frame
	frame.focus_set()
	if event.x<frame.winfo_width() and event.x >0:
		print ("clicked at", event.x, event.y)
		print(frame.winfo_width())

frame = Frame(root,width=100, height=100, relief="groove")
frame.bind("<Key>", key)
frame.bind("<B1-Motion>", callback)
frame.grid()
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)

root.mainloop()