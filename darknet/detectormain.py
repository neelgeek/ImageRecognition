"""Detector functions with different imread methods"""

import ctypes
from darknet.darknet_libwrapper import *

import time



def array_to_image(arr):
    arr = arr.transpose(2,0,1)
    c = arr.shape[0]
    h = arr.shape[1]
    w = arr.shape[2]
    arr = (arr/255.0).flatten()
    data = c_array(ctypes.c_float, arr)
    im = IMAGE(w,h,c,data)
    return im

def _detector(net, meta, image, thresh=.5, hier=.5, nms=.45):
    cuda_set_device(0)
    num = ctypes.c_int(0)
    num_ptr = ctypes.pointer(num)
    network_predict_image(net, image)
    dets = get_network_boxes(net, image.w, image.h, thresh, hier, None, 0, num_ptr)
    num = num_ptr[0]
    if (nms):
         do_nms_sort(dets, num, meta.classes, nms)

    res = []
    for j in range(num):
        for i in range(meta.classes):
            if dets[j].prob[i] > 0:
                b = dets[j].bbox
                # Notice: in Python3, mata.names[i] is bytes array from c_char_p instead of string
                res.append((meta.names[i], dets[j].prob[i], (b.x, b.y, b.w, b.h)))
    res = sorted(res, key=lambda x: -x[1])
    free_detections(dets, num)
    return res

# Darknet
net = load_network("/home/neel/ImageRecognition/darknet/cfg/yolov3.cfg", "/home/neel/ImageRecognition/darknet/yolov3.weights", 0)
meta = get_metadata("/home/neel/ImageRecognition/darknet/cfg/coco.data")
#im = load_image_color('traffic.jpg', 0, 0)

def makecount(result):
	objects = dict()
	
	for obj in result:
		key = str(obj[0])
		if key in objects:
			objects[key]+=1
		else:
			objects[key]=1
	return objects
		
			


def detect(imgPath):
	im = load_image_color(imgPath, 0, 0)
	start = time.time()	
	result = _detector(net, meta, im)
	end = time.time()
	print("Execution time: ",(end-start))	
	return(makecount(result))



