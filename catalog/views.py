
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from catalog.APIResponse import Utility
from catalog.recognizeVoice import getAudioToText
from voiceReq.UtilityClass import *
from catalog.SiteFuntion import *
from catalog.CustomSQL import getResultsBySQL, checkUserExist

import uuid
@csrf_exempt
def updateDelOrGetSingleVoiceReq(request, id=''):
    jsone = Utility()
    if request.method == 'GET':
        jsone.message = 'Success'
        results=getResultsBySQL('SELECT * FROM `voice_req` WHERE voice_req_id="'+id+'"')
        if len(list(results))>0:
            finalData=results[0]
            finalData['phones']=getResultsBySQL("SELECT * FROM `phone` WHERE voice_req_id='"+id+"'")
            finalData['names'] = getResultsBySQL("SELECT * FROM `name` WHERE voice_req_id='" + id + "'")
            finalData['email'] = getResultsBySQL("SELECT * FROM `email` WHERE voice_req_id='" + id + "'")

            if finalData['record_type'] ==2:
                callerReceiverInfo=getResultsBySQL("SELECT * FROM `receiver_caller` WHERE voice_req_id='"+id+"'")
                if len(list(callerReceiverInfo)) > 0:
                    finalData['caller_phone_no'] = callerReceiverInfo[0]['caller_phone_no']
                    finalData['receiver_phone_no'] = callerReceiverInfo[0]['receiver_phone_no']

            jsone.result = finalData
        else:
            jsone.message='No record found in database'

        return HttpResponse(jsone.toJson(), content_type="application/json")
    elif request.method == 'DELETE':
        var = 2222
        response_data = {}
        response_data['result'] = var
        response_data['message'] = 'Some error message'
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        jsone.message = 'The request method ' + request.method + ' is not allowed'
        jsone.error = True
        jsone.code = 405
        return HttpResponse(jsone.toJson(), content_type="application/json")

@csrf_exempt
def getAllOrSaveSigbleVoiceReq(request):
    jsone = Utility()

    if request.method == 'GET':
        user_id = request.GET.get('user_id')
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
        if checkUserExist(user_id)==False:
           jsone.message = 'User name is invalid'
           jsone.error = True
           jsone.code = 503
           return HttpResponse(jsone.toJson(), content_type="application/json")

        record_start_time = request.POST.get('record_start_time')
        record_end_time = request.POST.get('record_end_time')
        record_type=request.POST.get('record_type')
        if bool(request.FILES.get('audioFile', False)) == False or  not record_start_time or not record_end_time or not record_type:
            jsone.message = 'You can not keep record_type,audioFile,record_start_time,record_end_time parameters are empty'
            jsone.error = True
            jsone.code = 503
            return HttpResponse(jsone.toJson(), content_type="application/json")
        else:
            audioFile = request.FILES['audioFile']
            record_type_intval=int(record_type)
            if record_type_intval==1 or record_type_intval==2:
                if record_type_intval==1:
                    filename=uploadFile(audioFile)
                    if filename == 'error_file':
                        jsone.message = 'Only wav audio file is allowed'
                        jsone.error = True
                        jsone.code = 503
                        return HttpResponse(jsone.toJson(), content_type="application/json")
                    else:
                        text = getAudioToText(BASE_DIR + '/' + filename)
                        jsone.result = processText(record_type, user_id, record_start_time, record_end_time, text,
                                                   filename)
                        jsone.message = 'Uploaded successfully'
                        return HttpResponse(jsone.toJson(), content_type="application/json")
                else:
                    caller_phone_no = request.POST.get('caller_phone_no')
                    receiver_phone_no = request.POST.get('receiver_phone_no')
                    if not caller_phone_no or not receiver_phone_no:
                        jsone.message = 'You can not keep caller_phone_no ,receiver_phone_no parameters are empty when  record type values 2 and no more than 15 cahrecters'
                        jsone.error = True
                        jsone.code = 503
                        return HttpResponse(jsone.toJson(), content_type="application/json")
                    else:
                        if len(caller_phone_no) > 15 or len(receiver_phone_no) > 15:
                            jsone.message = 'Phone number more than 15 characters is not accepted.'
                            jsone.error = True
                            jsone.code = 503
                            return HttpResponse(jsone.toJson(), content_type="application/json")
                        filename = uploadFile(audioFile)
                        if filename == 'error_file':
                            jsone.message = 'Only wav audio file is allowed'
                            jsone.error = True
                            jsone.code = 503
                            return HttpResponse(jsone.toJson(), content_type="application/json")
                        else:
                            text = getAudioToText(BASE_DIR + '/' + filename)
                            jsone.result = processText(record_type, user_id, record_start_time, record_end_time, text,
                                                       filename, caller_phone_no, receiver_phone_no)
                            jsone.message = 'Uploaded successfully'
                            return HttpResponse(jsone.toJson(), content_type="application/json")

            else:
                jsone.message = 'record_type parameter value is invalid .only 1 ,2 are valid'
                jsone.error = True
                jsone.code = 503
                return HttpResponse(jsone.toJson(), content_type="application/json")

    else:
        jsone.message = 'The request method '+request.method+' is not allowed'
        jsone.error = True
        jsone.code = 405
        return HttpResponse(jsone.toJson(), content_type="application/json")