import sys
from pydub import AudioSegment
from pydub.playback import play

"""
Plays the sounds for a set of words
"""

for s in sys.argv[1:]:
    s = s.replace(",", "")
    audio = AudioSegment.from_mp3(f"../audio/{s}.mp3")
    play(audio)