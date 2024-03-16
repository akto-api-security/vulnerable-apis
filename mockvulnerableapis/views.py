from django.shortcuts import render
from .decorator import authorization_check
import json
import os
import copy


from django.http import HttpResponse
from rest_framework.decorators import api_view
from .models import SampleData
from types import SimpleNamespace


@api_view(['POST'])
def add_sample_data(request):
    url = request.data["url"]
    data = request.data["data"]
    try:
        if SampleData.objects.filter(url=url).exists():
            SampleData.objects.update(data=json.dumps(data))
        else:
            SampleData.objects.create(url=url, data=json.dumps(data))

        return HttpResponse(json.dumps(request.data), status=200)
    except Exception as e:
        return HttpResponse("Error Inserting Sample Data".format(e), status=500)


@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'HEAD', 'TRACE', 'TRACK', 'TestMethod'])
@authorization_check
def fetch_sample_data(request):
    url = request.path
    print(url)
    try:
        sample_data = SampleData.objects.get(url=url)
        print("sample_data_url")
        print(sample_data.url)
        sample_data_json = json.loads(sample_data.data)
        resp = sample_data_json["responsePayload"]
        status_code = sample_data_json["statusCode"]
        headers = sample_data_json["responseHeaders"]

        api_resp = HttpResponse(json.dumps(resp), status=status_code)

        for key, value in headers.items():
            api_resp[key] = value

        return api_resp
    except Exception as e:
        return HttpResponse("Error Executing Request".format(e), status=500)


@api_view(['GET'])
def metrics(request):
    return HttpResponse(json.dumps("{}"), status=200)

@api_view(['POST'])
def insert_data(request):
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    path = cur_dir + "/sampleapidata.json"
    f = open(path, "r")
    data = f.read()
    testData = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))

    for obj in testData:
        try:
            resp = obj.testData.responsePayload
            headers = obj.testData.responseHeaders
            try:
                resp = vars(obj.testData.responsePayload)
                for key in resp:
                    try:
                        resp[key] = vars(resp[key])
                    except Exception as e:
                        pass
            except Exception as e:
                print("error loading responsePayload " + obj.id + " " + str(e))
            try:
                headers = vars(obj.testData.responseHeaders)
            except Exception as e:
                print("error loading responseHeaders " + obj.id + " " + str(e))

            data = {
                "method": obj.testData.method,
                "responsePayload": resp,
                "statusCode": obj.testData.statusCode,
                "responseHeaders": headers
            }

            url = obj.testData.url
            if SampleData.objects.filter(url=url).exists():
                SampleData.objects.filter(url=url).update(data=json.dumps(data))
            else:
                SampleData.objects.create(url=url, data=json.dumps(data))

        except Exception as e:
            print("error inserting data " + obj.id + " " + str(e))

    return HttpResponse(json.dumps(request.data), status=200)
