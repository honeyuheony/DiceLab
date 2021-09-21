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
    cache.set('news', load_notionAPI_news()['body'])

# Create your views here.


def load_notionAPI_news():
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
                            body=json.dumps(body),  
                            headers=headers,
                            retries=False)
    source: Dict = loads(response.data.decode('utf-8'))
    data = []
    for r in source['results']:  
        page_id = r['url'].split("-")[-1]
        card = {}
        temp = r['properties']['title']['title']
        title = ''
        for t in temp:
            title = title + t["plain_text"] # news title
        card['title'] = title
        page_url = f"https://api.notion.com/v1/blocks/{page_id}/children?page_size=100"
        response = http.request('GET',
                                page_url,  
                                headers=headers,
                                retries=False)
        source2: Dict = loads(response.data.decode('utf-8'))
        
        # page inner
        content = []
        for r2 in source2['results']:
            block = {}
            if 'text' in r2: # text 요소로 시작하는 경우는 노션페이지 데이터가 한 줄이다.
                text = r2['paragraph']['text'][0]['plain_text']
                block['parent'] = text
                content.append(block)
                break
            elif 'bulleted_list_item' in r2:
                text = r2['bulleted_list_item']['text'][0]['plain_text']
                block['parent'] = text
                if r2['has_children']:
                    child_id = r2['id']
                    child_url = f'https://api.notion.com/v1/blocks/{child_id}/children'
                    response2 = http.request('GET',
                                                child_url,  # json파일로 인코딩
                                                headers=headers,
                                                retries=False)
                    source3: Dict = loads(
                        response2.data.decode('utf-8'))
                    block_child = [] 
                    # page_child
                    for r3 in source3['results']:
                        subtext = r3['bulleted_list_item']['text'][0]['plain_text']
                        block_child.append(subtext)
                    block['child'] = block_child
                content.append(block)
        card['content'] = content        
        data.append(card)        
    return {
        'statusCode': 200,
        'body': data
    }
