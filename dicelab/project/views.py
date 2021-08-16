from django.shortcuts import render
import json
import urllib3
from typing import Dict
from json import loads
from datetime import datetime
import re
from django.conf import settings

import os

http = urllib3.PoolManager()
Database_ID = getattr(settings, 'DATABASES_ID', 'Database_ID')
Internal_Integration_Token = getattr(
    settings, 'INTERNAL_INTEGRATION_TOKEN', 'Internal_Integration_Token')



# Create your views here.


def project(request):
    data = load_notionAPI_member()['body']
    return render(request, 'project.html', {'data' : data})

def load_notionAPI_member() :
    # read_key()

    url = f"https://api.notion.com/v1/databases/{Database_ID}/query"

    headers = {
        'Authorization': f'Bearer {Internal_Integration_Token}',
        'Notion-Version': '2021-07-27',
        "Content-Type": "application/json"
    }

    filter = {  # 가져올 데이터 필터
        "or" : [
            {
            "property": "course",
            "select": {
                    "is_not_empty": True
            }
        }
        ]
    }
    sorts = [  # 정렬
        {
            "property": "admission_date",
            "direction": "descending"
        }
    ]
    body = {
        "filter": filter,
        "sorts": sorts
    }
    response = http.request('POST',
                            url,
                            body=json.dumps(body),  # json파일로 인코딩
                            headers=headers,
                            retries=False)

    source: Dict = loads(response.data.decode('utf-8'))  # 자료형 명시
    with open("data.json", "w") as f:
        json.dump(source, f)
    return {
        'statusCode': 200,
        'body': json.dumps(source)
    }

