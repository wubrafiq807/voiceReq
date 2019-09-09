
from os import path
from pydub import AudioSegment

# files
src = "transcript.mp3"
dst = "test.wav"

def convertDataToWav(filepath,destination):


    # convert wav to mp3
    #AudioSegment.ffmpeg = "C:\ffmpeg\bin\ffmpeg.exe"
    #sound = AudioSegment.from_mp3(filepath)
    from pydub import silence, AudioSegment
    from pathlib import Path

    import os, sys

    print(sys.version)

    # AudioSegment.ffmpeg = os.getcwd()+"\\ffmpeg\\bin\\ffmpeg.exe"

    AudioSegment.converter = r"C:\\ffmpeg\\bin\\ffmpeg.exe"
    AudioSegment.ffprobe = r"C:\\ffmpeg\\bin64\\ffprobe.exe"

    # print (AudioSegment.converter)
    # print (AudioSegment.ffprobe)

    my_file = Path(filepath)

    print('ID1 : %s' % my_file)

    audio = AudioSegment.from_mp3(my_file)
    audio.export(destination+".wav", format="wav")




#convertDataToWav(src,dst)