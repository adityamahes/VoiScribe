import cv2
import requests
import threading
import io

cam = cv2.VideoCapture(0)
frame_width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
frame_rate = 20.0


def isopen(inp_frame, threshold):
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    mouth_cascade = cv2.CascadeClassifier('haarcascade_mcs_mouth.xml')

    # while True:
    gray = cv2.cvtColor(inp_frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(inp_frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        face_roi = gray[y + h // 2:y + h, x:x + w]
        mouths = mouth_cascade.detectMultiScale(face_roi, 1.5, 11)
        for (mx, my, mw, mh) in mouths:
            mouth_x = x + mx
            mouth_y = y + h // 2 + my
            cv2.rectangle(inp_frame, (mouth_x, mouth_y), (mouth_x + mw, mouth_y + mh), (0, 255, 0), 2)
            mouth_height = mh
            cv2.putText(inp_frame, f"Mouth Height: {mouth_height}px", (mouth_x, mouth_y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            if mouth_height < threshold:
                return False
            else:
                return True

        if cv2.waitKey(1) == ord('a'):
            break
def transcribe(file_path):
    url = "https://symphoniclabs--symphonet-vsr-modal-htn-model-upload-static-htn.modal.run/"

    with open(file_path, 'rb') as video_file:
        video = io.BytesIO(video_file.read())
        response = requests.post(url, files={'video': ('input.mp4', video, 'video/mp4')})
        print(response.text)
        with open("decoded.txt", 'a') as f:
            f.write(response.text)
segment_count = 0

while True:
    out = cv2.VideoWriter(f'segment_{segment_count}.mp4', fourcc, frame_rate, (frame_width, frame_height))

    for i in range(0, 50):
        print(".", end="")
        ret, frame = cam.read()
        out.write(frame)
        cv2.imshow('Camera', frame)
        if cv2.waitKey(1) == ord('q'):
            cam.release()
            cv2.destroyAllWindows()

        if isopen(frame, 3) and (i == 49):
            i -= 1

    out.release()
    file_name = f'segment_{segment_count}.mp4'
    transcribe(file_name)
    segment_count += 1

