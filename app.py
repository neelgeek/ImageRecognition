from flask import Flask
from flask import request,Response
import jsonpickle
import numpy as np
import cv2
import base64

app = Flask(__name__)


@app.route("/getCount",methods=['POST'])
def postImg():
    r = request
    img = r.files['image']   # Add file field name as 'image'
    imgBin = img.read()
    nparr = np.fromstring(imgBin, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    response = {'message': 'image received. size={}x{}'.format(img.shape[1], img.shape[0])
                }

    response_pickled = jsonpickle.encode(response)

    return Response(response=response_pickled, status=200, mimetype="application/json")

@app.route("/",methods=['GET'])
def default():
    return "Welcome !"

if __name__ == '__main__':
    print("App Started")
    app.run(debug=True)

