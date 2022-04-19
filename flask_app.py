from flask import Flask, request, render_template, redirect, url_for, send_file
from flask_cors import CORS
import numpy as np
import cv2
from clipcam import api
from PIL import Image
import os
from werkzeug.utils import secure_filename
import io

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png']
CORS(app)

@app.errorhandler(413)
def too_large(e):
    return "File is too large", 413

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check-server', methods=['POST'])
def index():
    return True

@app.route('/single', methods=['POST'])
def single():
    uploaded_file = request.files['file']
    CLIP_MODEL_NAME = request.form['clip_model_name']
    CAM_MODEL_NAME = request.form['cam_model_name']
    GUIDING_TEXT = request.form['guiding_text']
    ATTACK = request.form['attack']
    DISTILL_NUM = request.form['distill_num']

    if ATTACK == 'None':
        ATTACK = None
    DISTILL_NUM = int(DISTILL_NUM)

    img = Image.open(uploaded_file.stream)

    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS']:
            return "Invalid image", 400

    final_img = api(CLIP_MODEL_NAME, CAM_MODEL_NAME, [img], GUIDING_TEXT, DISTILL_NUM, ATTACK)

    file_object = io.BytesIO()
    final_img.save(file_object, 'PNG')
    file_object.seek(0)

    return send_file(file_object, mimetype='image/PNG')

@app.route('/grid', methods=['POST'])
def grid():
    uploaded_file_1 = request.files['file1']
    uploaded_file_2 = request.files['file2']
    uploaded_file_3 = request.files['file3']
    uploaded_file_4 = request.files['file4']
    CLIP_MODEL_NAME = request.form['clip_model_name']
    CAM_MODEL_NAME = request.form['cam_model_name']
    GUIDING_TEXT = request.form['guiding_text']
    ATTACK = request.form['attack']
    DISTILL_NUM = request.form['distill_num']

    if ATTACK == 'None':
        ATTACK = None
    DISTILL_NUM = int(DISTILL_NUM)

    img_1 = Image.open(uploaded_file_1.stream)
    img_2 = Image.open(uploaded_file_2.stream)
    img_3 = Image.open(uploaded_file_3.stream)
    img_4 = Image.open(uploaded_file_4.stream)
    final_img = api(CLIP_MODEL_NAME, CAM_MODEL_NAME, [img_1, img_2, img_3, img_4], GUIDING_TEXT, DISTILL_NUM, ATTACK)

    file_object = io.BytesIO()
    final_img.save(file_object, 'PNG')
    file_object.seek(0)

    return send_file(file_object, mimetype='image/PNG')

@app.route('/download')
def downloadFile ():
    #For windows you need to use drive name [ex: F:/Example.pdf]
    path = "imgs/images.zip"
    return send_file(path, as_attachment=True)

if __name__ == 'main':
    app.run() #啟動伺服器