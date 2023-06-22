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
    if url:
        response = HttpResponse()
        response['Location'] = url
        response.status_code = 302
        return response
    else:
        Data = fetch_file('sampleapis/Data/user_feedbacks.json')
        return JsonResponse(Data, safe=False)

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
    elif(csv_file_value and csv_file_value.endswith('.csv') and csv_file_value != '.csv'):
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
    elif(img_file_value and img_file_value.endswith('.jpg') and img_file_value != '.jpg'):
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
    elif(pdf_file_value and pdf_file_value.endswith('.pdf') and pdf_file_value != '.pdf'):
        return JsonResponse({'message': 'PDF uploaded successfully'})
    else:
        return JsonResponse({'error':'something went wrong(check file type)'},status=500)  


@api_view(['POST'])
def upload_lab_report(request):
    xml_file_value = request.GET.get('xml_file')
    
    if xml_file_value == 'https://ssrf.localdomain.pw/xml-without-body-md/301-http-.x.xml':
        res_data = {
            'ami-id': 'some-ami-id-value',
            'ami-launch-index': '1',
            'ami-manifest-path': '/path/to/manifest',
            'block-device-mapping': '/dev/sda1',
            'instance-action': 'pending',
        }
        return JsonResponse(res_data,safe=False)
    elif(xml_file_value and xml_file_value.endswith('.xml') and xml_file_value != '.xml'):
        return JsonResponse({'message': 'XML file uploaded successfully'})
    else:
        return JsonResponse({'error':'something went wrong(check file type)'},status=500)


@api_view(['GET'])
def search_portal(request):
    url = request.GET.get('url')
    if url == 'http://169.254.169.254/latest/meta-data/local-ipv4':
        res_data = {
            'ami-id': 'some-ami-id-value',
            'ami-launch-index': '1',
            'ami-manifest-path': '/path/to/manifest',
            'block-device-mapping': '/dev/sda1',
            'instance-action': 'pending',
        }
        return JsonResponse(res_data,safe=False)
    elif url == 'http://⑯⑨。②⑤④。⑯⑨｡②⑤④/latest/meta-data/local-ipv4':
        res_data = {
            'ami-id': 'some-ami-id-value',
            'ami-launch-index': '1',
            'ami-manifest-path': '/path/to/manifest',
            'block-device-mapping': '/dev/sda1',
            'instance-action': 'pending',
        }
        return JsonResponse(res_data,safe=False)
    elif  url:
        response = requests.get(url)
        data = response.text
        return JsonResponse({'data': data})
    else:
        return JsonResponse({'error':'something went wrong'}, status=500)

# @api_view(['GET'])
# def vulnerable_view_1(request):
#     url = request.GET.get('url')
#     if url =='http://⑯⑨。②⑤④。⑯⑨｡②⑤④/latest/meta-data/local-ipv4':
#         res_data = {
#             'ami-id': 'some-ami-id-value',
#             'ami-launch-index': '1',
#             'ami-manifest-path': '/path/to/manifest',
#             'block-device-mapping': '/dev/sda1',
#             'instance-action': 'pending',
#         }
#         return JsonResponse(res_data,safe=False)
#     elif  url:
#         response = requests.get(url)
#         data = response.text
#         return JsonResponse({'data': data})
#     else:
#         return JsonResponse({'error':'something went wrong'}, status=500)


@api_view(['GET'])
def getRecents(request):
    url = request.GET.get('url')
    if url =='http://localhost/admin':
        res_data = {
            "status": "success",
            "message": "Welcome to the Admin Panel",
            "data": {
                "user_count": 150,
                "last_login": "2023-06-19 15:30:45",
                "privileged_accounts": ["admin", "superuser"],
                "server_status": "Online"
            }
        }
        return JsonResponse(res_data,safe=False)
    elif url == 'http://①②⑦。⓪⓪⓪。⓪⓪①/admin':
        res_data = {
            "status": "success",
            "message": "Welcome to the Admin Panel",
            "data": {
                "user_count": 150,
                "last_login": "2023-06-19 15:30:45",
                "privileged_accounts": ["admin", "superuser"],
                "server_status": "Online"
            }
        }
        return JsonResponse(res_data,safe=False)
    elif  url:
        response = requests.get(url)
        data = response.text
        return JsonResponse({'data': data})
    else:
        return JsonResponse({'error':'something went wrong'}, status=500)

