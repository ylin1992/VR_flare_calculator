from flask import Flask, render_template, request, redirect, flash
import cv2
import helper
import os
from flare import clc_flare

images = {}
fnames = {}
images_to_show = {}
result_img = None
res = None


app = Flask(__name__)
UPLOAD_FOLDER = os.path.basename('uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "super secret key"
app.static_folder = 'static'



@app.route("/")
def index():
    #img = cv2.imread('./static/images/profile.png')
    #data_uri = helper.image_to_dataURI(img)
    return render_template("index.html", images_to_show=images_to_show, fname=fnames, res=res, result_img=result_img)


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
    return redirect("/")


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


if __name__ == '__main__':
    app.run(debug=True)