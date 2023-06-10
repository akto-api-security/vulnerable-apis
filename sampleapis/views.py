import json
import configparser

from django.shortcuts import render

from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view


config=configparser.ConfigParser()
config.read('config.ini')


@api_view(['GET', 'TRACE'])
def index(request):
    if request.method == 'GET':
        return HttpResponse("WELCOME !!")
    elif request.method == 'TRACE':
        response = HttpResponse("WELCOME !!", status=200)
        response['Custom_Header_Name'] = 'Custom_Header_Value'  # here we can add the custom header which will be used in validating the test
        return response
    else:
        return HttpResponse("Method not allowed", status=405)

    
@api_view(['POST', 'TRACK'])
def track(request):
    if request.method == 'POST':
        return HttpResponse("WELCOME !!")
    elif request.method == 'TRACK':
        response = HttpResponse("WELCOME !!", status=200)
        response['Custom_Header_Name'] = 'Custom_Header_Value'  # here we can add the custom header which will be used in validating the test
        return response
    else:
        return HttpResponse("Method not allowed", status=405)


@api_view(['GET', 'POST'])
def serverversion(request):
    response = HttpResponse("WELCOME !!")
   # here we can add the server details in header for example we can use(Apache/2.4.18 (Ubuntu) or (nginx/1.18.0) or (Express/4.17.1))
    # response['Server'] = 'Server Details'
    return response

@api_view(['GET'])
def echo(request):
    return HttpResponse(json.dumps(request.data), status=200)


@api_view(['GET'])
def useconfig(request):
    response = HttpResponse("WELCOME !!")
    custom_header_name = config.get('CustomHeader', 'Name')
    custom_header_value = config.get('CustomHeader', 'Value')
    response[custom_header_name] = custom_header_value
    return response