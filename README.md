# VOICE RECOGNITION SYSTEM

Base Url:
---------
    BASE_URL = "http://You host ip:8080/";

## Route for user API

User Login:
---------------------------------------------------------------
    Request Type: GET 
    API: /api-v1/users/
    
    Note: parameter email ,password ar mandatory
 
 Sign Up / Registration:
 ------------------------------------------------------------------
    Request Type: POST 
    API: /api-v1/users/
    
    Note: parameters are email, password, login_type. if login_type ==1 ,then password mandatory .valid login_type values are 1,2,3,4
    
Update User Info:
----------------------------------------------------------------------------------
    Request Type: PUT 
    API: /api-v1/users/<user_id>
    
    Note: Only email, phone, password, name can be updated.
 
User Find By Email:
--------------------------------------------------------------------
    Request Type: GET 
    API: /api-v1/users/check/<email_address>

User Find By user_id:
--------------------------------------------------------------------
    Request Type: GET 
    API: /api-v1/users/<user_id>
    
Reset Password:
----------------------------------
    Request Type: POST 
    API: /api-v1/get-password/users/<email_address>
  
## Route for voice recognition API

Get all recognition list for user:
---------------------------------------------------------------------------------------
    Request Type: GET
    API: /api-v1/voiceReqs/
    Note:.mandatory parameter is user_id.Optional parameter fromDate,toDate.
    valid from fromDate is not null and toDate not null and toDate>fromDate.
    

Create voice recognition:
-----------------------------------------
    Request Type: POST 
    API: /api-v1/voiceReqs/
    Note: You can not keep user_id, record_type,audioFile,record_start_time,record_end_time parameters are empty.And also the record_type value only 1 or 2.You can not keep caller_phone_no ,receiver_phone_no parameters are empty ,
    when  record_type parametr value is  2 .Please remeber phone numbers are no more than 15 charecters.

Get  recognition by ID:
-----------------------------------------
    Request Type: GET
    API: /api-v1/voiceReqs/<recogtion_id>/

Delete recognition by ID:
---------------------------------------------
    Request Type: DELETE
    API: /api-v1/voiceReqs/<recogtion_id>/
