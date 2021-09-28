import json
from json import loads
from typing import Dict
import urllib3
from django.conf import settings
from celery import shared_task
from .models import Project, AI_challenge


# 환경 변수 가져오기
http = urllib3.PoolManager()
Projects_Database_ID = getattr(
    settings, 'PROJECTS_DATABASES_ID', 'Database_ID')
AI_Challenge_Database_ID = getattr(
    settings, 'AI_CHALLENGE_DATABASES_ID', 'Database_ID')
Internal_Integration_Token = getattr(
    settings, 'INTERNAL_INTEGRATION_TOKEN', 'Internal_Integration_Token')
Notion = getattr(settings, 'NOTION_VERSION', 'Notion-version')


@shared_task
def set_data():
    p_data = load_notionAPI_project()['body']
    ai_data = load_notionAPI_ai_challenge()['body']
    temp = []
    for d in p_data:
        p, created = Project.objects.update_or_create(title=d['title'])
        p.date = d['date']
        p.status = d['status']
        p.assign = d['assign']
        p.area = d['area']
        p.label = d['label']
        p.save()
        temp.append(d['title'])
    for d in ai_data:
        a, created = AI_challenge.objects.update_or_create(title=d['title'])
        a.date = d['date']
        a.status = d['status']
        a.assign = d['assign']
        a.area = d['area']
        a.label = d['label']
        a.award = d['award']
        a.link = d['link']
        a.save()
        temp.append(d['title'])
    # Data Delete
    for db in Project.objects.all():
        if not db.title in temp:
            Project.objects.get(title=db.title).delete()
    for db in AI_challenge.objects.all():
        if not db.title in temp:
            AI_challenge.objects.get(title=db.title).delete()


def load_notionAPI_ai_challenge():
    url = f"https://api.notion.com/v1/databases/{AI_Challenge_Database_ID}/query"
    headers = {
        'Authorization': f'Bearer {Internal_Integration_Token}',
        'Notion-Version': Notion,
        "Content-Type": "application/json"
    }
    filter = {
        "or": [
            {
                "property": "status",
                "select": {
                            "is_not_empty": True
                }
            },
        ]
    }
    sorts = [
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
                            body=json.dumps(body),
                            headers=headers,
                            retries=False)

    source: Dict = loads(response.data.decode('utf-8'))
    data = []
    # 정규화 및 정제 후 json에 담기
    for r in source['results']:
        title = r['properties']['title']['title'][0]['plain_text']
        status = r['properties']['status']['select']['name']
        label = ', '.join([l['name'] for l in r['properties']['label']
                          ['multi_select']]) if 'label' in r['properties'] else 'None'
        assign = ', '.join([l['name'] for l in r['properties']['assign']
                            ['people']]) if 'assign' in r['properties'] else 'None'
        date = r['properties']['date']['date']['start'] + \
            " ~ " + r['properties']['date']['date']['end']
        link = r['properties']['link']['url'] if 'link' in r['properties'] else 'None'
        award = r['properties']['award']['rich_text'][0]['plain_text']
        area = r['properties']['area']['rich_text'][0]['plain_text']

        data.append({
            'title': title,
            'status': status,
            'link': link,
            'award': award,
            'area': area,
            'label': label,
            'assign': assign,
            'date': date,
        })
        # TODO implement
    return {
        'statusCode': 200,
        'body': data
    }


def load_notionAPI_project():
    url = f"https://api.notion.com/v1/databases/{Projects_Database_ID}/query"
    headers = {
        'Authorization': f'Bearer {Internal_Integration_Token}',
        'Notion-Version': Notion,
        "Content-Type": "application/json"
    }
    filter = {
        "or": [
            {
                "property": "Status",
                "select": {
                            "is_not_empty": True
                }
            },
        ]
    }
    sorts = [
        {
            "property": "Date",
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
        title = r['properties']['Title']['title'][0]['plain_text']
        status = r['properties']['Status']['select']['name']
        area = ', '.join([l['name'] for l in r['properties']['area']
                         ['multi_select']]) if 'area' in r['properties'] else 'None'
        label = ', '.join([l['name'] for l in r['properties']['label']
                          ['multi_select']]) if 'label' in r['properties'] else 'None'
        assign = ', '.join([l['name'] for l in r['properties']['assign']
                            ['people']]) if 'assign' in r['properties'] else 'None'
        date = r['properties']['Date']['date']['start'] + \
            " ~ " + r['properties']['Date']['date']['end']

        data.append({
            'title': title,
            'status': status,
            'area': area,
            'label': label,
            'assign': assign,
            'date': date
        })
        # TODO implement
    return {
        'statusCode': 200,
        'body': data
    }
