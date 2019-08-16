from catalog.CustomSQL import executeSQL
from catalog.recognizeVoice import extract_phone_numbers, extract_email_addresses,extract_names
from voiceReq.UtilityClass import getUuid
import datetime

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