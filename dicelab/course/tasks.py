from celery import shared_task
from django.conf import settings
from django.core.cache import cache
import json
import urllib3
from typing import Dict
from json import loads


http = urllib3.PoolManager()
Internal_Integration_Token = getattr(
    settings, 'INTERNAL_INTEGRATION_TOKEN', 'Internal_Integration_Token')
Course_Database_ID = getattr(
    settings, 'COURSE_DATABASE_ID', 'course_database_ID')
Notion = getattr(settings, 'NOTION_VERSION', 'Notion-version')


headers = {
    'Authorization': f'Bearer {Internal_Integration_Token}',
    'Notion-Version': Notion,
    "Content-Type": "application/json"
}


@shared_task
def set_cache():
    cache.set('semester', load_notionAPI_course()['body'])

# Create your views here.


def load_notionAPI_course():
    url = f"https://api.notion.com/v1/databases/{Course_Database_ID}/query"
    semester = {'2021_Spring': [], '2020_Fall': [], '2020_Spring': [],
                '2019_Fall': [], '2019_Spring': [], '2018_Fall': [], '2018_Spring': []}
    sorts = [  # 정렬
        {
            "property": "period",
            "direction": "descending"
        },
        {
            "property": "code",
            "direction": "ascending"
        }
    ]
    for key in semester:
        filter = {  # 가져올 데이터 필터
            "or": [
                {
                    "property": "period",
                    "multi_select": {
                        "contains": key
                    }
                }
            ]
        }
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
            code = r['properties']['code']['title'][0]['plain_text']
            name = r['properties']['name']['rich_text'][0]['plain_text']
            semester[key].append(code + ', ' + name)
        semester[key].sort()
    return {
        'statusCode': 200,
        'body': semester
    }
