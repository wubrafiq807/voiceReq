
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from catalog.APIResponse import Utility
from catalog.recognizeVoice import *
from voiceReq.constant import *
from catalog.CustomSQL import getResultsBySQL
import uuid
@csrf_exempt
def updateDelOrGetSingleVoiceReq(request, num=1):
    if request.method == 'PUT':
     var=2222
     response_data = {}
     response_data['result'] = var
     response_data['message'] = 'Some error message'
     return HttpResponse(json.dumps(response_data), content_type="application/json")
    elif request.method == 'GET':
        var = 2222
        response_data = {}
        response_data['result'] = var
        response_data['message'] = 'Some error message'
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    elif request.method == 'DELETE':
        var = 2222
        response_data = {}
        response_data['result'] = var
        response_data['message'] = 'Some error message'
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        from rest_framework.exceptions import ValidationError
        raise ValidationError("Invalid request", 403)

@csrf_exempt
def getAllOrSaveSigbleVoiceReq(request):
    jsone = Utility()
    if request.method == 'GET':
        var = 2222
        response_data = {}
        response_data['result'] = var
        response_data['message'] = 'Some error message'
        return HttpResponse(json.dumps(response_data), content_type="application/json")

    elif request.method == 'POST':
        user_id=request.POST['user_id']
        record_start_time=request.POST['record_start_time']
        record_end_time=request.POST['record_end_time']
        if bool(request.FILES.get('audioFile', False)) == False or not user_id.strip() or not record_start_time.strip() or not record_end_time.strip():
            #jsone=Utility()
            jsone.message = 'You can not keep audioFile,user_id,record_start_time,record_end_time fields are empty'
            jsone.error = True
            return HttpResponse(jsone.toJson(), content_type="application/json")
        else:
            from django.core.files.storage import FileSystemStorage
            audioFile = request.FILES['audioFile']
            extension=audioFile.name.split(".")[-1]
            if extension =='wav':
                fs = FileSystemStorage()
                path_upload = 'files/'
                unique_filename = str(uuid.uuid4())
                filename = fs.save(path_upload + unique_filename + '.wav', audioFile)
                text=getAudioToText(BASE_DIR+'/'+filename)
                names=extract_names(text)
                emails=extract_email_addresses(text)
                phones=extract_phone_numbers(text)
                query_result=getResultsBySQL('SELECT * FROM `voice_req`')
                print(query_result)
                result=query_result
                jsone.result=result
                print(jsone)
                jsone.message='Uploaded success'
                return HttpResponse(jsone.toJson(), content_type="application/json")
            else:
                jsone.message = 'Only wav audio file is allowed'
                jsone.error = True
                return HttpResponse(jsone.toJson(), content_type="application/json")

    else:
        from rest_framework.exceptions import ValidationError
        raise ValidationError("Invalid request", 403)