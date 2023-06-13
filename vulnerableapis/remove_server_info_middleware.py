class Remove_Server_Info_Middleware:
    def __init__(self, get_response):
        self.get_response=get_response
    
    def __call__(self, request):
        if request.path == '/sampleapis/academics/results/':
            response=self.get_response(request)
        elif request.method == 'TRACE' or request.method == 'TRACK':
            response=self.get_response(request)
            response['new_test_header']='test_val'
            response['Server']=''
        else:
            response=self.get_response(request)
            response['Server']=''
        
        return response
    