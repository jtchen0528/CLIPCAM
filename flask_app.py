from flask import Flask, request, Response, render_template
import numpy as np
import cv2
import jsonpickle

app = Flask(__name__)


@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/api/grid', methods=['POST'])
def grid():
    r = request
    # convert string of image data to uint8
    nparr = np.fromstring(r.data, np.uint8)
    # decode image
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    response = {'message': 'image received. size={}x{}'.format(img.shape[1], img.shape[0])
                }

    response_pickled = jsonpickle.encode(response)

    return Response(response=response_pickled, status=200, mimetype="application/json")

if __name__ == 'main':
    app.run() #啟動伺服器