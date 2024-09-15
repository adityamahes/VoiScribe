import cv2
import requests
import io
import google.generativeai as genai
import os
from gtts import gTTS
import time
import pygame.mixer

pygame.mixer.init()



cam = cv2.VideoCapture(0)
frame_width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('../Hack The North Submission/output.mp4', fourcc, 20.0, (frame_width, frame_height))


count = 0
while True:
    count += 1
    ret, frame = cam.read()

    # Write the frame to the output file
    out.write(frame)
    # Display the captured frame
    cv2.imshow('Camera', frame)

    # Press 'q' to exit the loop
    if cv2.waitKey(1) == ord('q'):
        break

# Release the video and writer objects before transcription
cam.release()
out.release()
# cv2.destroyAllWindows()


def transcribe(file_path):
    url = "https://symphoniclabs--symphonet-vsr-modal-htn-model-upload-static-htn.modal.run/"

    with open(file_path, 'rb') as video_file:
        video = io.BytesIO(video_file.read())
        response = requests.post(url, files={'video': ('input.mp4', video, 'video/mp4')})
        print(response)
        return (response.text)


def gemini(input):

    os.environ["API_KEY"] = 'AIzaSyCl3_jsnPlvI1Wr5rhT8z1IoFDuGcbZVzM'
    genai.configure(api_key=os.environ["API_KEY"])

    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    response = model.generate_content(input)
    print(response.text)



# Transcribe and save the result
transcription = transcribe("../Hack The North Submission/output.mp4").strip('".')
a = transcription.split()
print(a)
for i in range(len(a)):
    my_Obj = gTTS(text=a[i], lang="en", slow=False)
    my_Obj.save(rf'vid_segments\{i}.mp3')
    pygame.mixer.Sound(rf"vid_segments\{i}.mp3").play
    time.sleep(1.5)
    if cv2.waitKey(1) == ord('w'):
        a[i] = gemini(f"Give me one word similar phonetically sounding word for {a[i]} that the mute person might have meant")
        i -= 1







