from gtts import gTTS
import os

while True:
    with open("decoded.txt", 'r') as f:
        contents = f.read()
        language = "en"
        my_Obj = gTTS(text=contents, lang=language, slow=False)

        my_Obj.save("voice.mp3")

        os.system("voice.mp3")
