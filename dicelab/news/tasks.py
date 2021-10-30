from celery import shared_task
from django.conf import settings
from django.core.cache import cache
import json
import urllib3
from typing import Dict
from json import loads
from .models import News


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
def set_data():
    data = load_notionAPI_news()['body']
    temp = []
    for d in data:
        c, created = News.objects.update_or_create(
            title=d['title'], date=d['date'], content=json.dumps(d['content']))
        c.pic = d['pic']
        c.save()
        temp.append([d['title'], d['date'], json.dumps(d['content'])])
    # Data Delete
    for db in News.objects.all():
        if not [db.title, db.date, db.content] in temp:
            News.objects.get(title=db.title, date=db.date,
                             content=db.content).delete()


def get_block(id):
    url = f"https://api.notion.com/v1/blocks/{id}/children?page_size=100"
    response = http.request('GET',
                            url,  # json파일로 인코딩
                            headers=headers,
                            retries=False)
    source: Dict = loads(response.data.decode('utf-8'))  # 자료형 명시
    page = []
    for r in source['results']:
        block = {}
        if 'bulleted_list_item' in r:
            block['block'] = r['bulleted_list_item']['text'][0]['plain_text']
        else:
            continue
        if r['has_children']:
            block['child'] = get_block(r['id'])
        page.append(block)
    return page


def print_block(data):
    for d in data:
        print(d['block'])
        if 'child' in d:
            print_block(d['child'])


