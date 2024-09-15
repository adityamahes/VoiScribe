import cv2
import requests
import io
import google.generativeai as genai
import os
from gtts import gTTS
# import pygame.mixer
#
# pygame.mixer.init()


overlay_image = cv2.imread('zoom2.png', cv2.IMREAD_UNCHANGED)

if overlay_image is None:
    raise ValueError("Error loading overlay image. Please check the file path and file format.")

cam = cv2.VideoCapture(0)
frame_width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (frame_width, frame_height))


count = 0
while True:
    count += 1
    ret, frame = cam.read()


    ret, frame = cam.read()

    if not ret or frame is None:
        print("Error capturing frame from camera.")
        break


    if frame is None or overlay_image is None:
        print("Frame or overlay image is None")
        break


    overlay_resized = cv2.resize(overlay_image, (frame.shape[1], frame.shape[0]))


    if overlay_resized.shape[2] == 4:

        overlay_rgb = overlay_resized[:, :, :3]
        alpha_channel = overlay_resized[:, :, 3] / 255.0

        for c in range(0, 3):
            frame[:, :, c] = (alpha_channel * overlay_rgb[:, :, c] + (1 - alpha_channel) * frame[:, :, c])
    else:
        x_offset = 0
        y_offset = 0
        frame[y_offset:y_offset + overlay_resized.shape[0],
        x_offset:x_offset + overlay_resized.shape[1]] = overlay_resized

    out.write(frame)
    cv2.namedWindow('Camera', cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty('Camera', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    cv2.imshow('Camera', frame)

    if cv2.waitKey(1) == ord('q'):
        break
cam.release()
out.release()
cv2.destroyAllWindows()


def transcribe(file_path):
    url = "https://symphoniclabs--symphonet-vsr-modal-htn-model-upload-static-htn.modal.run/"

    with open(file_path, 'rb') as video_file:
        video = io.BytesIO(video_file.read())
        response = requests.post(url, files={'video': ('input.mp4', video, 'video/mp4')})
        print(response)
        return (response.text)


transcription = transcribe("output.mp4")


my_Obj = gTTS(text=transcription, lang="en", slow=False)

my_Obj.save("voice.mp3")

os.system("voice.mp3")
