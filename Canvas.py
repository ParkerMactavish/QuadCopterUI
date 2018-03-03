from tkinter import *
import time

trace = 0 

class CanvasEventsDemo: 
    def __init__(self, parent=None):
        canvas = Canvas(width=300, height=300, bg='beige') 
        canvas.pack()
        canvas.bind('<ButtonPress-1>', self.onStart)      
        canvas.bind('<B1-Motion>',     self.onGrow)       
        canvas.bind('<Double-1>',      self.onClear)      
        canvas.bind('<ButtonPress-3>', self.onMove)       
        self.canvas = canvas
        self.drawn  = None
        self.kinds = [canvas.create_oval, canvas.create_rectangle]
    def onStart(self, event):
        self.shape = self.kinds[0]
        self.kinds = self.kinds[1:] + self.kinds[:1]      
        self.start = event
        self.drawn = None
    def onGrow(self, event):                     
        canvas = event.widget
        if self.drawn: canvas.delete(self.drawn)
        objectId = self.shape(self.start.x, self.start.y, event.x, event.y)
        if trace: print(objectId)
        self.drawn = objectId
    def onClear(self, event):
        event.widget.delete('all')               
    def onMove(self, event):
        if self.drawn:                           
            if trace: print(self.drawn)
            canvas = event.widget
            diffX, diffY = (event.x - self.start.x), (event.y - self.start.y)
            canvas.move(self.drawn, diffX, diffY)
            self.start = event

class CanvasEventsDemoTags(CanvasEventsDemo):
    def __init__(self, parent=None):
        CanvasEventsDemo.__init__(self, parent)
        self.canvas.create_text(75, 8, text='Press o and r to move shapes')
        self.canvas.master.bind('<KeyPress-o>', self.onMoveOvals)    
        self.canvas.master.bind('<KeyPress-r>', self.onMoveRectangles)  
        self.kinds = self.create_oval_tagged, self.create_rectangle_tagged
    def create_oval_tagged(self, x1, y1, x2, y2):
        objectId = self.canvas.create_oval(x1, y1, x2, y2)
        self.canvas.itemconfig(objectId, tag='ovals', fill='blue')
        return objectId
    def create_rectangle_tagged(self, x1, y1, x2, y2):
        objectId = self.canvas.create_rectangle(x1, y1, x2, y2)
        self.canvas.itemconfig(objectId, tag='rectangles', fill='red')
        return objectId
    def onMoveOvals(self, event):
        print('moving ovals')
        self.moveInSquares(tag='ovals')          
    def onMoveRectangles(self, event):
        print('moving rectangles')
        self.moveInSquares(tag='rectangles')
    def moveInSquares(self, tag):                
        for i in range(5):
            for (diffx, diffy) in [(+20, 0), (0, +20), (-20, 0), (0, -20)]:
                self.canvas.move(tag, diffx, diffy)
                self.canvas.update()             
                time.sleep(0.25)                 

if __name__ == '__main__':
    CanvasEventsDemoTags()
    mainloop()