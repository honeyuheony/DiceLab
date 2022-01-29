import json
import urllib3
from typing import Dict
from json import loads
from django.conf import settings
from celery import shared_task
from .models import Demo

http = urllib3.PoolManager()
# Demo_Database_ID = getattr(
#     settings, 'DEMO_DATABASE_ID', 'Demo_Database_ID')
Demo_Database_ID = "619cc519d8594cbdb36eac60ad851be6"
# Internal_Integration_Token = getattr(
#     settings, 'INTERNAL_INTEGRATION_TOKEN', 'Internal_Integration_Token')
Internal_Integration_Token = 'secret_36kmAz4GSNiTRbvKcfgSAKGkkawUSZSgMuPLpjhRDNx'
Notion = getattr(settings, 'NOTION_VERSION', 'Notion-version')
headers = {
    'Authorization': f'Bearer {Internal_Integration_Token}',
    'Notion-Version': Notion,
    "Content-Type": "application/json"
}


@shared_task
def set_data():
    data = load_notionAPI_demo()['body']
    temp = []
    for d in data:
        c, created = Demo.objects.update_or_create(
            title=d['title'], date=d['date'])
        c.description = d['description']
        c.video = d['video']
        c.save()
        temp.append([d['title'], d['date']])
    # Data Delete
    for db in Demo.objects.all():
        if not [db.title, db.date] in temp:
            Demo.objects.get(title=db.title, date=db.date).delete()


def get_block(id):
    url = f"https://api.notion.com/v1/blocks/{id}/children?page_size=100"
    response = http.request('GET',
                            url,  # json파일로 인코딩
                            headers=headers,
                            retries=False)
    source: Dict = loads(response.data.decode('utf-8'))  # 자료형 명시
    with open("data.json", "w") as f:
        json.dump(source, f)
    for r in source['results']:
        if 'paragraph' in r:
            text = r['paragraph']['text'][0]['plain_text']
            print(text)
            return text
        else:
            return ''


def print_block(data):
    for d in data:
        print(d['block'])
        if 'child' in d:
            print_block(d['child'])


def load_notionAPI_demo():
    url = f"https://api.notion.com/v1/databases/{Demo_Database_ID}/query"
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
            "property": "date",
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
        title = r['properties']['title']['title'][0]['plain_text']
        try:
            page_id = r['id']
            description = get_block(page_id)
        except:
            description = ''
        try:
            video = r['properties']['video']['files'][0]['name']
        except:
            video = ''
        try:
            date = r['properties']['date']['date']['start'].replace('/', '.')
        except:
            date = ''
        data.append({
            'title': title,
            'date': date,
            'description': description,
            'video': video
        })
    return {
        'statusCode': 200,
        'body': data
    }
