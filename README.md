# VOICE RECOGNITION SYSTEM

Base Url:
---------
    BASE_URL = "http://192.168.100.74:8080/";

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

Reset Password:
----------------------------------
    Request Type: POST 
    API: /api-v1/get-password/users/<email_address>
  
## Route for voice recognition API

Request url for voice get all recognition list for user.mandatory parameter is user_id:
---------------------------------------------------------------------------------------
    GET /api-v1/voiceReqs/

Request url for create voice recognition:
-----------------------------------------
    POST /api-v1/voiceReqs/

Request url for get  recognition by ID:
-----------------------------------------
    GET /api-v1/voiceReqs/<recogtion_id>

Request url for delete recognition by ID:
---------------------------------------------
    DELETE /api-v1/voiceReqs/<recogtion_id>
