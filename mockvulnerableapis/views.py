from django.shortcuts import render
from .decorator import authorization_check
from asgiref.sync import async_to_sync
import asyncio
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
    node_id = request.data.get("node_id", "x1")
    try:
        SampleData.objects.update_or_create(url=url, node_id=node_id, defaults = {"data": json.dumps(data)})
        return HttpResponse(json.dumps(request.data), status=200)
    except Exception as e:
        return HttpResponse("Error Inserting Sample Data".format(e), status=500)

@async_to_sync
async def resp_delay(api_resp, delay=0):
    await asyncio.sleep(delay)
    return api_resp

@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'HEAD', 'TRACE', 'TRACK', 'TestMethod'])
@authorization_check
def fetch_sample_data(request):
    url = request.path
    node_id = request.headers.get('x-akto-node', "x1")
    print(url)
    try:
        sample_data = SampleData.objects.get(url=url, node_id=node_id)
        print("sample_data_url")
        print(sample_data.url)
        sample_data_json = json.loads(sample_data.data)
        resp = sample_data_json["responsePayload"]
        status_code = sample_data_json["statusCode"]
        headers = sample_data_json["responseHeaders"]
        median_response_time = sample_data_json["medianResponseTime"]

        api_resp = HttpResponse(json.dumps(resp), status=status_code)

        for key, value in headers.items():
            api_resp[key] = value

        return resp_delay(api_resp, median_response_time/1000)
    except Exception as e:
        return HttpResponse("Error Executing Request".format(e), status=500)


@api_view(['GET'])
def metrics(request):
    return HttpResponse(json.dumps("{}"), status=200)

def fetch_data(testData, id):
    resp = testData.responsePayload
    headers = testData.responseHeaders
    try:
        resp = vars(testData.responsePayload)
        for key in resp:
            try:
                resp[key] = vars(resp[key])
            except Exception as e:
                pass
    except Exception as e:
        print("error loading responsePayload " + id + " " + str(e))
    try:
        headers = vars(testData.responseHeaders)
    except Exception as e:
        print("error loading responseHeaders " + id + " " + str(e))

    data = {
        "method": testData.method,
        "responsePayload": resp,
        "statusCode": testData.statusCode,
        "responseHeaders": headers,
        "medianResponseTime": getattr(testData, 'medianResponseTime', 0)
    }

    return data, testData.url

@api_view(['POST'])
def insert_data(request):
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    path = cur_dir + "/sampleapidata.json"
    f = open(path, "r")
    data = f.read()
    testData = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))

    for obj in testData:
        try:
            if hasattr(obj.testData, 'method'):
                data, url = fetch_data(obj.testData, obj.id)
                SampleData.objects.update_or_create(url=url, node_id="x1", defaults = {"data": json.dumps(data)})
            else:
                for node_id, nodeTestData in obj.testData.__dict__.items():
                    node_data, node_url = fetch_data(nodeTestData, obj.id)
                    SampleData.objects.update_or_create(url=node_url, node_id=node_id, defaults = {"data": json.dumps(node_data)})

        except Exception as e:
            print("error inserting data " + obj.id + " " + str(e))

    return HttpResponse(json.dumps(request.data), status=200)