# @api_view(['GET'])
# def vulnerable_view_3(request):
#     url = request.GET.get('url')
#     if url == 'http://①②⑦。⓪⓪⓪。⓪⓪①/admin':
#         res_data = {
#             "status": "success",
#             "message": "Welcome to the Admin Panel",
#             "data": {
#                 "user_count": 150,
#                 "last_login": "2023-06-19 15:30:45",
#                 "privileged_accounts": ["admin", "superuser"],
#                 "server_status": "Online"
#             }
#         }
#     elif  url:
#         response = requests.get(url)
#         data = response.text
#         return JsonResponse({'data': data})
#     else:
#         return JsonResponse({'error':'something went wrong'}, status=500)


@api_view(['GET'])
def getTnp_notifications(request):
    url = request.GET.get('url')
    if url == 'http://make-127-0-0-1-rr.1u.ms/admin':
        res_data = {
            "status": "success",
            "message": "Welcome to the Admin Panel",
            "data": {
                "user_count": 150,
                "last_login": "2023-06-19 15:30:45",
                "privileged_accounts": ["admin", "superuser"],
                "server_status": "Online"
            }
        }
        return JsonResponse(res_data,safe=False)
    elif  url:
        response = requests.get(url)
        data = response.text
        return JsonResponse({'data': data})
    else:
        return JsonResponse({'error':'something went wrong'}, status=500)

@api_view(['GET'])
def getDocuments(request):
    file = request.GET.get('file')
    if file == '///etc/passwd':
        res_data = {'Data':'root:x:0:0:root:/root:/bin/ash\nbin:x:1:1:bin:/bin:/sbin/nologin\ndaemon:x:2:2:daemon:/sbin:/sbin/nologin\nadm:x:3:4:adm:/var/adm:/sbin/nologin\nlp:x:4:7:lp:/var/spool/lpd:/sbin/nologin\nsync:x:5:0:sync:/sbin:/bin/sync\nshutdown:x:6:0:shutdown:/sbin:/sbin/shutdown\nhalt:x:7:0:halt:/sbin:/sbin/halt\nmail:x:8:12:mail:/var/mail:/sbin/nologin\nnews:x:9:13:news:/usr/lib/news:/sbin/nologin\nuucp:x:10:14:uucp:/var/spool/uucppublic:/sbin/nologin\noperator:x:11:0:operator:/root:/sbin/nologin\nman:x:13:15:man:/usr/man:/sbin/nologin\npostmaster:x:14:12:postmaster:/var/mail:/sbin/nologin\ncron:x:16:16:cron:/var/spool/cron:/sbin/nologin\nftp:x:21:21::/var/lib/ftp:/sbin/nologin\nsshd:x:22:22:sshd:/dev/null:/sbin/nologin\nat:x:25:25:at:/var/spool/cron/atjobs:/sbin/nologin\nsquid:x:31:31:Squid:/var/cache/squid:/sbin/nologin\nxfs:x:33:33:X Font Server:/etc/X11/fs:/sbin/nologin\ngames:x:35:35:games:/usr/games:/sbin/nologin\ncyrus:x:85:12::/usr/cyrus:/sbin/nologin\nvpopmail:x:89:89::/var/vpopmail:/sbin/nologin\nntp:x:123:123:NTP:/var/empty:/sbin/nologin\nsmmsp:x:209:209:smmsp:/var/spool/mqueue:/sbin/nologin\nguest:x:405:100:guest:/dev/null:/sbin/nologin\nnobody:x:65534:65534:nobody:/:/sbin/nologin\nnginx:x:100:101:nginx:/var/lib/nginx:/sbin/nologin\nvnstat:x:101:102:vnstat:/var/lib/vnstat:/bin/false\nredis:x:102:103:redis:/var/lib/redis:/bin/false'}
        return JsonResponse(res_data,safe=False)
    elif  file:
        return JsonResponse({'message': 'you are trying to access files'})
    else:
        return JsonResponse({'error':'something went wrong'}, status=500)

@api_view(['GET'])
def echo(request):
    return HttpResponse(json.dumps(request.data), status=200)
