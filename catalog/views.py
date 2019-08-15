
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from catalog.APIResponse import Utility
from catalog.recognizeVoice import getAudioToText
from voiceReq.UtilityClass import *
from catalog.SiteFuntion import *
from catalog.CustomSQL import getResultsBySQL
import uuid
@csrf_exempt
def updateDelOrGetSingleVoiceReq(request, id=''):
    jsone = Utility()
    if request.method == 'PUT':
     var=2222
     response_data = {}
     response_data['result'] = var
     response_data['message'] = 'Some error message'
     return HttpResponse(json.dumps(response_data), content_type="application/json")
    elif request.method == 'GET':
        jsone.message = 'Success'
        jsone.result=getResultsBySQL('SELECT * FROM `voice_req` WHERE voice_req_id="'+id+'"')
        return HttpResponse(jsone.toJson(), content_type="application/json")
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
        user_id = request.GET.get('user_id')
        print(user_id)
        if not user_id:
            jsone.message = 'You can not keep user_id empty as parameter'
            jsone.error = True
            jsone.code = 503
            return HttpResponse(jsone.toJson(), content_type="application/json")
        else:
            query = 'SELECT * from voice_req WHERE user_id="' + user_id + '"'
            jsone.result=getResultsBySQL(query)
            jsone.message='success'
            return HttpResponse(jsone.toJson(), content_type="application/json")

    elif request.method == 'POST':
        user_id = request.POST.get('user_id')
        record_start_time = request.POST.get('record_start_time')
        record_end_time = request.POST.get('record_end_time')
        record_type=request.POST.get('record_type')
        if bool(request.FILES.get('audioFile', False)) == False or not user_id or not record_start_time or not record_end_time or not record_type:
            jsone.message = 'You can not keep record_type,audioFile,user_id,record_start_time,record_end_time parameters are empty'
            jsone.error = True
            jsone.code = 503
            return HttpResponse(jsone.toJson(), content_type="application/json")
        else:
            from django.core.files.storage import FileSystemStorage
            audioFile = request.FILES['audioFile']
            extension=audioFile.name.split(".")[-1]
            if extension =='wav':
                fs = FileSystemStorage()
                path_upload = 'files/'
                unique_filename = getUuid()
                filename = fs.save(path_upload + unique_filename + '.wav', audioFile)
                text=getAudioToText(BASE_DIR+'/'+filename)
                jsone.result=processText(record_type,user_id,record_start_time,record_end_time,text,filename)
                jsone.message='Uploaded successfully'
                return HttpResponse(jsone.toJson(), content_type="application/json")
            else:
                jsone.message = 'Only wav audio file is allowed'
                jsone.error = True
                jsone.code=503
                return HttpResponse(jsone.toJson(), content_type="application/json")

    else:
        jsone.message = 'The request method '+request.method+' is not allowed'
        jsone.error = True
        jsone.code = 405
        return HttpResponse(jsone.toJson(), content_type="application/json")