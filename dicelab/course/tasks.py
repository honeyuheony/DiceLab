from celery import shared_task
from django.conf import settings
from django.core.cache import cache
import json
import urllib3
from typing import Dict
from json import loads
from .forms import CoursesCreationForm


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


# @shared_task
def set_data():
    data = load_notionAPI_course()['body']
    for d in data:
        value = {'code': [d['code']], 'name': [
            d['name']], 'semester': d['semester']}
        form = CoursesCreationForm(value)
        print(value)
        if form.is_valid():
            form.save()
            print('success')
        else:
            print(form.errors)

# Create your views here.


def load_notionAPI_course():
    url = f"https://api.notion.com/v1/databases/{Course_Database_ID}/query"
    sorts = [  # 정렬
        {
            "property": "code",
            "direction": "ascending"
        }
    ]
    filter = {  # 가져올 데이터 필터
        "or": [
             {
                 "property": "name",
                 "text": {
                     "is_not_empty": True
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
    data = []
    for r in source['results']:
        code = r['properties']['code']['title'][0]['plain_text']
        name = r['properties']['name']['rich_text'][0]['plain_text']
        semester = ([l['name']
                    for l in r['properties']['period']['multi_select']]) if 'period' in r['properties'] else 'None'
        data.append(
            {
                'code': code,
                'name': name,
                'semester': semester
            }
        )
    return {
        'statusCode': 200,
        'body': data
    }
