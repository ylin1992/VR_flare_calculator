from base64 import decode
from flask import Flask, json, render_template, request, redirect, flash, jsonify
import cv2
import helper
import os
from flare import clc_flare, flare_helper
from flask_cors import CORS


images = {}
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

@app.route("/upload", methods=['POST'])
def upload():
    print(request.form.get('img_name'))
    if 'image' not in request.files:
        print('No file part')
        return redirect("/")
    print("***************File**************")
    for file in request.files.getlist('image'):
        print(file)
        if (len(file.filename) > 0):
            decoded_image = helper.decode_image(file)
            print(decoded_image)
            print(type(decoded_image))
            print(decoded_image.shape)
            if (len(decoded_image.shape) == 2):
                decoded_image = cv2.cvtColor(decoded_image, cv2.COLOR_GRAY2BGR)
            images[request.form.get('img_name')] = decoded_image
            images_to_show[request.form.get('img_name')] = helper.image_to_dataURI(decoded_image)
            fnames[request.form.get('img_name')] = file.filename
    return jsonify(images_to_show)


@app.route("/calculate", methods=['POST'])
def calculate():
    if len(images_to_show) != 3:
        print("Data not fully loaded yet")
        return redirect("/")
    global res, result_img
    res, result_img = clc_flare.run(images['image_w_1x'], images['image_b_1x'], images['image_w_8x'])
    res = f'{res: 2.3f}'
    result_img = helper.image_to_dataURI(result_img)
    return redirect("/")


@app.route("/upload-files", methods=['POST'])
def test_multi_upload():
    #print(request.files)
    #print(request.files.getlist('image')[0])
    tmp_image_list = []
    for file in request.files.getlist('image'):
        print("=> Processing: " + file.filename)
        decoded_image = helper.decode_image(file)
        print(decoded_image.shape)
        if (len(decoded_image.shape) == 2):
            decoded_image = cv2.cvtColor(decoded_image, cv2.COLOR_GRAY2BGR)
        tmp_image_list.append(decoded_image)
    print("Done")

    if (len(tmp_image_list) == 3):
        print("=> Start calculating")
        images_dict = flare_helper.sort_images(tmp_image_list)
        global res, result_img
        res, result_img = clc_flare.run(images_dict['white_1x'], images_dict['black_1x'], images_dict['white_8x'])
        res = f'{res: 2.3f}'
        print("Done")

    return jsonify({
        'result_image': helper.image_to_dataURI(result_img),
        'result': res
        })


if __name__ == '__main__':
    app.run(debug=True)