import cv2
import numpy as np
try:
    from base64 import encodebytes
except ImportError:
    from base64 import encodestring as encodebytes
def image_to_dataURI(image):
    content = cv2.imencode('.png', image)[1].tostring()
    encoded = encodebytes(content)
    return 'data:image/png ;base64, ' + str(encoded, 'utf-8')

def decode_image(image_file):
    return cv2.imdecode(np.fromstring(image_file.read(), np.uint8), cv2.IMREAD_UNCHANGED)