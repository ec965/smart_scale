'''
Based off of code from GoogleVisionTutorials
https://github.com/DexterInd/GoogleVisionTutorials/blob/master/camera_vision_label.py
and Google Cloud documentation
https://cloud.google.com/vision/docs/quickstart-client-libraries#client-libraries-usage-python
'''

import picamera

from google.cloud import vision
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/home/pi/smartscale2-ba90efe132f7.json"

client = vision.ImageAnnotatorClient()

def takephoto():
    camera = picamera.PiCamera()
    camera.image_effect = 'colorbalance'
    camera.capture('scale_img.jpg')
    camera.close()

def main():
    takephoto()

    with open('scale_img.jpg', 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.label_detection(image)
    labels = response.label_annotations
    print('Labels: ')
    for label in labels:
        print(label.description)
    return labels

if __name__ == "__main__":
    print(main())
