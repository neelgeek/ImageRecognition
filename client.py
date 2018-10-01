import pygame
import pygame.camera
import time
import requests

pygame.camera.init()
pygame.camera.list_cameras()
cam = pygame.camera.Camera("/dev/video0", (640, 480))
cam.start()
time.sleep(0.1)                 
img = cam.get_image()
pygame.image.save(img, "test.jpg")
cam.stop()

url = "http://139.59.29.92:5000/getCount"
fin = open("test.jpg","rb")
files = {'image': fin }
try:
    r = requests.post(url,files=files)
    print(r.text)
finally:
    fin.close()
