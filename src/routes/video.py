from fastapi import APIRouter, Request
from starlette.responses import StreamingResponse

import cv2

router = APIRouter()

def generate():
    # grab global references to the output frame and lock variables
    vid = cv2.VideoCapture(0)
    # loop over frames from the output stream
    while True:
        _, frame = vid.read()
        # wait until the lock is acquired
        # encode the frame in JPEG format
        (flag, encodedImage) = cv2.imencode(".jpg", frame)
        # ensure the frame was successfully encoded
        if not flag:
            continue
        # yield the output frame in the byte format
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
               bytearray(encodedImage) + b'\r\n')


@router.get('')
def get_video(request: Request):
    return StreamingResponse(generate(), media_type="multipart/x-mixed-replace;boundary=frame")