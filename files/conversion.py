
wav_file='E:/ai_project/voiceReq/files/efaa820c-7632-429e-87f2-f9c8ba6c1bbf.wav'

#sound = pydub.AudioSegment.from_wav(wav_file)
#sound.export('testss.wav', format="wav")

def convertDataToWav(filepath,destination):
    try:
        import pydub
        pydub.AudioSegment.converter = r"D:\pithonlib\ffmpeg-20190826-0821bc4-win64-static\bin\ffmpeg.exe"
        sound = pydub.AudioSegment.from_wav(filepath)
        sound.export(destination + '.wav', format="wav")
    except:
        print("error")




