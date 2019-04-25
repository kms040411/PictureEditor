from tkinter import *
from PIL import Image, ImageFilter, ImageTk
from tkinter import filedialog
from threading import Lock
import copy

import mozaic
import p_action

# global variables       
undo_stack = None           # Undo Stack

class App(Tk):
    def __init__(self):
        super().__init__()

        # Init Program Variables
        self.image = None               # Currently Open Image Object
        self.photoimage = None          # Currently Open PhotoImage Object
        self.file = None                # Currently Open File Path   

        self.o_mozaic_window = False    # Is mozaic window opened?

        self.undo_stack = list()        # Initialize Undo Stack
        self.undo_lock = Lock()

        # Root Window
        self.title("Simple Picture Editor")
        self.geometry("640x400+100+100")
        self.resizable(False, False)

        # Widgets
        self.canvas1 = Canvas(self)
        self.canvas1.pack(fill="both")

        # Events
        self.bind_all('<Control-KeyPress-z>', self.undo)

        # Menus
        self.root_menu = Menu(self)
        filemenu = Menu(self.root_menu, tearoff = 0)
        filemenu.add_command(label = "Open", command = self.openfile)
        filemenu.add_command(label = "Save", command = donothing)
        filemenu.add_command(label = "Save as...", command = donothing)
        filemenu.add_separator()
        filemenu.add_command(label = "Exit", command = self.quit)
        self.root_menu.add_cascade(label = "File", menu = filemenu)

        editmenu = Menu(self.root_menu, tearoff = 0)
        editmenu.add_command(label = "Mozaic", command = self.mozaic_menu)
        editmenu.add_separator()
        editmenu.add_command(label = "Undo", command = self.undo)
        self.root_menu.add_cascade(label = "Edit", menu = editmenu)

        self.config(menu = self.root_menu)

        self.mainloop()

    def mozaic_menu(self):
        if(self.o_mozaic_window):
            return
        self.o_mozaic_window = True
        mozaic_window = mozaic.Mozaic_Window(self)

    def openfile(self):
        self.file = filedialog.askopenfilename(title = "Open File", filetypes = (("JPEG Image", "*.jfif"), ("png files", "*.png")))
        self.image = Image.open(self.file)
        self.undo_stack = list()
        self.refreshImage()
    
    def refreshImage(self):
        self.photoimage = ImageTk.PhotoImage(self.image)
        current_width = self.photoimage.width()
        current_height = self.photoimage.height()
        root_width = self.winfo_x()
        root_height = self.winfo_y()

        self.geometry(str(current_width + 20) + "x" + str(current_height + 20) + "+" + str(root_width) + "+" + str(root_height))
        self.canvas1.create_image(0, 0, image = self.photoimage, anchor = NW)

    def undo(self, aux = None):
        self.undo_lock.acquire()

        if(len(self.undo_stack) == 0):
            return
        recent_event = self.undo_stack.pop()
        recent_event.restore()

        self.undo_lock.release()
        
    def restoreImage(self, img):
        self.image = copy.deepcopy(img)
        self.refreshImage()

def donothing():
    pass    # Temp Function that does nothing

if __name__ == "__main__":
    root = App()