from celery import shared_task
from django.conf import settings
from django.core.cache import cache
import json
import urllib3
from typing import Dict
from json import loads
from .models import News


http = urllib3.PoolManager()
Internal_Integration_Token = getattr(
    settings, 'INTERNAL_INTEGRATION_TOKEN', 'Internal_Integration_Token')
News_Database_ID = getattr(
    settings, 'NEWS_DATABASE_ID', 'news_database_ID')
Notion = getattr(settings, 'NOTION_VERSION', 'Notion-version')

headers = {
    'Authorization': f'Bearer {Internal_Integration_Token}',
    'Notion-Version': Notion,
    "Content-Type": "application/json"
}


@shared_task
def set_data():
    data = load_notionAPI_news()['body']
    temp = []
    for d in data:
        c, created = News.objects.update_or_create(
            title=d['title'], date=d['date'], content=json.dumps(d['content']))
        c.pic = d['pic']
        c.column_type = d['column_type']
        c.save()
        temp.append([d['title'], d['date'], json.dumps(d['content'])])
    # Data Delete
    for db in News.objects.all():
        if not [db.title, db.date, db.content] in temp:
            News.objects.get(title=db.title, date=db.date,
                             content=db.content).delete()


def get_block(id):
    url = f"https://api.notion.com/v1/blocks/{id}/children?page_size=100"
    response = http.request('GET',
                            url,  # json파일로 인코딩
                            headers=headers,
                            retries=False)
    source: Dict = loads(response.data.decode('utf-8'))  # 자료형 명시
    page = []
    for r in source['results']:
        block = {}
        if 'bulleted_list_item' in r:
            block['block'] = r['bulleted_list_item']['text'][0]['plain_text']
        else:
            continue
        if r['has_children']:
            block['child'] = get_block(r['id'])
        page.append(block)
    return page


def print_block(data):
    for d in data:
        print(d['block'])
        if 'child' in d:
            print_block(d['child'])


def load_notionAPI_news():
    url = f"https://api.notion.com/v1/databases/{News_Database_ID}/query"

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
            "direction": "ascending"
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
        temp = r['properties']['title']['title']
        title = ''
        for t in temp:
            title = title + t["plain_text"]

        try:
            date = r['properties']['date']['date']['start'].replace('/', '.')
        except:
            date = ''

        try:
            column_type = r['properties']['column_type']['select']['name']
        except:
            column_type = '..'

        try:
            page_id = r['id']
            content = get_block(page_id)
        except:
            content = ''

        try:
            pic = r['properties']['pic']['files'][0]['name']
        except:
            pic = ''

        data.append({'title': title, 'date': date,
                    'column_type': column_type, 'content': content, 'pic': pic})
    return {
        'statusCode': 200,
        'body': data
    }
