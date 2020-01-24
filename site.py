# -*- coding: utf-8 -*-
"""
Created on Fri Jan  3 20:30:29 2020

@author: ZHOU_YuZHAO
"""
from tkinter import *
import numpy as np          # This module is used for matrix operation
import csv
import matplotlib.pyplot
import read

# Using an agent to read raster file
readFile = read.Read()

root = Tk()


G, T, P = 0, 0, 0

# Using the function to get value
geology = readFile.readFromFile("best.geology")
transport = readFile.readFromFile("best.mway")
population = readFile.readFromFile("best.pop")
m = None

# This is a flag, control whether highlight
enable = False

shape = geology.shape

matplotlib.use('TkAgg')
fig = matplotlib.pyplot.figure()
canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(fig, master=root)
canvas._tkcanvas.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

# Uptate the image while draging the scroll bar 
def update():
    global G, T, P, m, enable
    total = G+T+P
# Assign the weight
    if total == 0:
        m = np.zeros(shape)
    else:
        m = (G/total)*geology + (T/total)*transport + (P/total) * population    
    fig.clear()
    matplotlib.pyplot.clf()
# Not highlight
    if not enable:
        matplotlib.pyplot.imshow(m)
# When highlight, all the other areas would be shown as grey
    else:
        matplotlib.pyplot.imshow(m, cmap=matplotlib.pyplot.cm.gray)

    if enable:
        top10 = np.percentile(m, 90)
        mask = np.array(np.where(m >= top10, 127, 0))
        blue = np.array([np.zeros(shape), np.zeros(shape), np.ones(shape)*255, np.ones(shape)*mask])
        blue = np.transpose(blue, axes=(1, 2, 0))
        matplotlib.pyplot.imshow(blue.astype('uint8'))

    matplotlib.pyplot.imshow(m, cmap=matplotlib.pyplot.cm.gray)
 #   matplotlib.pyplot.draw()
    canvas.draw()
# Overlay the three layers and display the image based on the weight obtained from the scale bar
def setG(text):
    global G
    G = int(text)
    update()
def setT(text):
    global T
    T = int(text)
    update()
def setP(text):
    global P
    P = int(text)
    update()

# to save the weighted map as txt format
def save():
    global file_path
# Ask the saving path
    file_path = filedialog.asksaveasfilename(title=u'Save file',filetypes = [(".txt","TXT")])
    print('Save this file to:：', file_path)
# Write the content into txt
    with open(file_path + ".txt", mode='a+', encoding="UTF-8") as f:
        for line in range(m.shape[0]):
            strline = ",".join([str(int(value)) for value in m[line]]) + "\n"
            f.write(strline)
# Inform after customer save successfully
    dialog.Dialog(None, {'title': 'File Modified', 'text': 'Save Successful', 'bitmap': 'warning', 'default': 0,
                         'strings': ('OK', 'Cancle')})
    print('Save Successful')

# Change the flag when highlight
def highlight():
    global enable
    enable = not enable
    update()

# Create a GUI to operate
menu = Menu(root)
root.config(menu = menu)
file_menu = Menu(menu)
menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Save", command=save)

highlight_menu = Menu(menu)
menu.add_cascade(label="Highlight", menu=highlight_menu)
highlight_menu.add_command(label="Enable/Disable", command=highlight)

# Display the image
Label(root, text="Geology").pack()
Scale(root,from_=0,to=100,resolution=1,length=400, orient=HORIZONTAL, command=setG).pack()
Label(root, text="Transport").pack()
Scale(root,from_=0,to=100,resolution=1,length=400, orient=HORIZONTAL, command=setT).pack()
Label(root, text="Population").pack()
Scale(root,from_=0,to=100,resolution=1,length=400, orient=HORIZONTAL, command=setP).pack()
mainloop()

