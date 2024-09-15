import io
import requests


def transcribe(file_path):
    url = "https://symphoniclabs--symphonet-vsr-modal-htn-model-upload-static-htn.modal.run"

    with open(file_path, 'rb') as video_file:
        print("hey")
        # video = io.BytesIO(video_file.read())
        # print("hello")
        # response = requests.post(url, files={'video': ('segment_0.mp4', video, 'video/mp4')})
        # print(response.text)

        with open(file_path, 'rb') as video_file:
            video = io.BytesIO(video_file.read())

        response = requests.post(url, files={'video': ('segment_0.mp4', video, 'video/mp4')})
        #print(response.text)
        return(response.text)


print(transcribe("segment_0.mp4"))
