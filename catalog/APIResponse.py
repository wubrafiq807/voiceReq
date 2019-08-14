class APIResponse:
    def  jsonResponse(self,result,error,message):
        response_data = {}
        response_data['result'] = ''
        response_data['error'] = True
        response_data['message'] = ''
        return  response_data