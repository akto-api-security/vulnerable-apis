import json
import time
import uuid

from django.shortcuts import render
from django.shortcuts import redirect

from django.http import HttpResponse
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view

@api_view(['GET'])
def index(request):
    return HttpResponse("WELCOME !!", status=200)


def fetch_file(file):
    with open(file, 'r') as json_file:
        data = json.load(json_file)
    return data

@api_view(['GET', 'TRACE'])
def getUserProfile(request):
    Data = fetch_file('sampleapis/Data/profile_details.json')
    if request.method == 'GET':
        return JsonResponse(Data, safe=False)
    elif request.method == 'TRACE':
        return JsonResponse(Data, status=200, safe=False)
    else:
        return HttpResponse("Method not allowed", status=405)

    
@api_view(['GET', 'TRACK'])
def getNotices(request):
    Data = fetch_file('sampleapis/Data/notices.json')
    if request.method == 'GET':
        return JsonResponse(Data, safe=False)
    elif request.method == 'TRACK':
        return JsonResponse(Data, status=200, safe=False)
    else:
        return HttpResponse("Method not allowed", status=405)


@api_view(['GET', 'POST'])
def getResults(request):
    Data = fetch_file('sampleapis/Data/result.json')
    return JsonResponse(Data, safe=False)

@api_view(['GET', 'POST'])
def getFeedbacks(request):
    url = request.GET.get('url')
    response = HttpResponse()
    response['Location'] = url
    response.status_code = 302
    return response

@api_view(['GET'])
def getCourseList(request):
    limit = request.GET.get('limit')
    resources = fetch_course_list_from_file(limit)
    return JsonResponse(resources, safe=False)


def fetch_course_list_from_file(limit):
    with open('sampleapis/Data/courses.json', 'r') as file:
        Data = json.load(file)
        resources = Data['courses']
    return resources[:int(limit)]

# old api version test
#version-1 
@api_view(['GET', 'POST'])
def payment_v1(request):
    payment_id = str(uuid.uuid4())
    payment_data = {
        'payment_id': payment_id,
        'amount': 50000.0,
        'currency': 'INR',
        'status': 'completed'
    }
    time.sleep(10)
    return JsonResponse(payment_data, status=200)

#version-2
@api_view(['GET', 'POST'])
def payment_v2(request):
    payment_id = str(uuid.uuid4())
    payment_data = {
        'merchant_name': 'XYZ Store',
        'payee_name': 'John Doe',
        'payment_id': payment_id,
        'amount': 75000.0,
        'currency': 'INR',
        'status': 'completed'
    }
    time.sleep(5)
    return JsonResponse(payment_data, status=200)

@api_view(['GET', 'POST'])
def getAttendence(request):
    Data = fetch_file('sampleapis/Data/attendence.json')
    response = JsonResponse(Data, safe=False)
    del response['Content-Type']
    return response

@api_view(['GET'])
def echo(request):
    return HttpResponse(json.dumps(request.data), status=200)
