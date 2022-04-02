from fastapi import APIRouter, HTTPException, Request, Response, status
from starlette.responses import StreamingResponse

import cv2

router = APIRouter()

def generate(app):
    app.video = cv2.VideoCapture(0)
    while True:
        _, frame = app.video.read()
        (flag, encodedImage) = cv2.imencode(".jpg", frame)
        if not flag:
            continue
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
               bytearray(encodedImage) + b'\r\n')


@router.get('')
def get_video(request: Request):
    return StreamingResponse(generate(request.app), media_type="multipart/x-mixed-replace;boundary=frame")


@router.get('/stop')
def stop_video(request: Request):
    if not request.app.video:
        raise HTTPException(status.HTTP_409_CONFLICT, 'Nothing to stop!')
    request.app.video.release()
    request.app.video = None
    return Response(status_code=status.HTTP_200_OK)