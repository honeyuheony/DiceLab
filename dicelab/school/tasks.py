import json
import urllib3
from typing import Dict
from json import loads
from django.conf import settings
from celery import shared_task
from .models import School, Lecture

http = urllib3.PoolManager()
School_Database_ID = getattr(
    settings, 'SCHOOL_DATABASE_ID', 'School_Database_ID')
Internal_Integration_Token = getattr(
    settings, 'INTERNAL_INTEGRATION_TOKEN', 'Internal_Integration_Token')
Notion = getattr(settings, 'NOTION_VERSION', 'Notion-version')
headers = {
    'Authorization': f'Bearer {Internal_Integration_Token}',
    'Notion-Version': Notion,
    "Content-Type": "application/json"
}


@shared_task
def set_data():
    data = load_notionAPI_school()['body']
    for d in data:
        school, created = School.objects.update_or_create(title=d['title'])
        for l, u in d['lecture']:
            lecture, created = Lecture.objects.update_or_create(
                name=l, url=u)
            school.lecture.add(lecture)
            school.save()


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
            'lecture': lecture,
        })
    return {
        'statusCode': 200,
        'body': data
    }
