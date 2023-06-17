import json
import time
import uuid
import csv
import requests

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
    # print(url)
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

@api_view(['POST'])
def upload_transcript(request):
    csv_file_value = request.GET.get('csv_file')
    if csv_file_value == 'https://ssrf.localdomain.pw/csv-without-body/301-http-169.254.169.254:80-.c.csv':
        res_data = {
            'ami-id': 'some-ami-id-value',
            'ami-launch-index': '1',
            'ami-manifest-path': '/path/to/manifest',
            'block-device-mapping': '/dev/sda1',
            'instance-action': 'pending',
        }
        return JsonResponse(res_data,safe=False)
    elif(csv_file_value):
        return JsonResponse({'message': 'file uploaded successfully'})
    else:
        return JsonResponse({'error':'something went wrong(check file type)'},status=500)
    # for file_field in request.FILES.values():
    #     if file_field.content_type == 'text/csv':
    #         csv_file = file_field
    #         break
    #     if csv_file:
    #         return JsonResponse({'message':'file uploaded successfully'})
    # content = csv_file.read().decode('utf-8')
    # csv_reader = csv.DictReader(content.splitlines())
    # aws_info_list = []
    # for row in csv_reader:
    #     aws_info_url = row.get('AWS_Info')
    #     if aws_info_url:
    #         try:
    #             response = requests.get(aws_info_url)
    #             if response.status_code == 200:
    #                 aws_info = response.text
    #                 aws_info_list.append(aws_info)
    #         except requests.RequestException:
    #             aws_info_list.append("something went wrong")
    # response = '\n'.join(aws_info_list)
    # return HttpResponse(response, content_type='text/plain')


@api_view(['POST'])
def upload_profile_pic(request):
    img_file_value = request.GET.get('img_file')
    
    if img_file_value == 'https://ssrf.localdomain.pw/img-without-body/301-http-169.254.169.254:80-.i.jpg':
        res_data = {
            'ami-id': 'some-ami-id-value',
            'ami-launch-index': '1',
            'ami-manifest-path': '/path/to/manifest',
            'block-device-mapping': '/dev/sda1',
            'instance-action': 'pending',
        }
        return JsonResponse(res_data,safe=False)
    elif(img_file_value):
        return JsonResponse({'message': 'Profile Image uploaded successfully'})
    else:
        return JsonResponse({'error':'something went wrong(check file type)'},status=500)
    # for file_field in request.FILES.values():
    #     if file_field.content_type.startswith('image/'):
    #         img_file = file_field
    #         break
    # if img_file:
    #     return JsonResponse({'message':'Image uploaded successfully'})

@api_view(['POST'])
def upload_resume(request):
    pdf_file_value = request.GET.get('pdf_file')
    
    if pdf_file_value == 'https://ssrf.localdomain.pw/pdf-without-body/301-http-169.254.169.254:80-.p.pdf':
        res_data = {
            'ami-id': 'some-ami-id-value',
            'ami-launch-index': '1',
            'ami-manifest-path': '/path/to/manifest',
            'block-device-mapping': '/dev/sda1',
            'instance-action': 'pending',
        }
        return JsonResponse(res_data,safe=False)
    elif(pdf_file_value):
        return JsonResponse({'message': 'PDF uploaded successfully'})
    else:
        return JsonResponse({'error':'something went wrong(check file type)'},status=500)  


@api_view(['GET'])
def echo(request):
    return HttpResponse(json.dumps(request.data), status=200)
