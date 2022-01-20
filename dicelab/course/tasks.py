from celery import shared_task
from django.conf import settings
import json
import urllib3
from typing import Dict
from json import loads
from .models import Semester, Course


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
def set_data():
    data = load_notionAPI_course()['body']
    temp = []
    # Data Create or Update
    for d in data:
        c, created = Course.objects.update_or_create(
            name=d['name'])
        c.code = d['code']
        c.save()
        for s in d['semester']:
            obj, created = Semester.objects.get_or_create(
                year=s[0:4], title=s[5:])
            c.semester.add(obj)
            c.save()
        temp.append(d['code'])
    # Data Delete
    for db in Course.objects.all():
        if not db.code in temp:
            Course.objects.get(code=db.code).delete()


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
        code = r['properties']['code']['title'][0]['plain_text'] if r['properties']['code']['title'] else ""
        name = r['properties']['name']['rich_text'][0]['plain_text']
        semester = ([l['name']
                    for l in r['properties']['semester']['multi_select']]) if 'semester' in r['properties'] else 'None'
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
