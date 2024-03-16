from functools import wraps
from django.http import HttpResponse

def authorization_check(view_function):
    @wraps(view_function)
    def wrap(request, *args, **kwargs):
        if 'HTTP_AUTHORIZATION' not in request.META:
            return HttpResponse('Unauthorized', status=401)
        return view_function(request, *args, **kwargs)
    return wrap