def load_notionAPI_news():
    url = f"https://api.notion.com/v1/databases/{News_Database_ID}/query"

    filter = {  # 가져올 데이터 필터
        "or": [
            {
                "property": "title",
                "text": {
                    "is_not_empty": True
                }
            }
        ]
    }
    sorts = [  # 정렬
        {
            "property": "date",
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
        temp = r['properties']['title']['title']
        title = ''
        for t in temp:
            title = title + t["plain_text"]

        try:
            date = r['properties']['date']['date']['start'].replace('/', '.')
        except:
            date = ''

        try:
            column_type = r['properties']['column_type']['name']
        except:
            column_type = ''

        try:
            page_id = r['id']
            content = get_block(page_id)
        except:
            content = ''

        try:
            pic = r['properties']['pic']['files'][0]['name']
        except:
            pic = ''

        data.append({'title': title, 'date': date,
                    'column_type': column_type, 'content': content, 'pic': pic})
    return {
        'statusCode': 200,
        'body': data
    }


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

    data = []
    for n, r in enumerate(source['results']):
        try:
            temp = r['properties']['title']['title']
            title = ''
            for t in temp:
                title = title + t["plain_text"]
            date = r['properties']['date']['date']['start'].replace('/', '.')
            title = title + ' (' + date + ')'
        except:
            title = None

        try:
            where = r['properties']['where']['rich_text'][0]['plain_text']
        except:
            where = None

        try:
            subject = r['properties']['subject']['rich_text'][0]['plain_text']
            if '\n' in subject:
                subject = subject.split('\n')
        except:
            subject = None

        try:
            result = r['properties']['result']['rich_text'][0]['plain_text']
            if '\n' in result:
                result = result.split('\n')
        except:
            result = None

        try:
            participant = []
            temp = r['properties']['participant']['multi_select']
            for t in temp:
                participant.append(t['name'])
        except:
            participant = None

        try:
            pic = []
            temp = r['properties']['pic']['files']
            for t in temp:
                pic.append(t['name'])
        except:
            pic = []
        if len(pic):
            data_to_html = '<div class="news_have_pic"><li><h6>' + title + '</h6><ul>'
        else:
            data_to_html = '<div style="width:100%;"><li><h6>' + title + '</h6><ul>'
        if where != None:
            data_to_html += '<li>' + where + '</li>'
        if participant != None:
            data_to_html += '<li>' + ",".join(participant) + '</li>'
        if subject == None:
            if result != None:
                data_to_html += '<li>' + result + '</li>'
        else:
            for s, r in zip(subject, result):
                data_to_html += '<li>' + s + ' - ' + r + '</li>'
        data_to_html += '</ul></li></div>'

        if len(pic):
            if len(pic) == 1:
                for p in pic:
                    data_to_html += '<div class="news_img"><img src="../static/image/' + \
                        p + '" alt="loading"></div>'
            else:
                data_to_html += '</ul></li></div>'
                data_to_html += f'<div id="carouselExampleDark_ai{str(n+1)}" class="carousel carousel-dark slide mx-auto news_have_pic"'
                data_to_html += 'style="overflow: hidden;"data-bs-ride="carousel">'
                data_to_html += '<div class="carousel-indicators">'
                for i, p in enumerate(pic):
                    active = 'class="active"'
                    if i:
                        active = ''
                    data_to_html += f'<button type="button" data-bs-target="#carouselExampleDark_ai{str(n+1)}" data-bs-slide-to="{str(i)}" {active}'
                    data_to_html += f'aria-current="true" aria-label="Slide {str(i+1)}"></button>'
                data_to_html += '</div><div class="carousel-inner text-center">'
                for i, p in enumerate(pic):
                    active = 'active'
                    if not i:
                        active = ''
                    data_to_html += f'<div class="carousel-item {active}">'
                    data_to_html += f'<img class="d-block img-fluid w-100" style="width: 80%; height: 400px;"; src="../static/image/{p}" alt="loading">'
                    data_to_html += '<div class="carousel-caption d-md-block"></div></div>'
                data_to_html += '</div>'
                data_to_html += f'<button class="carousel-control-prev" type="button" data-bs-target="#carouselExampleDark_ai{str(n+1)}" data-bs-slide="prev">'
                data_to_html += '<span class="carousel-control-prev-icon" aria-hidden="true"></span>'
                data_to_html += '<span class="visually-hidden">Previous</span></button>'
                data_to_html += f'<button class="carousel-control-next" type="button" data-bs-target="#carouselExampleDark_ai{str(n+1)}" data-bs-slide="next">'
                data_to_html += '<span class="carousel-control-next-icon" aria-hidden="true"></span>'
                data_to_html += '<span class="visually-hidden">Next</span></button></div>'
        data.append({'title': title, 'date': date, 'htmldata': data_to_html})

    return {
        'statusCode': 200,
        'body': data
    }


def load_notionAPI_news_school():
    url = f"https://api.notion.com/v1/databases/{News_School_Database_ID}/query"

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

    data = []
    for r in source['results']:
        try:
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
            for t in temp:
                course.append(t['name'])
        except:
            course = None
        try:
            period = r['properties']['period']['rich_text'][0]['plain_text']
        except:
            period = None
        try:
            pic = []
            temp = r['properties']['pic']['files']
            for t in temp:
                pic.append(t['name'])
        except:
            pic = None

        data_to_html = '<div class="news_content"><li><h6>' + title + '</h6><ul>'
        if course != None:
            data_to_html += '<li>Courses<ul>'
            for c in course:
                data_to_html += '<li>' + c + '</li>'
            data_to_html += '</ul></li>'
        if period != None:
            data_to_html += '<li>기간: ' + period + '</li>'

        data_to_html += '</ul></li></div>'
        if pic != None:
            for p in pic:
                data_to_html += '<div><img  class="news_img" src="../static/image/' + \
                    p + '" alt="loading"></div>'
        data.append({'title': title, 'date': date, 'htmldata': data_to_html})
    return {
        'statusCode': 200,
        'body': data
    }


def load_notionAPI_news_thesis():
    url = f"https://api.notion.com/v1/databases/{News_Thesis_Database_ID}/query"

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

    data = []
    for r in source['results']:
        try:
            temp = r['properties']['title']['title']
            title = ''
            for t in temp:
                title = title + t["plain_text"]
            date = r['properties']['date']['date']['start'].replace('/', '.')
            title = title + ' (' + date + ')'
        except:
            title = None
        try:
            thesis_name = r['properties']['thesis_name']['rich_text'][0]['plain_text']
        except:
            thesis_name = None
        try:
            publication = r['properties']['publication']['rich_text'][0]['plain_text']
        except:
            publication = None
        try:
            participant = []
            temp = r['properties']['participant']['multi_select']
            for t in temp:
                participant.append(t['name'])
        except:
            participant = None
        try:
            pic = []
            temp = r['properties']['pic']['files']
            for t in temp:
                pic.append(t['name'])
        except:
            pic = None

        data_to_html = '<div class="news_content"><li><h6>' + title + '</h6><ul>'
        if thesis_name != None:
            data_to_html += '<li>' + thesis_name + '</li>'
        if participant != None:
            data_to_html += '<li>' + ','.join(participant) + '</li>'
        if participant != None:
            data_to_html += '<li>' + publication + '</li>'

        data_to_html += '</ul></li></div>'
        if pic != None:
            for p in pic:
                data_to_html += '<div><img  class="news_img" src="../static/image/' + \
                    p + '" alt="loading"></div>'
        data.append({'title': title, 'date': date, 'htmldata': data_to_html})
    return {
        'statusCode': 200,
        'body': data
    }


def load_notionAPI_news_work():
    url = f"https://api.notion.com/v1/databases/{News_Work_Database_ID}/query"

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
    data = []

    for r in source['results']:
        try:
            temp = r['properties']['title']['title']
            title = ''
            for t in temp:
                title = title + t["plain_text"]
            date = r['properties']['date']['date']['start'].replace('/', '.')
            title = title + ' (' + date + ')'
        except:
            title = None
        try:
            work_name = r['properties']['work_name']['rich_text'][0]['plain_text']
        except:
            work_name = None
        try:
            period = r['properties']['period']['rich_text'][0]['plain_text']
        except:
            period = None
        try:
            support = r['properties']['support']['rich_text'][0]['plain_text']
        except:
            support = None
        try:
            pic = []
            temp = r['properties']['pic']['files']
            for t in temp:
                pic.append(t['name'])
        except:
            pic = None

        data_to_html = '<div class="news_content"><li><h6>' + title + '</h6><ul>'
        if work_name != None:
            data_to_html += '<li>과제명: ' + work_name + '</li>'
        if period != None:
            data_to_html += '<li>기간: ' + period + '</li>'
        if support != None:
            data_to_html += '<li>지원: ' + support + '</li>'

        data_to_html += '</ul></li></div>'
        if pic != None:
            for p in pic:
                data_to_html += '<div><img  class="news_img" src="../static/image/' + \
                    p + '" alt="loading"></div>'
        data.append({'title': title, 'date': date, 'htmldata': data_to_html})
    return {
        'statusCode': 200,
        'body': data
    }


def load_notionAPI_news_researcher():
    url = f"https://api.notion.com/v1/databases/{News_Researcher_Database_ID}/query"

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
    data = []
    for r in source['results']:
        try:
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
            for t in temp:
                researcher.append(t['name'])
        except:
            researcher = None
        try:
            info = r['properties']['info']['rich_text'][0]['plain_text']
        except:
            info = None
        try:
            pic = []
            temp = r['properties']['pic']['files']
            for t in temp:
                pic.append(t['name'])
        except:
            pic = None

        data_to_html = '<div class="news_content"><li><h6>' + title + '</h6><ul>'
        if researcher != None:
            data_to_html += '<li>' + ','.join(researcher)
            if info != None:
                data_to_html += info + '</li>'
            else:
                data_to_html += '</li>'

        data_to_html += '</ul></li></div>'
        if pic != None:
            for p in pic:
                data_to_html += '<div><img  class="news_img" src="../static/image/' + \
                    p + '" alt="loading"></div>'
        data.append({'title': title, 'date': date, 'htmldata': data_to_html})
    return {
        'statusCode': 200,
        'body': data
    }


def load_notionAPI_news_etc():
    url = f"https://api.notion.com/v1/databases/{News_Etc_Database_ID}/query"

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
    data = []

    for r in source['results']:
        try:
            temp = r['properties']['title']['title']
            title = ''
            for t in temp:
                title = title + t["plain_text"]
            date = r['properties']['date']['date']['start'].replace('/', '.')
            title = title + ' (' + date + ')'
        except:
            title = None
        try:
            info = r['properties']['info']['rich_text'][0]['plain_text']
        except:
            info = None
        try:
            participant = []
            temp = r['properties']['participant']['multi_select']
            for t in temp:
                participant.append(t['name'])
            if len(participant) == 0:
                participant = None
        except:
            participant = None
        try:
            pic = []
            temp = r['properties']['pic']['files']
            for t in temp:
                pic.append(t['name'])
        except:
            pic = None

        data_to_html = '<div class="news_content"><li><h6>' + title + '</h6><ul>'
        if info != None:
            data_to_html += '<li>' + info + '</li>'
        if participant != None:
            data_to_html += '<li>' + ','.join(participant) + '</li>'

        data_to_html += '</ul></li></div>'
        if pic != None:
            for p in pic:
                data_to_html += '<div><img  class="news_img" src="../static/image/' + \
                    p + '" alt="loading"></div>'
        data.append({'title': title, 'date': date, 'htmldata': data_to_html})
    return {
        'statusCode': 200,
        'body': data
    }
