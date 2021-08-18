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
School_Database_ID = getattr(
    settings, 'SCHOOL_DATABASE_ID', 'School_Database_ID')
Internal_Integration_Token = getattr(
    settings, 'INTERNAL_INTEGRATION_TOKEN', 'Internal_Integration_Token')

headers = {
    'Authorization': f'Bearer {Internal_Integration_Token}',
    'Notion-Version': '2021-07-27',
    "Content-Type": "application/json"
}

# Create your views here.


def school(request):
    school = load_notionAPI_school()['body']
    return render(request, 'school.html', {'school': school})


def load_notionAPI_school():
    url = f"https://api.notion.com/v1/databases/{School_Database_ID}/query"
    filter = {  # 가져올 데이터 필터
        "or": [
                {
                    "property": "title",
                    "text": {
                        "is_not_empty": True
                    }
                }
        ]
    }
    sorts = [  # 정렬
        {
            "property": "title",
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
        json.dump(source['results'], f)
    data = []
    for r in source['results']:
        title = r['properties']['Title']['title'][0]['plain_text']
        lecture = [l['title'][0]['plain_text']
                   for l in r['properties']['lecture']['rollup']['array']]
        url = [l['url']
               for l in r['properties']['url']['rollup']['array']]
        lecture = zip(lecture, url)

        data.append({
            'title': title,
            'lecture': lecture
        })
    return {
        'statusCode': 200,
        'body': data
    }
