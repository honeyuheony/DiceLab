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
News_AI_Database_ID = getattr(
    settings, 'NEWS_AI_DATABASE_ID', 'news_ai_database_ID')
News_School_Database_ID = getattr(
    settings, 'NEWS_SCHOOL_DATABASE_ID', 'news_school_database_ID')
News_Thesis_Database_ID = getattr(
    settings, 'NEWS_THESIS_DATABASE_ID', 'news_thesis_database_ID')
News_Work_Database_ID = getattr(
    settings, 'NEWS_WORK_DATABASE_ID', 'news_work_database_ID')
News_Researcher_Database_ID = getattr(
    settings, 'NEWS_RESEARCHER_DATABASE_ID', 'news_researcher_database_ID')
News_Etc_Database_ID = getattr(
    settings, 'NEWS_ETC_DATABASE_ID', 'news_etc_database_ID')
Notion = getattr(settings, 'NOTION_VERSION', 'Notion-version')

headers = {
    'Authorization': f'Bearer {Internal_Integration_Token}',
    'Notion-Version': Notion,
    "Content-Type": "application/json"
}


@shared_task
def set_cache():
    cache.set('news', load_notionAPI_news()['body'])

def set_database():
    print(load_notionAPI_news_ai()['body'])
    print(load_notionAPI_news_school()['body'])
    print(load_notionAPI_news_thesis()['body'])
    print(load_notionAPI_news_work()['body'])
    print(load_notionAPI_news_researcher()['body'])
    print(load_notionAPI_news_etc()['body'])
set_database()
# Create your views here.


def load_notionAPI_news_ai():
    url = f"https://api.notion.com/v1/databases/{News_AI_Database_ID}/query"
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

    data = {}
    for r in source['results']:
        try :
            temp = r['properties']['title']['title']
            title = ''
            for t in temp:
                title = title + t["plain_text"]
            date = r['properties']['date']['date']['start'].replace('/', '.')
            title = title + ' (' + date + ')'
        except:
            title = None

        try :
            where = r['properties']['where']['rich_text'][0]['plain_text']
        except:
            where = None

        try:
            subject = r['properties']['subject']['rich_text'][0]['plain_text']
            if '\n' in subject :
                subject = subject.split('\n')
        except:
            subject = None

        try:
            result = r['properties']['result']['rich_text'][0]['plain_text']
            if '\n' in result :
                result = result.split('\n')
        except:
            result = None

        try:
            participant = []
            temp = r['properties']['participant']['multi_select']
            for t in temp :
                participant.append(t['name'])
        except:
            participant = None

        try:
            pic = []
            temp = r['properties']['pic']['files']
            for t in temp :
                pic.append(t['name'])
        except:
            pic = None

        data_to_html = '<li><h6>' + title + '</h6><ul>'
        if where != None :
            data_to_html += '<li>' + where + '</li>'
        if participant != None :
            data_to_html += '<li>' + ",".join(participant) + '</li>'
        if subject == None :
            data_to_html += '<li>' + result + '</li>'
        else :
            for s, r in zip(subject, result) :
                data_to_html += '<li>' + s + ' - ' + r + '</li>'
        if pic != None :
            for p in pic :
                data_to_html += '<div><img src="{% get_static_prefix %}image/news/ai/' + p + '" alt="loading"></div>'
        data_to_html += '</ul></li>'
        data.append({'date' : date, 'code' : data_to_html})
    return {
        'statusCode': 200,
        'body': data
    }

def load_notionAPI_news_school():
    url = f"https://api.notion.com/v1/databases/{Database_ID}/query"
    
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

    for r in source['results']:
        try :
            temp = r['properties']['title']['title']
            title = ''
            for t in temp:
                title = title + t["plain_text"]
            date = r['properties']['date']['date']['start'].replace('/', '.')
            title = title + ' (' + date + ')'
        except:
            title = None
        try:
            course = []
            temp = r['properties']['course']['multi_select']
            for t in temp :
                course.append(t['name'])
        except:
            course = None
        try :
            period = r['properties']['period']['rich_text'][0]['plain_text']
        except:
            period = None
        try:
            pic = []
            temp = r['properties']['pic']['files']
            for t in temp :
                pic.append(t['name'])
        except:
            pic = None

        data_to_html = '<li><h6>' + title + '</h6><ul>'
        if course != None :
            data_to_html += '<li>Courses<ul>'
            for c in course :
                data_to_html += '<li>' + c + '</li>'
            data_to_html += '</ul></li>'
        if period != None :
            data_to_html += '<li>기간: ' + period + '</li>'
        if pic != None :
            for p in pic :
                data_to_html += '<div><img src="{% get_static_prefix %}image/news/ai/' + p + '" alt="loading"></div>'
        data_to_html += '</ul></li>'
        data.append({'date' : date, 'code' : data_to_html})
    return {
        'statusCode': 200,
        'body': data
    }

