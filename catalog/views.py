
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from catalog.APIResponse import Utility
from catalog.recognizeVoice import getAudioToText
from voiceReq.UtilityClass import *
from catalog.SiteFuntion import *
from catalog.CustomSQL import getResultsBySQL, checkUserExist,executeSQL
from validate_email import validate_email
from voiceReq.UtilityClass import *
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
            finalData['emails'] = getResultsBySQL("SELECT * FROM `email` WHERE voice_req_id='" + id + "'")

            if finalData['record_type'] ==2:
                callerReceiverInfo=getResultsBySQL("SELECT * FROM `receiver_caller` WHERE voice_req_id='"+id+"'")
                if len(list(callerReceiverInfo)) > 0:
                    finalData['caller_phone_no'] = callerReceiverInfo[0]['caller_phone_no']
                    finalData['receiver_phone_no'] = callerReceiverInfo[0]['receiver_phone_no']

            jsone.result = finalData
        else:
            jsone.message='No record found in database'
            jsone.result=[]
        return HttpResponse(jsone.toJson(), content_type="application/json")
    elif request.method == 'DELETE':
        results=getResultsBySQL("SELECT * FROM `phone` WHERE voice_req_id='"+id+"'")
        if len(list(results))>0:
            executeSQL("DELETE FROM `phone` WHERE voice_req_id='" + id + "'")
            executeSQL("DELETE FROM `name` WHERE voice_req_id='" + id + "'")
            executeSQL("DELETE FROM `email` WHERE voice_req_id='" + id + "'")
            executeSQL("DELETE FROM `receiver_caller` WHERE voice_req_id='" + id + "'")
            executeSQL('DELETE FROM `voice_req` WHERE voice_req_id="' + id + '"')
            jsone.message = 'Success fully deleted'
            return HttpResponse(jsone.toJson(), content_type="application/json")
        else:
            jsone.message = 'No record in database.That can be delete by the ID'
            jsone.result=[]
            return HttpResponse(jsone.toJson(), content_type="application/json")

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

@csrf_exempt
def signUpOrLoginUser(request):
    jsone = Utility()

    if request.method == 'GET':
        email = request.GET.get('email')
        password = request.GET.get('password')
        if validate_email(email)==False:
            jsone.message = 'Invalid meail Address'
            jsone.error = True
            jsone.code = 405
            return HttpResponse(jsone.toJson(), content_type="application/json")
        if not email or not password:
            jsone.message = 'email and password parameters can not be empty'
            jsone.error = True
            jsone.code = 405
            return HttpResponse(jsone.toJson(), content_type="application/json")
        users=getResultsBySQL("SELECT * FROM `user` WHERE email='"+email+"' and password='"+computeMD5hash(password)+"'")
        jsone.result = users
        if len(list(users))<1:
            jsone.error=True
            jsone.message="record not found"
        else:
            jsone.message="login in success"

        return HttpResponse(jsone.toJson(), content_type="application/json")

    elif request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        login_type = request.POST.get('login_type')
        type_flag=False

        if not login_type:
            jsone.code = 503
            jsone.message = 'You can not keep empty login_type parameters are empty'
            jsone.result = []
            return HttpResponse(jsone.toJson(), content_type="application/json")
        if login_type=='1' or login_type=='2' or login_type=='3' or login_type=='4':
            type_flag=True

        if type_flag==False:
            jsone.code = 503
            jsone.message = 'Invalid value passed into login_type parameter.The valid values are 1,2,3,4'
            jsone.result = []
            return HttpResponse(jsone.toJson(), content_type="application/json")

        if (login_type =='1') and (not email or not password):
            jsone.code = 503
            jsone.message = 'You can not keep empty email,password parameters are empty'
            jsone.result = []
            return HttpResponse(jsone.toJson(), content_type="application/json")
        if (login_type !='1') and not email:
            jsone.code = 503
            jsone.message = 'You can not keep empty email parameters are empty'
            jsone.result = []
            return HttpResponse(jsone.toJson(), content_type="application/json")

        if validate_email(email):
            if len(list(getResultsBySQL("SELECT * FROM `user` WHERE email='" + email + "'"))) > 0:
                jsone.code = 503
                jsone.message = 'Email address already exist in the database'
                jsone.result = []
                return HttpResponse(jsone.toJson(), content_type="application/json")

            user_id = getUuid()
            query = "INSERT INTO user SET user_id='" + user_id + "',email='" + email + "', login_type=" + login_type + ""
            if login_type=='1':
                query=query+",password='"+computeMD5hash(password)+"'"
            executeSQL(query)
            jsone.message = 'Signup success'
            jsone.result = getResultsBySQL("SELECT * FROM `user` WHERE user_id='" + user_id + "'")[0]
            return HttpResponse(jsone.toJson(), content_type="application/json")
        else:
            jsone.code = 503
            jsone.message = 'Invalid email address'
            return HttpResponse(jsone.toJson(), content_type="application/json")

    else:
        jsone.message = 'The request method ' + request.method + ' is not allowed'
        jsone.error = True
        jsone.code = 405
        return HttpResponse(jsone.toJson(), content_type="application/json")
@csrf_exempt
def updateUser(request):
    jsone = Utility()

    if request.method == 'GET':
        email = request.GET.get('email')
        password = request.GET.get('password')
        jsone.message = 'The request method ' + request.method + ' is not allowed'
        jsone.error = True
        jsone.code = 405
        return HttpResponse(jsone.toJson(), content_type="application/json")
    elif request.method == 'POST':
        email = request.GET.get('email')
        password = request.GET.get('password')
        jsone.message = 'The request method ' + request.method + ' is not allowed'
        jsone.error = True
        jsone.code = 405
        return HttpResponse(jsone.toJson(), content_type="application/json")
    else:
        jsone.message = 'The request method ' + request.method + ' is not allowed'
        jsone.error = True
        jsone.code = 405
        return HttpResponse(jsone.toJson(), content_type="application/json")

