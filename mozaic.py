from tkinter import *
from PIL import Image, ImageFilter, ImageTk
import copy

import editor
import p_action

class Mozaic_Window(Toplevel):
    def __init__(self, parent):
        super(Mozaic_Window, self).__init__(parent)
        self.attributes("-toolwindow", 1)
        self.title("Mozaic")
        self.parent = parent
        self.geometry("200x140+{}+{}".format(parent.winfo_x() + parent.winfo_width() + 30, parent.winfo_y()))
        self.resizable(False, False)
        self.drawWidgets()

        self.target = 0     # 0: Entire, 1: Selected
        self.level = 2      # Default mozaic level

    def drawWidgets(self):
        def radio():
            self.target = targetOption.get()
        targetOption = IntVar()
        radio1 = Radiobutton(self, text = "Apply to the Entire Picture", value = 0, variable = targetOption, command = radio)
        radio1.pack(side = "top")
        radio2 = Radiobutton(self, text = "Apply to the Selected Area", value = 1, variable = targetOption, command = radio)
        radio2.pack(side = "top")

        def scale_func(aux):
            self.level = mozaic_level.get()
        mozaic_level = IntVar()
        scale1 = Scale(self, label = "Set Mozaic Level", variable = mozaic_level, command = scale_func, orient = "horizontal", showvalue = True, resolution = 1, from_ = 2, to = 50)
        scale1.pack(side = "top")

        button1 = Button(self, text = "Apply", command = self.mozaic)
        button1.pack(side = "top", fill = "x")
        
    def mozaic(self):
        if(self.target == 0):
            img = self.parent.image
            new_action = p_action.Action(self.parent, copy.deepcopy(img), "Mozaic <{}>".format(self.level))
            new_action.stack()
            if(img == None):
                print("No Image")
            pixels = img.load()
            for i in range(0, img.size[0], self.level):
                for j in range(0, img.size[1], self.level):
                    self.pixel_average(pixels, i, j, self.level, img.size)
            self.parent.refreshImage()
        else:
            return
            
    
    def pixel_average(self, pixels, left, top, level, size):
        average = [0, 0, 0]
        total_pixels = 0
        for i in range(left, min(left + level, size[0])):
            for j in range(top, min(top + level, size[1])):
                average[0] = average[0] + pixels[i, j][0]
                average[1] = average[1] + pixels[i, j][1]
                average[2] = average[2] + pixels[i, j][2]
                total_pixels += 1
        average[0] = int(average[0] / total_pixels)
        average[1] = int(average[1] / total_pixels)
        average[2] = int(average[2] / total_pixels)

        for i in range(left, min(left + level, size[0])):
            for j in range(top, min(top + level, size[1])):
                pixels[i, j] = tuple(average)

    def __del__(self):
        self.parent.o_mozaic_window = False

