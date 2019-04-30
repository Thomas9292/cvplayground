#!/usr/bin/env python3
import os
import cv2
from flask import Flask, render_template, url_for, Response, request
from face_detection import face_detection

app = Flask(__name__)


@app.route("/")
def hello():
    return render_template('home.html')


def get_webcam(mirror=True, check_faces=True):
    '''
    Creates open-cv VideoCapture object and encodes it as bytestring
    '''
    camera = cv2.VideoCapture(0)

    while True:
        _, image = camera.read()
        if mirror:
            image = cv2.flip(image, 1)
        
        if check_faces:
            faces = face_detection(image)
            for (x, y, w, h) in faces:
                cv2.rectangle(image, (x, y), (x+w, y+h), (255, 100, 100), 2)

        jpg_image = cv2.imencode('.jpg', image)[1]
        image_string = jpg_image.tostring()
        yield b'--frame\r\n' b'Content-Type: text/plain\r\n\r\n' + image_string + b'\r\n'

    del camera


@app.route("/webcam")
def webcam():
    '''
    Calls the get_webcam function and returns the response to fill img in home.html
    '''
    return Response(get_webcam(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.context_processor
def override_url_for():
    '''
    Code to override url_for to expire css files. Tells browser to update style when
    changes have been made to css
    '''
    return dict(url_for=dated_url_for)


def dated_url_for(endpoint, **values):
    '''
    Attaches timestamp to url
    '''
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)


if __name__ == '__main__':
    app.run(debug=True, threaded=True)
