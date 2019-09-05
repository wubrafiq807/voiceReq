def convertDataToWav(filepath):
    import pydub
    pydub.AudioSegment.converter = r"D:\pithonlib\ffmpeg-20190826-0821bc4-win64-static\bin\ffmpeg.exe"
    sound = pydub.AudioSegment.from_wav(filepath)
    sound.export(filepath, format="wav")