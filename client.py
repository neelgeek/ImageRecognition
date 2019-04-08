# import pygame
# import pygame.camera
import time
import requests
from envoirment import Env
from tkinter import *
from PIL import ImageTk, Image

'''
pygame.camera.init()
pygame.camera.list_cameras()
cam = pygame.camera.Camera("/dev/video0", (640, 480))
cam.start()
time.sleep(0.1)                 
img = cam.get_image()
pygame.image.save(img, "test.jpg")
cam.stop()
'''
t_red = 10
e = Env(0.7, 0.1, 0.1)
imagelist = ['test1.jpg', 'test2.jpg', 'test3.jpg', 'test4.jpg']
url = "http://35.200.141.144:5000/getCount"
i = 0


def req(j):
    global i
    global image_id
    global canvas
    fin = open(imagelist[j], "rb")
    files = {'image': fin}
    try:
        print("Sending Request to Server for", imagelist[i])
        r = requests.post(url, files=files)
        data = r.json()
        bus = 0
        truck = 0
        car = data["b'car'"]
        if "b'bus'" in data:
            bus = data["b'bus'"]
        if "b'truck'" in data:
            truck = data["b'truck'"]
        res = "car: ",car," bus: ",bus," truck: ",truck
        #ResponseVal.delete(0,END)
        #ResponseVal.insert(0,res)
        weighted_sum = car * 2 + bus * 4 + truck * 4;
        print("Weighted Sum =", weighted_sum)
        WeightedVal.delete(0, END)
        WeightedVal.insert(0, weighted_sum)
        t_green = e.red_traffic(weighted_sum)
        print("Green Time =", t_green)
        GreenVal.delete(0, END)
        GreenVal.insert(0, t_green)
        # time.sleep(t_green/10)
        print("Red Time =", t_red)
        RedVal.delete(0, END)
        RedVal.insert(0, t_red)
        print("\n")
        #time.sleep(t_red/3)
        # canvas.delete("all")
        update_image(j+1)
        #canvas.pack()
        i = i + 1
        if (i == 4):
            i = 0
            # gui(i)
    finally:
        fin.close()
def update_image(j):
    global img
    try:
        img = ImageTk.PhotoImage(Image.open(imagelist[j]))
        canvas.itemconfigure(image_id, image=img)
    except IOError:  # missing or corrupt image file
        img = None


if __name__ == "__main__":
    root = Tk()
    root.title("Smart Signal")
    frame = Frame(root)
    frame.pack(fill=X)
    canvas = Canvas(frame)
    img = ImageTk.PhotoImage(Image.open(imagelist[i]))
    image_id = canvas.create_image(40, 60, anchor=NW, image=img)
    canvas.pack()
    button1 = Button(frame, text='Send', fg='black', bg='yellow', command=lambda: req(i), height=1, width=7)
    button1.pack()
    # frame3 = Frame(root)
    # frame3.pack(fill=X)
    # Response = Label(frame3, text='Response:')
    # Response.configure(font=('Verdana', 14, 'bold'))
    # Response.pack(side=LEFT, padx=5, pady=5)
    # ResponseVal = Entry(frame3, text='')
    # ResponseVal.pack(fill=X, padx=5, expand=True)
    frame4 = Frame(root)
    frame4.pack(fill=X)
    Weighted = Label(frame4, text='Weighted Sum:')
    Weighted.configure(font=('Verdana', 14, 'bold'))
    Weighted.pack(side=LEFT, padx=5, pady=5)
    WeightedVal = Entry(frame4, text='')
    WeightedVal.pack(fill=X, padx=5, expand=True)
    frame1 = Frame(root)
    frame1.pack(fill=X)
    Green = Label(frame1, text='Green:')
    Green.configure(font=('Verdana', 14, 'bold'))
    Green.pack(side=LEFT, padx=5, pady=5)
    GreenVal = Entry(frame1, text='')
    GreenVal.pack(fill=X, padx=5, expand=True)
    frame2 = Frame(root)
    frame2.pack(fill=X)
    Red = Label(frame2, text='Red:')
    Red.configure(font=('Verdana', 14, 'bold'))
    Red.pack(side=LEFT, padx=5, pady=5)
    RedVal = Entry(frame2, text='')
    RedVal.pack(fill=X, padx=5, expand=True)
    root.mainloop()




