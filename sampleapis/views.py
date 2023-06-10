import json

from django.shortcuts import render

from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view

@api_view(['GET'])
def index(request):
    return HttpResponse("WELCOME !!", status=200)


@api_view(['GET', 'TRACE'])
def trace_method_test(request):
    if request.method == 'GET':
        return HttpResponse("WELCOME !!")
    elif request.method == 'TRACE':
        response = HttpResponse("WELCOME !!", status=200)
        # response['Custom_Header_Name'] = 'Custom_Header_Value'  # here we can add the custom header which will be used in validating the test
        return response
    else:
        return HttpResponse("Method not allowed", status=405)

    
@api_view(['POST', 'TRACK'])
def track_method_test(request):
    if request.method == 'POST':
        return HttpResponse("WELCOME !!")
    elif request.method == 'TRACK':
        response = HttpResponse("WELCOME !!", status=200)
        # response['Custom_Header_Name'] = 'Custom_Header_Value'  # here we can add the custom header which will be used in validating the test
        return response
    else:
        return HttpResponse("Method not allowed", status=405)


@api_view(['GET', 'POST'])
def server_version_disclosure_test(request):
    response = HttpResponse("WELCOME !!")
   # here we can add the server details in header for example we can use(Apache/2.4.18 (Ubuntu) or (nginx/1.18.0) or (Express/4.17.1))
    # response['Server'] = 'Server Details'
    return response

@api_view(['GET'])
def echo(request):
    return HttpResponse(json.dumps(request.data), status=200)
