from celery import shared_task
from django.conf import settings
from django.core.cache import cache
import urllib3
from typing import Dict
from json import loads

http = urllib3.PoolManager()
Page_ID = getattr(
    settings, 'PAGE_ID', 'Page_ID')
Internal_Integration_Token = getattr(
    settings, 'INTERNAL_INTEGRATION_TOKEN', 'Internal_Integration_Token')
Notion = getattr(settings, 'NOTION_VERSION', 'Notion-version')

headers = {
    'Authorization': f'Bearer {Internal_Integration_Token}',
    'Notion-Version': Notion,
    "Content-Type": "application/json"
}

# Create your views here.


@shared_task
def set_cache():
    cache.set('page', load_notionAPI_professor()['body'])


def load_notionAPI_professor():
    url = f"https://api.notion.com/v1/blocks/{Page_ID}/children?page_size=100"
    response = http.request('GET',
                            url,  # json파일로 인코딩
                            headers=headers,
                            retries=False)
    source: Dict = loads(response.data.decode('utf-8'))  # 자료형 명시
    page = []
    for r in source['results']:
        if 'paragraph' in r:
            line = r['paragraph']['text'][0]['plain_text']
            page.append({'text': line, 'is_paragraph': True})
        elif 'bulleted_list_item' in r:
            line = r['bulleted_list_item']['text'][0]['plain_text']
            page.append({'text': line, 'is_paragraph': False})
    return {
        'statusCode': 200,
        'body': page
    }
