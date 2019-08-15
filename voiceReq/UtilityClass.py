import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import uuid
def getUuid():
    return str(uuid.uuid4())