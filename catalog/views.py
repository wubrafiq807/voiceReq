
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from catalog.APIResponse import Utility
from catalog.recognizeVoice import getAudioToText
from voiceReq.UtilityClass import *
from catalog.SiteFuntion import *
from catalog.CustomSQL import getResultsBySQL, checkUserExist,executeSQL,apiKeyIsValid
from validate_email import validate_email
from voiceReq.UtilityClass import *
from rest_framework.decorators import api_view
@api_view(['DELETE','GET'])
@csrf_exempt
def updateDelOrGetSingleVoiceReq(request, id=''):
    jsone = Utility()
    if checkApiKey(request) == False:
        return getInvalidApiKEyError()
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
            jsone.result=None
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

@api_view(['POST','GET'])
@csrf_exempt
def getAllOrSaveSigbleVoiceReq(request):
    jsone = Utility()
    if checkApiKey(request) == False:
        return getInvalidApiKEyError()

    if request.method == 'GET':
        user_id = request.GET.get('user_id')
        fromDate = request.GET.get('fromDate')
        toDate = request.GET.get('toDate')
        validateRangeVar=validateRange(fromDate, toDate)
        if validateRangeVar ==0:
            jsone.message = 'Invalid date range.Valid range is toDate>fromDate'
            jsone.error = True
            jsone.code = 503
            jsone.result = None
            return HttpResponse(jsone.toJson(), content_type="application/json")

        if not user_id:
            jsone.message = 'You can not keep user_id empty as parameter'
            jsone.error = True
            jsone.code = 503
            jsone.result = None
            return HttpResponse(jsone.toJson(), content_type="application/json")
        else:
            query = "SELECT * from voice_req WHERE user_id='" + user_id + "'"
            if validateRangeVar ==1:
                query+=" and created_date >= '"+fromDate+"' and created_date <= '"+toDate+" 23:59'"

            print(query)
            jsone.result=getResultsBySQL(query)
            jsone.message='success'
            return HttpResponse(jsone.toJson(), content_type="application/json")

    elif request.method == 'POST':
        user_id = request.POST.get('user_id')
        if not user_id:
            jsone.message = 'User ID must'
            jsone.error = True
            jsone.code = 503
            jsone.result = None
            return HttpResponse(jsone.toJson(), content_type="application/json")
        if checkUserExist(user_id)==False:
           jsone.message = 'User ID is invalid'
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

def checkApiKey(request):
    api_key=request.headers.get('X-Api-Key')
    apiFlag=False
    if api_key is not None:
        if apiKeyIsValid(api_key)==True:
            apiFlag=True

    return apiFlag

@api_view(['POST','GET'])
@csrf_exempt
def signUpOrLoginUser(request):

    jsone = Utility()
    if checkApiKey(request) == False:
        return getInvalidApiKEyError()

    if request.method == 'GET':
        email = request.GET.get('email')
        password = request.GET.get('password')
        if validate_email(email)==False:
            return getInvalidEmailError()
        if not email or not password:
            jsone.message = 'email and password parameters can not be empty'
            jsone.error = True
            jsone.code = 405
            return HttpResponse(jsone.toJson(), content_type="application/json")
        users=getResultsBySQL("SELECT * FROM `user` WHERE email='"+email+"' and password='"+computeMD5hash(password)+"'")

        if len(list(users))<1:
            jsone.error=True
            jsone.message="Email or password is invalid"
            jsone.result = None
        else:
            jsone.message="login in success"
            jsone.result = users[0]

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
                jsone.error=True
                jsone.result = None
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


@api_view(['PUT', 'GET'])
@csrf_exempt
def updateUser(request,id=''):
    jsone = Utility()
    if checkApiKey(request) == False:
        return getInvalidApiKEyError()

    if request.method == 'PUT':
        put = request.data
        users=getResultsBySQL("select * from user where user_id='"+id+"'")
        if len(list(users))<1:
            jsone.error=True
            jsone.message="User ID is not found"
            jsone.result=[]
            jsone.code = 405
            return HttpResponse(jsone.toJson(), content_type="application/json")

        email = put.get('email')
        name = put.get('name')
        phone = put.get('phone')
        password = put.get('password')

        if not email is None and len(email)>0:
            if validate_email(email) == False:
                return getInvalidEmailError()
            if len(list(
                    getResultsBySQL("select * from user where email='" + email + "' and user_id!='" + id + "'"))) > 0:
                jsone.message = 'Email address already used for another user'
                jsone.error = True
                jsone.code = 405
                jsone.result=None
                return HttpResponse(jsone.toJson(), content_type="application/json")

        updateQuery="UPDATE user SET login_type=1 "
        if not name is None and len(name) > 0:
            updateQuery+=",name='"+name+"'"

        if not password is None and len(password)>0:
            updateQuery+=",password='"+computeMD5hash(password)+"'"
        if not phone is None and len(phone) > 0:
           updateQuery+=",phone='"+phone+"'"

        if not email is None and len(email):
            updateQuery+=",email='"+email+"'"
        updateQuery+=" WHERE user_id='"+id+"'"
        print(updateQuery)
        executeSQL(updateQuery)
        jsone.result=getResultsBySQL("select * from user where user_id='"+id+"'")[0]
        jsone.message="update success"
        return HttpResponse(jsone.toJson(), content_type="application/json")
    if request.method=='GET':
        user=getResultsBySQL("select * from user where user_id='" + id + "'")
        if len(list(user))>0:
            jsone.result = getResultsBySQL("select * from user where user_id='" + id + "'")[0]
            jsone.message = "result success"
        else:
            jsone.result=None
            jsone.error=False
        return HttpResponse(jsone.toJson(), content_type="application/json")




@api_view(['GET'])
@csrf_exempt
def checkUser(request,email=''):
    jsone = Utility()
    if checkApiKey(request) == False:
        return getInvalidApiKEyError()

    if request.method == 'GET':
        if validate_email(email) == False:
            return getInvalidEmailError()
        user=getResultsBySQL("SELECT * FROM `user` WHERE email='" + email + "'")
        if len(list(user))>0:
            jsone.result=user[0]
            jsone.message="Email exist in user"

        else:
            jsone.result=None
            jsone.error=True
            jsone.message = "Invalid email"
        return HttpResponse(jsone.toJson(), content_type="application/json")

@api_view(['POST'])
@csrf_exempt
def getPassword(request,email=''):
    jsone = Utility()
    if checkApiKey(request) == False:
        return getInvalidApiKEyError()

    if request.method == 'POST':

        if validate_email(email) == False:
            return getInvalidEmailError()
        user=getResultsBySQL("SELECT * FROM `user` WHERE email='" + email + "'")
        if len(list(user))>0:
            autoPassword=getRamdomPassword()
            updateQuery="update user set password='"+computeMD5hash(autoPassword)+"' where email='"+email+"'"
            executeSQL(updateQuery)
            sendPasswordToUserEmail(request,email,autoPassword)
            user = getResultsBySQL("SELECT * FROM `user` WHERE email='" + email + "'")
            jsone.result=user[0]
            jsone.message="New password '"+autoPassword+"' has been sent your email"

        else:
            jsone.result=None
            jsone.message = "Invalid email"
            jsone.error=True
        return HttpResponse(jsone.toJson(), content_type="application/json")

