from django.shortcuts import render
import json
import urllib3
from typing import Dict
from json import loads
from datetime import datetime
import re
from django.conf import settings

import os


http = urllib3.PoolManager()
Page_ID = getattr(
    settings, 'PAGE_ID', 'Page_ID')
Internal_Integration_Token = getattr(
    settings, 'INTERNAL_INTEGRATION_TOKEN', 'Internal_Integration_Token')

headers = {
    'Authorization': f'Bearer {Internal_Integration_Token}',
    'Notion-Version': '2021-07-27',
    "Content-Type": "application/json"
}

# Create your views here.


def professor(request):
    page = load_notionAPI_professor()['body']
    return render(request, 'professor.html', {'page' : page})


def load_notionAPI_professor():
    url = f"https://api.notion.com/v1/blocks/{Page_ID}/children?page_size=100"
    response = http.request('GET',
                            url, # json파일로 인코딩
                            headers=headers,
                            retries=False)
    source: Dict = loads(response.data.decode('utf-8'))  # 자료형 명시
    page = []
    for r in source['results']:
        if 'paragraph' in r :
            line = r['paragraph']['text'][0]['plain_text']
            page.append({'text' : line, 'is_paragraph' : True})
        elif 'bulleted_list_item' in r :
            line = r['bulleted_list_item']['text'][0]['plain_text']
            page.append({'text' : line, 'is_paragraph' : False})
    return {
        'statusCode': 200,
        'body': page
    }