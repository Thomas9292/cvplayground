#!/usr/bin/env python3
import os
from flask import Flask, render_template, url_for, Response
from face_detection import get_stream

app = Flask(__name__)


@app.route("/")
def home_page():
    return render_template('webcam.html')


@app.route("/haar_face_recognition")
def haar_face_recognition_page():
    return render_template('haar_face_recognition.html')


@app.route("/lbp_face_recognition")
def lbp_face_recognition_page():
    return render_template('lbp_face_recognition.html')


@app.route("/webcam")
def webcam():
    '''
    Calls the get_stream function and returns the response to fill img in home.html
    '''
    return Response(get_stream(check_faces=False), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route("/haar_face_detect")
def webcam_with_haar_face_detect():
    '''
    Calls the get_stream function and returns the response with face detection to
    fill img in face_recognition.html
    '''
    return Response(get_stream(check_faces='haar'), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route("/lbp_face_detect")
def webcam_with_lbp_face_detect():
    '''
    Calls the get_stream function and returns the response with face detection to
    fill img in face_recognition.html
    '''
    return Response(get_stream(check_faces='lbp'), mimetype='multipart/x-mixed-replace; boundary=frame')


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
