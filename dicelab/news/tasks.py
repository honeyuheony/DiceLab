from celery import shared_task
from django.conf import settings
from django.core.cache import cache
import json
import urllib3
from typing import Dict
from json import loads


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
def set_cache():
    cache.set('semester', load_notionAPI_course()['body'])

# Create your views here.


def load_notionAPI_course():
    url = f"https://api.notion.com/v1/databases/{News_Database_ID}/query"
    filter = {  # 가져올 데이터 필터
        "or": [
            {
                "property": "date",
                "date": {
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
    with open("data.json", "w") as f:
        json.dump(source['results'], f)

    data = []
    for r in source['results']:
        page_id = r['url'].split("-")[-1]
        temp = r['properties']['title']['title']
        title = ''
        for t in temp:
            title = title + t["plain_text"]
        page_url = f"https://api.notion.com/v1/blocks/{page_id}/children?page_size=100"
        response = http.request('GET',
                                page_url,  # json파일로 인코딩
                                headers=headers,
                                retries=False)
        source2: Dict = loads(response.data.decode('utf-8'))  # 자료형 명시
        page = []
        for r2 in source2['results']:
            text = r2['bulleted_list_item']['text'][0]['plain_text']
            for t in text:
                print(t["plain_text"])
    return {
        'statusCode': 200,
        'body': semester
    }
