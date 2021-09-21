from flask import Flask, render_template
import cv2
import helper
app = Flask(__name__)

@app.route("/")
def index():
    img = cv2.imread('./static/images/profile.png')
    data_uri = helper.image_to_dataURI(img)
    return render_template("index.html", image_to_show=data_uri)

if __name__ == '__main__':
    app.run(debug=True)