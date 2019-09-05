import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import uuid
def getUuid():
    return str(uuid.uuid4())
def uploadFile(audioFile):
    from django.core.files.storage import FileSystemStorage
    from files.conversion import convertDataToWav
    extension = audioFile.name.split(".")[-1]
    responseData='error_file'
    if extension == 'wav':
        fs = FileSystemStorage()
        path_upload = 'files/'
        unique_filename = getUuid()
        responseData = fs.save(path_upload + unique_filename + '.wav', audioFile)
        convertDataToWav(path_upload + unique_filename + '.wav',unique_filename)
        print(responseData);

    return responseData
import hashlib

def computeMD5hash(my_string):
    m = hashlib.md5()
    m.update(my_string.encode('utf-8'))
    return m.hexdigest()


