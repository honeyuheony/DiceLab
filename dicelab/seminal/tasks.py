import json
import urllib3
from typing import Dict
from json import loads
from django.conf import settings
from celery import shared_task
from .models import Seminal
import re

http = urllib3.PoolManager()
Seminal_Database_ID = getattr(
    settings, 'SEMINAL_DATABASE_ID', 'Seminal_Database_ID')
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
    data = load_notionAPI_seminal()['body']
    temp = []
    for d in data:
        s, created = Seminal.objects.update_or_create(
            title=d['title'])
        s.date = d['date']
        s.speaker = d['speaker']
        s.source = d['source']
        s.year = d['year']
        s.area = d['area']
        s.paper = d['paper']
        s.save()
        temp.append(d['title'])
    # Data Delete
    for db in Seminal.objects.all():
        if not db.title in temp:
            Seminal.objects.get(title=db.title).delete()


def load_notionAPI_seminal():
    url = f"https://api.notion.com/v1/databases/{Seminal_Database_ID}/query"
    filter = {  # 가져올 데이터 필터
        "or": [
                {
                    "property": "Status",
                    "select": {
                        "equals": "Done"
                    }
                },
            {
                    "property": "Status",
                    "select": {
                        "equals": "To Review"
                    }
                }
        ]
    }
    sorts = [  # 정렬
        {
            "property": "Date",
            "direction": "descending"
        }
    ]
    # 첫번째 100개 데이터 호출
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

    # # 두 번째 100개 데이터 호출
    # body2 = {
    #     "filter": filter,
    #     "sorts": sorts,
    #     "start_cursor": source['next_cursor']
    # }

    # response2 = http.request('POST',
    #                          url,
    #                          body=json.dumps(body2),
    #                          headers=headers,
    #                          retries=False)
    # source2: Dict = loads(response2.data.decode('utf-8'))

    # source['results'] += source2['results']

    data = []
    for r in source['results']:
        title = '-'
        source = '-'
        year = '-'
        paper = "link"

        if 'Name' in r['properties'] and r['properties']['Name']['title']:
            p = re.compile(r"@\s*(?P<source>[\w\s-]+)[\W ]*(?P<year>\d{4})$")
            rawtitle = r['properties']['Name']['title'][0]['plain_text']
            if p.search(rawtitle):
                title = p.sub('', rawtitle)
                source = p.search(rawtitle).group('source')
                year = p.search(rawtitle).group('year')
            else:
                title = rawtitle
                paper = ''

        data.append({
            'date': r['properties']['Date']['date']['start'][2:] if 'Date' in r['properties'] else '19-01-01',
            'speaker': r['properties']['Assign']['people'][0]['name'] if 'Assign' in r['properties'] and r['properties']['Assign']['people'] else '-',
            'title': title,
            'source': r['properties']['Source']['select']['name'] if not source and 'Source' in r['properties'] else source,
            'year': r['properties']['Year']['number'] if not year and 'Year' in r['properties'] else year,
            'area': ', '.join([l['name'] for l in r['properties']['Label']['multi_select']]) if 'Label' in r['properties'] else '-',
            'slide': r['properties']["Slide link"]['url'] if 'Slide link' in r['properties'] else '',
        })
        if paper:
            data[-1]['paper'] = 'https://scholar.google.com/scholar?hl=ko&q=' + \
                data[-1]['title'].replace(' ', '+')
        if r['properties']['Status']['select']['name'] == 'To Review':
            data[-1]['title'] = '[To Review] '+data[-1]['title']

    return {
        'statusCode': 200,
        'body': data
    }