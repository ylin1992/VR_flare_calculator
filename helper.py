import cv2
import base64

def image_to_dataURI(image):
    content = cv2.imencode('.png', image)[1].tostring()
    encoded = base64.encodestring(content)
    return 'data:image/png ;base64, ' + str(encoded, 'utf-8')