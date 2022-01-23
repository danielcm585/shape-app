"""
Lab 09: Problem, an example
- draw elastic (rubber) shapes on a canvas by
  a left mouse-click and dragging,
- move the last drawn shape by a right mouse-click
"""

from tkinter import *
from tkinter.colorchooser import askcolor
from tkinter.messagebox import *

class DrawMoveRubberShapes(object):
    def __init__(self):
        window = Tk()                                               # Create a window
        window.title("Lab 09: Draw Rubber Shapes, Select and Move") # Set a title
        window.resizable(False,False)                               # Make the window unresizable
        
        # Create pulldown menu to choose a shape
        menubar = Menu(window)                                      # Create a menu bar
        window.config(menu=menubar)                                 # Display the menu bar
        
        # Create a pulldown menu, and add it to the menu bar
        shapeMenu = Menu(menubar, tearoff=True)                     # Create a tear-able shape menus
        shapeMenu.add_radiobutton(label="line", command=self.chooseLine)
        shapeMenu.add_radiobutton(label="oval/circle", command=self.chooseOval)
        shapeMenu.add_radiobutton(label="rectangle", command=self.chooseRectangle)
        menubar.add_cascade(label="Choose a Shape", menu=shapeMenu) # Insert the shape menus into menu bar
        
        # Create a canvas, bound to mouse events
        self.canvas = Canvas(window, width=500, height=400, relief='ridge', bg='white', bd=5)
        self.canvas.pack()                                          # Show canvas

        # Mouse click operations
        self.canvas.bind('<ButtonPress-1>', self.onStart)           # Left-Click
        self.canvas.bind('<ButtonPress-3>', self.onSelect)          # Right-click

        # Basic drawing 
        self.canvas.bind('<B1-Motion>', self.onGrow)                # + Drag
        
        # Moving objects
        self.canvas.bind('<B3-Motion>', self.onMove)                # + Drag
        
        # Press d to delete object
        self.canvas.bind('<KeyPress-d>', self.deleteObj)            # + Press D 
        self.canvas.focus_set()

        # Press h for help
        self.canvas.create_text(102,15, font='Courier', text='Press h for help')
        self.canvas.bind('<KeyPress-h>', self.showHelp)             # Press H
        self.canvas.focus_set()

        # To rememver the last drawing and shape
        self.drawn = None                                           # Initialize var to store selected object
        self.shape = self.canvas.create_line                        # Set shape to default (line)
        
        # Create and add a frame to window
        frame1 = Frame(window, borderwidth=2)                       # Create a frame below the canvas
        frame1.pack()                                               # Show frame
        
        # Create a button for choosing color using a color chooser
        self.fillColor = StringVar()                                # Initialize fill color var
        self.fillColor.set('red')                                   # Set to default (red)
        
        def colorCommand():
            (rgb,color) = askcolor()                                # Take new color
            if color != None:
                self.fillColor.set(color)                           # Change fill color var
                colorButton["bg"] = color                           # Change color button bg
        
        # Create the color button
        colorButton = Button(frame1, text="Color", command=colorCommand, bg=self.fillColor.get())
        colorButton.grid(row=1,column=1)                            # Show color button

        def clearCanvas():
            self.canvas.delete('drawing')                           # Delete all drawings

        # Create the clear button
        clearButton = Button(frame1, text='Clear', command=clearCanvas)
        clearButton.grid(row=1, column=2)                           # Show clear button

        # Start the mainloop
        window.mainloop()

    def chooseLine(self):
        self.shape = self.canvas.create_line                        # Change shape to line

    def chooseOval(self):
        self.shape = self.canvas.create_oval                        # Change shape to oval

    def chooseRectangle(self):
        self.shape = self.canvas.create_rectangle                   # Change shape to rectangle

    # Remember the left mouse press to start drawing
    def onStart(self, event):
        self.start = event                                          # Set the starting coordinates
        self.drawn = None                                           # Initialize var of selected object

    # Elastic drawing: delete and redraw, repeatedly
    def onGrow(self, event):
        canvas = event.widget
        if (self.drawn): 
            canvas.delete(self.drawn)                               # Delete old object
        objectId = self.shape(self.start.x, self.start.y, event.x, event.y, fill=self.fillColor.get(), tags='drawing')
        self.drawn = objectId                                       # Change into new object

    # Select the closest object on canvas
    def onSelect(self, event):
        self.start = event                                          # Set the starting coordinates
        self.drawn = self.canvas.find_closest(x=event.x, y=event.y) # select the closest object

    # Move the shape during right-click + drag
    def onMove(self, event):
        if (self.drawn):
            canvas = event.widget
            diffX, diffY = (event.x-self.start.x),(event.y-self.start.y)
            canvas.move(self.drawn, diffX, diffY)                   # Move object in the same direction as the mouse
            self.start = event                                      # Set current coordinates as the starting coordinates

    def showHelp(self, event):
        helpMessage = """Mouse commands:
 Left+Drag = Draw new rubber shape
 Right = Select a shape
 Right+Drag = Drag the selected shape
        
Keyboard commands:
 d = Delete the selected shape
 h = Help"""                                                        # Create help message
        showinfo(title='Draw, Select, Move', message=helpMessage)   # Show infobox containing help

    def deleteObj(self, event):
        canvas = event.widget
        canvas.delete(self.drawn)                                   # Delete the selected object

if __name__ == '__main__':
    DrawMoveRubberShapes()