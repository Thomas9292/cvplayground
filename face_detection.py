import os
import time
import cv2
import psutil


def get_stream(mirror=True, check_faces=False):
    '''
    Creates open-cv VideoCapture object and encodes it as bytestring
    if check_faces is true, opencv is used to detect faces and add rectangles
    '''
    FACE_DETECT_FRAMERATE = 2   # Check for faces every X frames

    camera = cv2.VideoCapture(0)

    if check_faces == 'haar':
        classifier = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    elif check_faces == 'lbp':
        script_dir = os.path.dirname(__file__)
        rel_path = "data/lbpcascade_frontalface_improved.xml"
        classifier = cv2.CascadeClassifier(os.path.join(script_dir, rel_path))

    iteration, fps = 0, 0
    faces = []
    start_time = time.time()

    while True:
        # Read image from camera file
        _, image = camera.read()

        # Mirror the image so that left side shows left on screen
        if mirror:
            image = cv2.flip(image, 1)

        # Detect the faces and annotate them with a rectangle
        if check_faces:
            if iteration % FACE_DETECT_FRAMERATE == 0:
                faces = cv2_face_detection(image, classifier)
            for (x, y, w, h) in faces:
                cv2.rectangle(image, (x, y), (x+w, y+h), (255, 100, 100), 2)

        # Add framerate and cpu usage to video
        if iteration % 10 == 0:
            cpu_percent = psutil.cpu_percent()
            fps = 10 / (time.time() - start_time)
            start_time = time.time()
        cv2.putText(image, "FPS: {}".format(round(fps, 2)),
                    (2, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 0))
        cv2.putText(image, "CPU: {}%".format(cpu_percent),
                    (2, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 0))
        
        # Increment frame counter
        iteration += 1

        # Encode the image to jpg, then to string and return binary string generator
        jpg_image = cv2.imencode('.jpg', image)[1]
        image_string = jpg_image.tostring()
        yield b'--frame\r\n' b'Content-Type: text/plain\r\n\r\n' + image_string + b'\r\n'

    del camera


def cv2_face_detection(image, classifier):
    # Convert the image to grayscale needed for detection
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    faces = classifier.detectMultiScale(
        gray_image, scaleFactor=1.1, minNeighbors=8, minSize=(30, 30))

    return faces


if __name__ == '__main__':
    # TODO: find path for lbpcascades
    pass
