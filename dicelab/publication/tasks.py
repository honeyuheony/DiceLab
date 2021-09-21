from celery import shared_task
from django.conf import settings
import urllib3
from typing import Dict
import json
from json import loads
from .models import Patents, Publication

# 환경 변수 가져오기
http = urllib3.PoolManager()
Publication_Database_ID = getattr(
    settings, 'PUBLICATION_DATABASE_ID', 'Database_ID')
Patents_Database_ID = getattr(
    settings, 'PATENTS_DATABASE_ID', 'Database_ID')
Internal_Integration_Token = getattr(
    settings, 'INTERNAL_INTEGRATION_TOKEN', 'Internal_Integration_Token')
Notion = getattr(settings, 'NOTION_VERSION', 'Notion-version')


@shared_task
def set_data():
    pub_data = load_notionAPI_publication()['body']
    pat_data = load_notionAPI_patents()['body']
    for d in pub_data:
        Publication.objects.update_or_create(
            title=d['title'], label=d['label'], paper_link=d['paper_link'], assign=d['assign'], thesis=d['thesis'], year=d['year'])
    for d in pat_data:
        Patents.objects.update_or_create(
            title=d['title'], country=d['country'], num=d['num'], year=d['year'], assign=d['assign'])


def load_notionAPI_publication():
    url = f"https://api.notion.com/v1/databases/{Publication_Database_ID}/query"
    headers = {
        'Authorization': f'Bearer {Internal_Integration_Token}',
        'Notion-Version': Notion,
        "Content-Type": "application/json"
    }
    filter = {
        "or": [
            {
                "property": "label",
                "select": {
                            "is_not_empty": True
                }
            },
        ]
    }
    sorts = [
        {
            "property": "year",
            "direction": "descending"
        }
    ]
    body = {
        "filter": filter,
        "sorts": sorts
    }
    response = http.request('POST',
                            url,
                            body=json.dumps(body),
                            headers=headers,
                            retries=False)

    source: Dict = loads(response.data.decode('utf-8'))
    data = []
    # 정규화 및 정제 후 json에 담기
    for r in source['results']:
        title = r['properties']['title']['title'][0]['plain_text']
        label = r['properties']['label']['select']['name']
        paper_link = r['properties']['paper link']['url']
        thesis = r['properties']['thesis']['rich_text'][0]['plain_text']
        year = r['properties']['year']['select']['name']
        assign = ', '.join([l['name'] for l in r['properties']['assign']
                            ['multi_select']]) if 'assign' in r['properties'] else 'None'

        data.append({
            'title': title,
            'label': label,
            'paper_link': paper_link,
            'thesis': thesis,
            'year': year,
            'assign': assign,
        })
        # TODO implement
    return {
        'statusCode': 200,
        'body': data
    }


def load_notionAPI_patents():
    url = f"https://api.notion.com/v1/databases/{Patents_Database_ID}/query"
    headers = {
        'Authorization': f'Bearer {Internal_Integration_Token}',
        'Notion-Version': Notion,
        "Content-Type": "application/json"
    }
    filter = {
        "or": [
            {
                "property": "year",
                "select": {
                            "is_not_empty": True
                }
            },
        ]
    }
    sorts = [
        {
            "property": "year",
            "direction": "descending"
        }
    ]
    body = {
        "filter": filter,
        "sorts": sorts
    }
    response = http.request('POST',
                            url,
                            body=json.dumps(body),
                            headers=headers,
                            retries=False)

    source: Dict = loads(response.data.decode('utf-8'))
    data = []
    # 정규화 및 정제 후 json에 담기
    for r in source['results']:
        title = r['properties']['title']['title'][0]['plain_text']
        country = r['properties']['country']['select']['name']
        num = r['properties']['num']['rich_text'][0]['plain_text']
        year = r['properties']['year']['select']['name']
        assign = ', '.join([l['name'] for l in r['properties']['assign']
                            ['multi_select']]) if 'assign' in r['properties'] else 'None'

        data.append({
            'title': title,
            'country': country,
            'num': num,
            'year': year,
            'assign': assign,
        })
        # TODO implement
    return {
        'statusCode': 200,
        'body': data
    }
