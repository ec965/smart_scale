'''
Based off of code from GoogleVisionTutorials
https://github.com/DexterInd/GoogleVisionTutorials/blob/master/camera_vision_label.py
and Google Cloud documentation
https://cloud.google.com/vision/docs/quickstart-client-libraries#client-libraries-usage-python
'''

import picamera

from google.cloud import vision

client = vision.ImageAnnotatorClient()

def takephoto():
    camera = picamera.Picamera()
    camera.capture('image.jpg')

def main():
    takephoto()

    with open('image.jpg', 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.label_detection(image)
    labels = response.label_annotations

    print('Labels: ')
    for label in labels:
        print(label.description)
