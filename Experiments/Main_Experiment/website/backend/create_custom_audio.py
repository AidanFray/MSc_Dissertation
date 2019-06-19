
from pydub import AudioSegment
from flask_cors import cross_origin
import os


@cross_origin()
def gen(words):

    filePath = f"./{''.join(words)}.mp3"

    print(filePath)
    if not os.path.isfile(filePath):

        # combined = ""
        # for w in words:
        #     a = AudioSegment.from_mp3(f"audio/{w.upper()}.mp3")
        #     combined += a

        a1 = AudioSegment.from_mp3(f"audio/{words[0].upper()}.mp3")
        a2 = AudioSegment.from_mp3(f"audio/{words[1].upper()}.mp3")

        combined = a1 + a2

        combined.export(filePath, format="mp3")
        print("[!] Audio created!")

    return filePath