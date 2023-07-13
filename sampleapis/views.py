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
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import UserProfile
from .models import CardDetail
from .models import student,Result
from django.db import connection
from .database import db
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

@api_view(['GET'])
def index(request):
    return render(request, 'index.html')

@api_view(['POST'])
def user_signUp(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')
    first_name = request.data.get('first_name')
    last_name = request.data.get('last_name')

    if not username or not password:
        return Response({'error': 'Please provide username and password'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.create_user(username=username, email=email, first_name=first_name, last_name=last_name, password=password)
        user_profile = UserProfile(user=user, email=email, username=username, name=f"{first_name} {last_name}")
        user_profile.save() 
        full_name = f"{user.first_name} {user.last_name}"
        return Response({'success': 'User created successfully', 'id': user.id, 'username': user.username, 'full_name': full_name, 'email': user.email}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def user_signIn(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({'error': 'Please provide both username and password'}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(request, username=username, password=password)

    if user is None:
        return Response({'error': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)

    login(request, user)

    refresh = RefreshToken.for_user(user)
    token = str(refresh.access_token)

    return Response({'username': str(username), 'refresh': str(refresh), 'access': token}, status=status.HTTP_200_OK)

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
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
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
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
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

@api_view(['PUT'])
def update_email(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        new_email = request.data.get('email')
        user.email = new_email
        user.save()
        user_profile = UserProfile.objects.get(user=user)
        user_profile.email = new_email
        user_profile.save()

        return Response({'success': 'Email updated successfully'}, status=200)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['PUT'])
def update_phone_number(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        new_phone_number = request.data.get('phone_number')
        user_profile = UserProfile.objects.get(user=user)
        user_profile.phone_number = new_phone_number
        user_profile.save()

        return Response({'success': 'Phone number updated successfully'}, status=200)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)
    except UserProfile.DoesNotExist:
        return Response({'error': 'User profile not found'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['PUT'])
def change_username(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        new_username = request.data.get('username')
        if User.objects.filter(username=new_username).exists():
            return Response({'error': 'Username is already taken'}, status=400)
        user.username = new_username
        user.save()
        user_profile = UserProfile.objects.get(user=user)
        user_profile.username = new_username
        user_profile.save()

        return Response({'success': 'Username changed successfully'}, status=200)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)
    except UserProfile.DoesNotExist:
        return Response({'error': 'User profile not found'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['PUT'])
def edit_user_profile(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        user_profile = UserProfile.objects.get(user=user)
        user_profile.bio = request.data.get('bio', user_profile.bio)
        user_profile.roll_number = request.data.get('roll_number', user_profile.roll_number)
        user_profile.date_of_birth = request.data.get('date_of_birth', user_profile.date_of_birth)
        user_profile.departement = request.data.get('departement', user_profile.departement)
        user_profile.address = request.data.get('address', user_profile.address)
        user_profile.save()

        return Response({'success': 'User profile updated successfully'}, status=200)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)
    except UserProfile.DoesNotExist:
        return Response({'error': 'User profile not found'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['DELETE'])
def delete_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        user.delete()
        return Response({'success': 'User account deleted successfully'})
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def add_card(request, user_id):
    card_number = request.data.get('card_number')
    card_holder_name = request.data.get('card_holder_name')
    card_expiry_date = request.data.get('card_expiry_date')
    card_type = request.data.get('card_type')
    payment_network = request.data.get('payment_network')

    try:
        user = User.objects.get(id=user_id)
        existing_card = CardDetail.objects.filter(user=user, card_number=card_number).first()
        if existing_card:
            return Response({'error': 'Card details already exist for this user'}, status=status.HTTP_400_BAD_REQUEST)
        card_detail = CardDetail.objects.create(user=user, card_number=card_number, card_holder_name=card_holder_name, card_expiry_date=card_expiry_date, card_type=card_type, payment_network=payment_network)
        return Response({'message': 'Card detail added successfully'}, status=status.HTTP_201_CREATED)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# @api_view(['GET'])
# def get_card_details(request, user_id):
#     try:
#         # user = User.objects.get(id=user_id)
#         # card_details = CardDetail.objects.filter(user=user)
#         with connection.cursor() as cursor:
#             cursor.execute("""
#                 SELECT
#                     card_number,
#                     card_holder_name,
#                     card_expiry_date,
#                     card_type,
#                     payment_network
#                 FROM
#                     sampleapis_carddetail
#                 WHERE
#                     user_id = %s
#             """, [user_id])
#             card_details = cursor.fetchall()
#         card_data = []
#         for card in card_details:
#             card_data.append({
#                 'card_number': card.card_number,
#                 'card_holder_name': card.card_holder_name,
#                 'card_expiry_date': card.card_expiry_date,
#                 'card_type': card.card_type,
#                 'payment_network': card.payment_network
#             })

#         return Response({'card_details': card_data}, status=status.HTTP_200_OK)
#     except User.DoesNotExist:
#         return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
#     except Exception as e:
#         return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_card_details(request, user_id):
    try:
        with connection.cursor() as cursor:
            query = """
                SELECT
                    card_number,
                    card_holder_name,
                    card_expiry_date,
                    card_type,
                    payment_network
                FROM
                    sampleapis_carddetail
                WHERE
                    user_id = '{}'
            """.format(user_id)
            cursor.execute(query)
            card_details = cursor.fetchall()

        card_data = []
        for card in card_details:
            card_data.append({
                'card_number': card[0],
                'card_holder_name': card[1],
                'card_expiry_date': card[2],
                'card_type': card[3],
                'payment_network': card[4]
            })

        return Response({'card_details': card_data}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['GET', 'POST'])
def open_library(request):
    forwarded_host = request.META.get('HTTP_X_FORWARDED_HOST')
    real_host = request.META.get('HTTP_X_REAL_HOST')
    origin_host = request.META.get('HTTP_X_ORIGIN_HOST')
    host_override = request.META.get('HTTP_X_HOST_OVERRIDE')
    forwarded_server = request.META.get('HTTP_X_FORWARDED_SERVER')
    proxy_host = request.META.get('HTTP_X_PROXY_HOST')
    url = request.GET.get('url')

    if any([forwarded_host, real_host, origin_host, host_override, forwarded_server, proxy_host]):
        host = forwarded_host or real_host or origin_host or host_override or forwarded_server or proxy_host
        new_location = f"https://{host}/?url={url}"
        response = HttpResponse()
        response['Location'] = new_location
        response.status_code = 302
        return response
    return HttpResponse('welcome!!')

@api_view(['GET'])
def view_blog(request,url):
    response = HttpResponse()
    response['Location'] = url
    response.status_code = 302
    return response

# @api_view(['GET'])
# def abbc(request):
#     url = request.GET.get('url')
#     response = HttpResponse()
#     response['Location'] = url
#     response.status_code = 302
#     return response

@api_view(['POST'])
def add_student(request):
    name = request.data.get('name')
    roll_no = request.data.get('roll_no')
    departement = request.data.get('departement')
    batch = request.data.get('batch')

    if name is None or roll_no is None:
        return Response({'error': 'Missing required fields'}, status=400)
    
    try:
        existing_student = student.objects.using('mongo').get(roll_no=roll_no)
        return Response({'error': 'Student with the same roll number already exists'}, status=400)
    except student.DoesNotExist:
        pass

    new_student = student(name=name, roll_no=roll_no, departement=departement, batch=batch)
    new_student.save(using='mongo')

    return Response({'message': 'Student added successfully'}, status=201)


@api_view(['POST'])
def add_result(request):
    roll_no = request.data.get('roll_no')
    subject1 = request.data.get('subject1')
    subject2 = request.data.get('subject2')
    subject3 = request.data.get('subject3')
    subject4 = request.data.get('subject4')
    subject5 = request.data.get('subject5')
    subject6 = request.data.get('subject6')

    try:
        user = student.objects.using('mongo').get(roll_no=roll_no)
    except student.DoesNotExist:
        return JsonResponse({'error': 'Student does not exist'})

    result_count = Result.objects.using('mongo').filter(user=user).count()
    if result_count > 0:
        return JsonResponse({'error': 'Result already exists for the user'})

    new_result = Result(user=user, subject1=subject1, subject2=subject2, subject3=subject3, subject4=subject4, subject5=subject5, subject6=subject6)
    new_result.save(using='mongo')

    return JsonResponse({'success': 'Result added successfully'})

# @api_view(['GET'])
# def get_student(request, roll_no):
#     try:
#         student = student.objects.using('mongo').get(roll_no=roll_no)
#         student_data = {
#             'name': student.name,
#             'roll_no': student.roll_no,
#             'department': student.department,
#             'batch': student.batch
#         }
#         return Response({'student': student_data}, status=status.HTTP_200_OK)
#     except student.DoesNotExist:
#         return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)
#     except Exception as e:
#         return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_student(request):
    try:
        collection = db['STUDENTS_TABLE']
        query = {'roll_no': request.data["roll_no"]}
        items = list(collection.find(filter=query))

        if items:
            student_data = []
            for item in items:
                student_data.append({
                    'name': item['name'],
                    'roll_no': item['roll_no'],
                    'departement': item['departement'],
                    'batch': item['batch']
                })
            return Response({'student': student_data}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)