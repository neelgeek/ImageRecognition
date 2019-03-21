#import pygame
#import pygame.camera
import time
import requests
from envoirment import Env 
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
t_red=10
e = Env(0.7,0.1,0.1)
imagelist= ['test1.jpg','test2.jpg','test3.jpg','test4.jpg']
url = "http://35.200.141.144:5000/getCount"
i=0
def req(i):
    fin = open(imagelist[i],"rb")
    files = {'image': fin }
    try:
        print("Sending Request to Server for",imagelist[i])
        r = requests.post(url,files=files)
        data = r.json()
        bus = 0
        truck = 0
        car = data["b'car'"]
        if "b'bus'" in data:
            bus = data["b'bus'"]
        if "b'truck'" in data:
            truck = data["b'truck'"]
        weighted_sum = car*2 + bus *4+truck*4;
        print("Weighted Sum =",weighted_sum)
        t_green=e.red_traffic(weighted_sum)
        print("Green Time =",t_green)
        time.sleep(t_green/10)
        print("Red Time =",t_red)
        print("\n")
        time.sleep(t_red/3)
        i=i+1
        if(i==4):
            i=0
        req(i)
    finally:
        fin.close()

req(i)
