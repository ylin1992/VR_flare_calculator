import cv2
try:
    from base64 import encodebytes
except ImportError:
    from base64 import encodestring as encodebytes
def image_to_dataURI(image):
    content = cv2.imencode('.png', image)[1].tostring()
    encoded = encodebytes(content)
    return 'data:image/png ;base64, ' + str(encoded, 'utf-8')