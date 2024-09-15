import cv2
import requests
import io
import google.generativeai as genai
import os
from gtts import gTTS


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
    response = model.generate_content("Correct this broken english into good english (give possible words for words you are unsure meaning of)   : " + input)
    print(response.text)


# Transcribe and save the result
transcription = transcribe("../Hack The North Submission/output.mp4")
# contents = gemini(transcription)

my_Obj = gTTS(text=transcription, lang="en", slow=False)

my_Obj.save("voice.mp3")

os.system("../Hack The North Submission/voice.mp3")

