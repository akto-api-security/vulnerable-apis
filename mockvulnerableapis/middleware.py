from django.http import HttpResponse

class AuthenticationTokenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Exept these paths from authentication token check
        self.bypass_paths = ['/api/insert_data', '/login']

    def __call__(self, request):
        print(request.path)
        if any(path in request.path for path in self.bypass_paths):
            return self.get_response(request)
        if 'HTTP_ACCESS_TOKEN' not in request.META:
            return HttpResponse('Unauthorized', status=401)

        response = self.get_response(request)
        return response