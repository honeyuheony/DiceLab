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
Member_Graduate_Database_ID = getattr(
    settings, 'MEMBER_GRADUATE_DATABASE_ID', 'member_graduate_database_ID')
Member_Ungraduate_Database_ID = getattr(
    settings, 'MEMBER_UNGRADUATE_DATABASE_ID', 'member_ungraduate_database_ID')
Member_Urp_Database_ID = getattr(
    settings, 'MEMBER_URP_DATABASE_ID', 'member_urp_database_ID')
Member_Alumni_Database_ID = getattr(
    settings, 'MEMBER_ALUMNI_DATABASE_ID', 'member_alumni_database_ID')
Internal_Integration_Token = getattr(
    settings, 'INTERNAL_INTEGRATION_TOKEN', 'Internal_Integration_Token')

headers = {
    'Authorization': f'Bearer {Internal_Integration_Token}',
    'Notion-Version': '2021-07-27',
    "Content-Type": "application/json"
}

# Create your views here.


def member(request):
    graduate = load_notionAPI_member_graduate()['body']
    ungraduate = load_notionAPI_member_ungraduate()['body']
    urp = load_notionAPI_member_urp()['body']
    alumni = load_notionAPI_member_alumni()['body']

    return render(request, 'member.html', {
        'graduate': graduate, 'ungraduate': ungraduate, 'urp': urp, 'alumni': alumni})


def load_notionAPI_member_graduate():
    url = f"https://api.notion.com/v1/databases/{Member_Graduate_Database_ID}/query"
    filter = {  # 가져올 데이터 필터
        "or": [
            {
                "property": "course",
                "select": {
                    "is_not_empty": True
                }
            }
        ]
    }
    sorts = [  # 정렬
        {
            "property": "admission_date",
            "direction": "ascending"
        },
        {
            "property": "name",
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
    data = []
    for r in source['results']:
        name = r['properties']['name']['title'][0]['plain_text']
        course = r['properties']['course']['select']['name']
        admission_date = r['properties']['admission_date']['select']['name']
        research_interests = [l['name']
                              for l in r['properties']['research_interests']['multi_select']]
        email = r['properties']['email']['rich_text'][0]['plain_text']
        linked = '-'

        data.append({
            'name': name,
            'course': course,
            'admission_date': admission_date,
            'research_interests': research_interests,
            'email': email,
            'linked': linked
        })
    return {
        'statusCode': 200,
        'body': data
    }


def load_notionAPI_member_ungraduate():
    url = f"https://api.notion.com/v1/databases/{Member_Ungraduate_Database_ID}/query"
    filter = {  # 가져올 데이터 필터
        "or": [
            {
                "property": "course",
                "select": {
                    "is_not_empty": True
                }
            }
        ]
    }
    sorts = [  # 정렬
        {
            "property": "course",
            "direction": "descending"
        },
        {
            "property": "name",
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
        name = r['properties']['name']['title'][0]['plain_text']
        course = r['properties']['course']['select']['name']
        research_interests = [l['name']
                              for l in r['properties']['research_interests']['multi_select']]
        email = r['properties']['email']['rich_text'][0]['plain_text'] if len(
            r['properties']['email']['rich_text']) != 0 else ''

        data.append({
            'name': name,
            'course': course,
            'research_interests': research_interests,
            'email': email
        })
    return {
        'statusCode': 200,
        'body': data
    }


def load_notionAPI_member_urp():
    url = f"https://api.notion.com/v1/databases/{Member_Urp_Database_ID}/query"
    sorts = [  # 정렬
        {
            "property": "course",
            "direction": "descending"
        },
        {
            "property": "team",
            "direction": "ascending"
        },
        {
            "property": "name",
            "direction": "ascending"
        }
    ]
    team_list = {'3_1': [], '4_1': [], '4_2': []}
    for key in team_list:
        filter = {  # 가져올 데이터 필터
            "or": [
                {
                    "property": "team",
                    "select": {
                        "equals": key
                    }
                }
            ]
        }
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
        for r in source['results']:
            name = r['properties']['name']['title'][0]['plain_text']
            team_list[key].append(name)
        team_list[key] = ', '.join(team_list[key])
    data = team_list
    return {
        'statusCode': 200,
        'body': data
    }


def load_notionAPI_member_alumni():
    url = f"https://api.notion.com/v1/databases/{Member_Alumni_Database_ID}/query"
    team_list = {'2020_1': [], '2020_2': [], '2020_3': [], '2021_1': [],
                 '2021_2': [], '2022_1': [], '2022_2': [], '2022_3': []}
    sorts = [  # 정렬
        {
            "property": "name",
            "direction": "ascending"
        }
    ]
    for key in team_list:
        filter = {  # 가져올 데이터 필터
            "or": [
                {
                    "property": "team",
                    "select": {
                        "equals": key
                    }
                }
            ]
        }
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
        for r in source['results']:
            name = r['properties']['name']['title'][0]['plain_text']
            team_list[key].append(name)
        team_list[key] = ', '.join(team_list[key])
    data = team_list
    return {
        'statusCode': 200,
        'body': data
    }
