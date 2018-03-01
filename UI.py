from tkinter.ttk import Label, Button, Checkbutton, Entry, \
Radiobutton, Notebook
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

Flag={("Sync", False), ("UIActive", True)}

Addr=("192.168.1.1", 239)

class UI:
	def __init__(self, master):
		
