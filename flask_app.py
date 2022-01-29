from flask import Flask, request, render_template, redirect, url_for, send_file
import numpy as np
import cv2
from clipcam import api
from PIL import Image
import os
from werkzeug.utils import secure_filename
import io

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 8 * 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png']

@app.errorhandler(413)
def too_large(e):
    return "File is too large", 413

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/single', methods=['POST'])
def single():
    uploaded_file = request.files['file']
    img = Image.open(uploaded_file.stream)

    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS']:
            return "Invalid image", 400

    final_img = api('ViT-B/16', 'GradCAM', [img], 'white trunks')

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
    img_1 = Image.open(uploaded_file_1.stream)
    img_2 = Image.open(uploaded_file_2.stream)
    img_3 = Image.open(uploaded_file_3.stream)
    img_4 = Image.open(uploaded_file_4.stream)
    final_img = api('ViT-B/16', 'GradCAM', [img_1, img_2, img_3, img_4], 'white trunks')

    file_object = io.BytesIO()
    final_img.save(file_object, 'PNG')
    file_object.seek(0)

    return send_file(file_object, mimetype='image/PNG')

if __name__ == 'main':
    app.run() #啟動伺服器