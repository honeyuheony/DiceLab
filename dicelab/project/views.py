import json
from json import loads
from typing import Dict
import urllib3
from django.shortcuts import render
from django.conf import settings


# 환경 변수 가져오기
http = urllib3.PoolManager()
Projects_Database_ID = getattr(
    settings, 'PROJECTS_DATABASES_ID', 'Database_ID')
AI_Challenge_Database_ID = getattr(
    settings, 'AI_CHALLENGE_DATABASES_ID', 'Database_ID')
Internal_Integration_Token = getattr(
    settings, 'INTERNAL_INTEGRATION_TOKEN', 'Internal_Integration_Token')
Notion = getattr(settings, 'NOTION_VERSION', 'Notion-version')


def project(request):
    projects = load_notionAPI_project()['body']
    ai_challenges = load_notionAPI_ai_challenge()['body']
    return render(request, 'project.html', {'projects': projects, 'ai_challenges': ai_challenges})


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
            'area': area
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
