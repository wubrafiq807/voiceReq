# voiceReq APP
##Route for user API
 GET /api-v1/users/  #request url for login ,parameter email ,password ar mandatory
 
 POST /api-v1/users/ # request url for sign up .parameters are email,password,login_type
 if login_type ==1 ,then password mandatory .valid login_type values are 1,2,3,4