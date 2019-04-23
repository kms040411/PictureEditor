from tkinter import *
from PIL import Image, ImageFilter

def gui():
    
    window = Tk()
    window.title("Mozaik")
    window.geometry("640x400+100+100")
    window.resizable(False, False)
    
    

    window.mainloop()

def mozaik(image, level = 2):
    pixels = image.load()

    for i in range(0, image.size[0], level):
        for j in range(0, image.size[1], level):
            pixel_average(pixels, i, j, level, image.size)
    
    image.show()

def pixel_average(pixels, left, top, level, size):
    average = [0, 0, 0]
    total_pixels = level * level
    for i in range(left, min(left + level, size[0])):
        for j in range(top, min(top + level, size[1])):
            average[0] = average[0] + pixels[i, j][0]
            average[1] = average[1] + pixels[i, j][1]
            average[2] = average[2] + pixels[i, j][2]
    average[0] = int(average[0] / total_pixels)
    average[1] = int(average[1] / total_pixels)
    average[2] = int(average[2] / total_pixels)

    for i in range(left, min(left + level, size[0])):
        for j in range(top, min(top + level, size[1])):
            pixels[i, j] = tuple(average)

if __name__ == "__main__":
    #gui()
    image = Image.open('ultimate.png')
    mozaik(image, 30)