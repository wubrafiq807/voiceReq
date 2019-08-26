from sympy.integrals.rubi.utility_function import log

from catalog.CustomSQL import executeSQL
from catalog.recognizeVoice import extract_phone_numbers, extract_email_addresses,extract_names
from voiceReq.UtilityClass import getUuid
import datetime
from catalog.APIResponse import Utility
from django.http import HttpResponse

def processText(record_type,user_id,record_start_time,record_end_time,text,fileName, caller_phone_no='', receiver_phone_no=''):
    names = extract_names(text)
    emails = extract_email_addresses(text)
    phones = extract_phone_numbers(text)
    voice_req_id=getUuid()
    voice_req_query = 'INSERT INTO voice_req SET record_type='+record_type+', user_id="'+user_id+'",voice_req_id="'+voice_req_id+'",text="'+text+'",audio_file_name="'+fileName+'",record_start_time="'+record_start_time+'",record_end_time="'+record_end_time+'",created_date="'+str(datetime.datetime.now())+'"'
    executeSQL(voice_req_query)
    for name in names:
        query='INSERT INTO name SET name_id="'+getUuid()+'",name="'+name+'",voice_req_id="'+voice_req_id+'"'
        executeSQL(query)

    for email in emails:
        query = 'INSERT INTO email SET email_id="' + getUuid() + '",email="' + email + '",voice_req_id="' + voice_req_id + '"'
        executeSQL(query)

    for phone in phones:
        query = 'INSERT INTO phone SET phone_id="' + getUuid() + '",phone="' + phone + '",voice_req_id="' + voice_req_id + '"'
        executeSQL(query)
    if caller_phone_no !="" and receiver_phone_no !="":
        query="INSERT INTO receiver_caller SET receiver_caller_id='"+getUuid()+"',caller_phone_no='"+caller_phone_no+"',receiver_phone_no='"+receiver_phone_no+"',voice_req_id='"+voice_req_id+"'"
        executeSQL(query)

    return text
def getRamdomPassword():
    import random

    s = "abcdefghijklmnopqrstuvwxyz01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()?"
    passlen = 8
    p = "".join(random.sample(s, passlen))
    return p

def getInvalidApiKEyError():

    jsone = Utility()
    jsone.message = 'X-Api-Key is invalid .Please pass a header as key value pairs like X-Api-Key=>"example api key"'
    jsone.error = True
    jsone.code = 503
    jsone.result = None
    return HttpResponse(jsone.toJson(), content_type="application/json")

def getInvalidEmailError():
    jsone = Utility()
    jsone.message = 'Invalid email Address'
    jsone.error = True
    jsone.code = 405
    jsone.result=None
    return HttpResponse(jsone.toJson(), content_type="application/json")

def sendPasswordToUserEmail(request,toemail, password):
    from django.core.mail import BadHeaderError, send_mail
    from voiceReq import settings
    subject =  'Voice REQ System new password',
    message = 'You new password is :'+password+''
    email_from = settings.BANDIT_EMAIL
    recipient_list = [toemail]
    send_mail(subject, message, email_from, recipient_list, fail_silently=False)


def validateRange(fromDate, toDate):
    if fromDate is None and toDate is None:
        return 2
    if fromDate is not None and toDate is not None:
        if fromDate>=toDate:
            return 0
        if toDate>fromDate:
            return 1
    if (fromDate is not None and toDate is None) or (toDate is not None and fromDate is None):
         return 0




