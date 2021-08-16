import json
import re
from datetime import datetime
from json import loads
from typing import Dict
import urllib3
from django.shortcuts import render
from django.conf import settings

# Create your views here.

# 환경 변수 가져오기
http = urllib3.PoolManager()
Database_ID = getattr(settings, 'DATABASES_ID', 'Database_ID')
Internal_Integration_Token = getattr(
    settings, 'INTERNAL_INTEGRATION_TOKEN', 'Internal_Integration_Token')


def project(request):
    data: Dict = load_notionAPI_project()
    print(data)
    return render(request, 'project.html', {'data': data})


def load_notionAPI_project():
    url = f"https://api.notion.com/v1/databases/{Database_ID}/query"
    headers = {
        'Authorization': f'Bearer {Internal_Integration_Token}',
        'Notion-Version': '2021-07-27',
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
    # 정규화 및 정제 후 json에 담기
    # for r in source['results']:
    #     title = '-'
    #     source = '-'
    #     year = '-'
    #     paper = "link"

    #     if 'Name' in r['properties'] and r['properties']['Name']['title']:
    #         p = re.compile(r"@\s*(?P<source>[\w\s-]+)[\W ]*(?P<year>\d{4})$")
    #         rawtitle = r['properties']['Name']['title'][0]['plain_text']
    #         if p.search(rawtitle):
    #             title = p.sub('', rawtitle)
    #             source = p.search(rawtitle).group('source')
    #             year = p.search(rawtitle).group('year')
    #         else:
    #             title = rawtitle
    #             paper = ''

    #     data.append({
    #         'date': r['properties']['Date']['date']['start'][2:] if 'Date' in r['properties'] else '19-01-01',
    #         'speaker': r['properties']['Assign']['people'][0]['name'] if 'Assign' in r['properties'] and r['properties']['Assign']['people'] else '-',
    #         'title': title,
    #         'source': r['properties']['Source']['select']['name'] if not source and 'Source' in r['properties'] else source,
    #         'year': r['properties']['Year']['number'] if not year and 'Year' in r['properties'] else year,
    #         'area': ', '.join([l['name'] for l in r['properties']['Label']['multi_select']]) if 'Label' in r['properties'] else '-',
    #         'slide': r['properties']["Slide link"]['url'] if 'Slide link' in r['properties'] else '',
    #     })
    #     if paper:
    #         data[-1]['paper'] = 'https://scholar.google.com/scholar?hl=ko&q=' + \
    #             data[-1]['title'].replace(' ', '+')
    #     if r['properties']['Status']['select']['name'] == 'To Review':
    #         data[-1]['title'] = '[To Review] '+data[-1]['title']

    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps(source)
    }
