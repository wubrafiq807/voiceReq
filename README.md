# VOICE RECOGNITION SYSTEM

## Route for user API

 <code>GET /api-v1/users/</code>  #request url for login ,parameter email ,password ar mandatory
 
<code>POST /api-v1/users/</code> # request url for sign up .parameters are email,password,login_type
 if login_type ==1 ,then password mandatory .valid login_type values are 1,2,3,4
 
 <code>PUT /api-v1/users/<user_id>/</code> # request url for update  user info .Only email,phone,password,name can be 
 be updated.
 
 <code>GET /api-v1/users/check/<email_address>/</code>#Request url for checking email address already exist int the system.
 
 <code>POST /api-v1/get-password/users/<email_address></code> #Request url for forget password
  
## Route for voice recognition API
  
 <code>GET /api-v1/voiceReqs/</code> # request url for voice get all recognition list for user.mandatory parameter is user_id
  
 <code>POST /api-v1/voiceReqs/</code># Request url for create voice recognition 
 
 <code>GET /api-v1/voiceReqs/<recogtion_id>/</code> # Request url for get  recognition by ID 
 
 <code>DELETE /api-v1/voiceReqs/<recogtion_id>/</code> # request url for delete recognition by ID