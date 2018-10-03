from flask import Flask
from flask import request,Response
import jsonpickle
import numpy as np
import cv2
import logging
from logging.handlers import RotatingFileHandler
from time import strftime
from flask import Flask, url_for, send_from_directory, request
from werkzeug import secure_filename
import os
import json
from darknet import detectormain as dm



app = Flask(__name__)

PROJECT_HOME = os.path.dirname(os.path.realpath(__file__))
UPLOAD_FOLDER = '{}/uploads/'.format(PROJECT_HOME)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/getCount",methods=['POST'])
def postImg():
    r = request
    img = r.files['image']   # Add file field name as 'image'
    img_name = secure_filename(img.filename)
    saved_path = os.path.join(app.config['UPLOAD_FOLDER'], img_name)
    img.save(saved_path)
    results = dm.detect(saved_path) 
    '''
    response = {'message': 'image received. size={}x{}'.format(img.shape[1], img.shape[0])
                }
    '''
    response_pickled = jsonpickle.encode(results)

    return Response(response=response_pickled, status=200, mimetype="application/json")

@app.route("/",methods=['GET'])
def default():
    return "Welcome !"

@app.after_request
def after_request(response):
    timestamp = strftime('[%Y-%b-%d %H:%M]')
    logger.error('%s || %s || %s || %s || %s || %s', timestamp, request.remote_addr, request.method, request.scheme, request.full_path, response.status)
    return response


if __name__ == '__main__':
    handler = RotatingFileHandler('app.log', maxBytes=100000, backupCount=3)
    logger = logging.getLogger('tdm')
    logger.setLevel(logging.ERROR)
    logger.addHandler(handler)
    print("App Started")
    app.run()

