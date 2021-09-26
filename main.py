from base64 import decode
from flask import Flask, json, render_template, request, redirect, flash, jsonify
import cv2
import helper
import os
from flare import clc_flare, flare_helper
from flask_cors import CORS


images = []
fnames = {}
images_to_show = {}
result_img = None
res = None


app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER = os.path.basename('uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "super secret key"
app.static_folder = 'static'



@app.route("/")
def index():
    #img = cv2.imread('./static/images/profile.png')
    #data_uri = helper.image_to_dataURI(img)
    #return render_template("index.html", images_to_show=images_to_show, fname=fnames, res=res, result_img=result_img)
    return {'this': 'is a test'}


@app.route("/upload-files", methods=['POST'])
def test_multi_upload():
    #print(request.files)
    #print(request.files.getlist('image')[0])
    global images
    if len(images) == 0:
        print("=> fetching data from frontend...")
        for file in request.files.getlist('image'):
            print("=> Processing: " + file.filename)
            decoded_image = helper.decode_image(file)
            print(decoded_image.shape)
            if (len(decoded_image.shape) == 2):
                decoded_image = cv2.cvtColor(decoded_image, cv2.COLOR_GRAY2BGR)
            images.append(decoded_image)
        print("=> fetching done")
    res, result_img = calculate();
    images = []

    return jsonify({
        'result_image': helper.image_to_dataURI(result_img),
        'result': res
        })

def calculate():
    global images
    if (len(images) == 3):
        print("=> Start calculating")
        images_dict = flare_helper.sort_images(images)
        global res, result_img
        res, result_img = clc_flare.run(images_dict['white_1x'], images_dict['black_1x'], images_dict['white_8x'])
        res = f'{res: 2.3f}'
        print("Done")
    
    return res, result_img

@app.route("/load-sample", methods=['GET'])
def load_sample_images():
    print("=> loading sample images from database...")
    base64_images = []
    for file in ['./flare/blk_1x.png', './flare/white_1x.png', './flare/white_8x.png']:
        im = cv2.imread(file)
        base64_images.append({'image':helper.image_to_dataURI(cv2.resize(im, (0,0), fx=0.25, fy=0.25))})
        images.append(im)
    return jsonify(base64_images)

if __name__ == '__main__':
    app.run(debug=True)