def load_notionAPI_news_thesis():
    url = f"https://api.notion.com/v1/databases/{Database_ID}/query"
    
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

    for r in source['results']:
        try :
            temp = r['properties']['title']['title']
            title = ''
            for t in temp:
                title = title + t["plain_text"]
            date = r['properties']['date']['date']['start'].replace('/', '.')
            title = title + ' (' + date + ')'
        except:
            title = None
        try :
            thesis_name = r['properties']['thesis_name']['rich_text'][0]['plain_text']
        except:
            thesis_name = None
        try :
            publication = r['properties']['publication']['rich_text'][0]['plain_text']
        except:
            publication = None
        try:
            participant = []
            temp = r['properties']['participant']['multi_select']
            for t in temp :
                participant.append(t['name'])
        except:
            participant = None

        data_to_html = '<li><h6>' + title + '</h6><ul>'
        if thesis_name != None :
            data_to_html += '<li>' + thesis_name + '</li>'
        if participant != None :
            data_to_html += '<li>' + ','.join(participant) + '</li>'
        if participant != None :
            data_to_html += '<li>' + publication + '</li>'
        if pic != None :
            for p in pic :
                data_to_html += '<div><img src="{% get_static_prefix %}image/news/ai/' + p + '" alt="loading"></div>'
        data_to_html += '</ul></li>'
        data.append({'date' : date, 'code' : data_to_html})
    return {
        'statusCode': 200,
        'body': data
    }

def load_notionAPI_news_work():
        url = f"https://api.notion.com/v1/databases/{Database_ID}/query"
    
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

    for r in source['results']:
        try :
            temp = r['properties']['title']['title']
            title = ''
            for t in temp:
                title = title + t["plain_text"]
            date = r['properties']['date']['date']['start'].replace('/', '.')
            title = title + ' (' + date + ')'
        except:
            title = None
        try :
            work_name = r['properties']['work_name']['rich_text'][0]['plain_text']
        except:
            work_name = None
        try :
            period = r['properties']['period']['rich_text'][0]['plain_text']
        except:
            period = None
        try :
            support = r['properties']['support']['rich_text'][0]['plain_text']
        except:
            support = None

        data_to_html = '<li><h6>' + title + '</h6><ul>'
        if work_name != None :
            data_to_html += '<li>과제명: ' + work_name + '</li>'
        if period != None :
            data_to_html += '<li>기간: ' + period + '</li>'
        if support != None :
            data_to_html += '<li>지원: ' + support + '</li>'
        if pic != None :
            for p in pic :
                data_to_html += '<div><img src="{% get_static_prefix %}image/news/ai/' + p + '" alt="loading"></div>'
        data_to_html += '</ul></li>'
        data.append({'date' : date, 'code' : data_to_html})
    return {
        'statusCode': 200,
        'body': data
    }

def load_notionAPI_news_researcher():
    url = f"https://api.notion.com/v1/databases/{Database_ID}/query"
    
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

    for r in source['results']:
        try :
            temp = r['properties']['title']['title']
            title = ''
            for t in temp:
                title = title + t["plain_text"]
            date = r['properties']['date']['date']['start'].replace('/', '.')
            title = title + ' (' + date + ')'
        except:
            title = None
        try:
            researcher = []
            temp = r['properties']['researcher']['multi_select']
            for t in temp :
                researcher.append(t['name'])
        except:
            researcher = None
        try :
            info = r['properties']['info']['rich_text'][0]['plain_text']
        except:
            info = None

        data_to_html = '<li><h6>' + title + '</h6><ul>'
        if researcher != None :
            data_to_html += '<li>' + ','.join(researcher)
            if info != None :
                data_to_html += info + '</li>'
            else :
                data_to_html += '</li>'
        if pic != None :
            for p in pic :
                data_to_html += '<div><img src="{% get_static_prefix %}image/news/ai/' + p + '" alt="loading"></div>'
        data_to_html += '</ul></li>'
        data.append({'date' : date, 'code' : data_to_html})
    return {
        'statusCode': 200,
        'body': data
    }

def load_notionAPI_news_etc():
    url = f"https://api.notion.com/v1/databases/{Database_ID}/query"
    
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

    for r in source['results']:
        try :
            temp = r['properties']['title']['title']
            title = ''
            for t in temp:
                title = title + t["plain_text"]
            date = r['properties']['date']['date']['start'].replace('/', '.')
            title = title + ' (' + date + ')'
        except:
            title = None
        try :
            info = r['properties']['info']['rich_text'][0]['plain_text']
        except:
            info = None
        try:
            participant = []
            temp = r['properties']['participant']['multi_select']
            for t in temp :
                participant.append(t['name'])
        except:
            participant = None
        try:
            pic = []
            temp = r['properties']['pic']['files']
            for t in temp :
                pic.append(t['name'])
        except:
            pic = None

        data_to_html = '<li><h6>' + title + '</h6><ul>'
        if info != None :
            data_to_html += '<li>' + info + '</li>'
        if participant != None :
            data_to_html += '<li>' + ','.join(participant) + '</li>'
        if pic != None :
            for p in pic :
                data_to_html += '<div><img src="{% get_static_prefix %}image/news/ai/' + p + '" alt="loading"></div>'
        data_to_html += '</ul></li>'
        data.append({'date' : date, 'code' : data_to_html})
    return {
        'statusCode': 200,
        'body': data
    }