from celery import shared_task
from django.conf import settings
import urllib3
from typing import Dict
import json
from json import loads
from .models import Dissertation, Master, Research_interests, Linked, Graduated, Alumni, Team, Project

http = urllib3.PoolManager()
Member_Graduate_Database_ID = getattr(
    settings, 'MEMBER_GRADUATE_DATABASE_ID', 'member_graduate_database_ID')
Member_Ungraduate_Database_ID = getattr(
    settings, 'MEMBER_UNGRADUATE_DATABASE_ID', 'member_ungraduate_database_ID')
Member_Urp_Database_ID = getattr(
    settings, 'MEMBER_URP_DATABASE_ID', 'member_urp_database_ID')
Member_Alumni_Database_ID = getattr(
    settings, 'MEMBER_ALUMNI_DATABASE_ID', 'member_alumni_database_ID')
Member_Master_Database_ID = getattr(
    settings, 'MEMBER_MASTER_DATABASE_ID', 'member_master_database_ID')
Notion = getattr(settings, 'NOTION_VERSION', 'Notion-version')
Internal_Integration_Token = getattr(
    settings, 'INTERNAL_INTEGRATION_TOKEN', 'Internal_Integration_Token')

headers = {
    'Authorization': f'Bearer {Internal_Integration_Token}',
    'Notion-Version': Notion,
    "Content-Type": "application/json"
}


@shared_task
def set_data():

    temp = []
    temp_master = []
    research_interests_temp = []
    linked_temp = []
    team_temp = []
    project_temp = []
    dissertation_temp = []

    # Data Create or Update
    # Graduate
    data = load_notionAPI_member_graduate()['body']
    for d in data:
        g, created = Graduated.objects.update_or_create(
            name=d['name'])
        g.course = d['course']
        g.admission_date = d['admission_date']
        g.email = d['email']
        g.pic = d['pic']
        g.research_interests.clear()
        count = 0
        for r in d['research_interests']:
            if count < 3:
                obj, created = Research_interests.objects.get_or_create(
                    title=r)
                g.research_interests.add(obj)
                research_interests_temp.append(r)
                g.save()
                count += 1
        g.linked.clear()
        if d['linked'] != None:
            for key, value in d['linked'].items():
                obj, created = Linked.objects.get_or_create(
                    title=key.replace(" : ", ""), link=value)
                g.linked.add(obj)
                linked_temp.append(obj.title)
                g.save()
        temp.append(d['name'])
    # Alumni
    data = load_notionAPI_member_alumni()['body']
    for d in data:
        a, created = Alumni.objects.update_or_create(
            name=d['name'])
        a.graduate_year = d['graduate_year']
        if d['course'] != None:
            a.course = d['course']
        else:
            a.course = ''
        obj, created = Team.objects.get_or_create(title=d['team'])
        a.team.add(obj)
        team_temp.append(obj.title)
        a.save()
        if d['project'] != None:
            obj, created = Project.objects.get_or_create(
                title=d['project'], year=d['graduate_year'])
            a.project.add(obj)
            project_temp.append(obj.title)
            a.save()
        temp.append(d['name'])
    # Master
    data = load_notionAPI_member_master()['body']
    for d in data:
        g, created = Master.objects.update_or_create(
            name=d['name'])
        g.graduate_year = d['graduate_year']
        g.email = d['email']
        g.pic = d['pic']
        if d['dissertation'] != None:
            obj, created = Dissertation.objects.update_or_create(
                title=d['dissertation'], paper_link=d['paper_link'], slide_link=d['slide_link'])
            dissertation_temp.append(obj)
            g.dissertation.add(obj)
            g.save()
        g.linked.clear()
        if d['linked'] != None:
            for key, value in d['linked'].items():
                obj, created = Linked.objects.get_or_create(
                    title=key.replace(" : ", ""), link=value)
                g.linked.add(obj)
                linked_temp.append(obj.title)
                g.save()
        temp_master.append(d['name'])

    # Data Delete
    for db in Graduated.objects.all():
        if not db.name in temp:
            Graduated.objects.get(name=db.name).delete()
    for db in Alumni.objects.all():
        if not db.name in temp:
            Alumni.objects.get(name=db.name).delete()
    for db in Master.objects.all():
        if not db.name in temp_master:
            Master.objects.get(name=db.name).delete()

    for db in Research_interests.objects.all():
        if not db.title in research_interests_temp:
            Research_interests.objects.get(title=db.title).delete()
    for db in Linked.objects.all():
        if not db.title in linked_temp:
            Linked.objects.get(title=db.title).delete()
    for db in Team.objects.all():
        if not db.title in team_temp:
            Team.objects.get(title=db.title).delete()
    for db in Project.objects.all():
        if not db.title in project_temp:
            Project.objects.get(title=db.title).delete()
    for db in Dissertation.objects.all():
        if not db in dissertation_temp:
            db.delete()


def load_notionAPI_member_master():
    url = f"https://api.notion.com/v1/databases/{Member_Master_Database_ID}/query"
    filter = {  # 가져올 데이터 필터
        "or": [
            {
                "property": "name",
                "text": {
                    "is_not_empty": True
                }
            }
        ]
    }
    sorts = [  # 정렬
        {
            "property": "graduate_year",
            "direction": "descending"
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
        try:
            name = r['properties']['name']['title'][0]['plain_text']
        except:
            continue

        try:
            graduate_year = r['properties']['graduate_year']['select']['name']
        except:
            graduate_year = ''
        try:
            dissertation = r['properties']['dissertation']['select']['name']
        except:
            dissertation = ''
        try:
            email = r['properties']['email']['email'].replace("@", "'at'")
        except:
            email = ''
        links = ''
        try:
            temp = r['properties']['linked']['rich_text']
            for t in temp:
                links += t['plain_text']
            links = links.split("\n")
            link_title = []
            link_content = []
            for link in links:
                if " : " in link:
                    link_title.append(link)
                else:
                    link_content.append(link)
            linked = dict(zip(link_title, link_content))
        except:
            linked = {}
        try:
            pic = r['properties']['pic']['files'][0]['name']
        except:
            pic = ''
        try:
            paper_link = r['properties']['paper_link']['url']
        except:
            paper_link = ''
        try:
            slide_link = r['properties']['slide_link']['url']
        except:
            slide_link = ''
        data.append({
            'name': name,
            'graduate_year': graduate_year,
            'dissertation': dissertation,
            'email': email,
            'linked': linked,
            'pic': pic,
            'paper_link': paper_link,
            'slide_link': slide_link
        })
    return {
        'statusCode': 200,
        'body': data
    }


def load_notionAPI_member_graduate():
    url = f"https://api.notion.com/v1/databases/{Member_Graduate_Database_ID}/query"
    filter = {  # 가져올 데이터 필터
        "or": [
            {
                "property": "name",
                "text": {
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
            "property": "admission_date",
            "direction": "descending"
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
        try:
            name = r['properties']['name']['title'][0]['plain_text']
        except:
            continue
        try:
            course = r['properties']['course']['select']['name']
        except:
            course = ''
        try:
            admission_date = r['properties']['admission_date']['select']['name']
        except:
            admission_date = ''
        try:
            research_interests = [l['name']
                                  for l in r['properties']['research_interests']['multi_select']]
        except:
            research_interests = []
        try:
            email = r['properties']['email']['email'].replace("@", "'at'")
        except:
            email = ''
        links = ''
        try:
            temp = r['properties']['linked']['rich_text']
            for t in temp:
                links += t['plain_text']
            links = links.split("\n")
            link_title = []
            link_content = []
            for link in links:
                if " : " in link:
                    link_title.append(link)
                else:
                    link_content.append(link)
            linked = dict(zip(link_title, link_content))
        except:
            linked = {}
        try:
            pic = r['properties']['pic']['files'][0]['name']
        except:
            pic = ''

        data.append({
            'name': name,
            'course': course,
            'admission_date': admission_date,
            'research_interests': research_interests,
            'email': email,
            'linked': linked,
            'pic': pic
        })
    return {
        'statusCode': 200,
        'body': data
    }


def load_notionAPI_member_alumni():
    url = f"https://api.notion.com/v1/databases/{Member_Alumni_Database_ID}/query"
    filter = {  # 가져올 데이터 필터
        "or": [
                {
                    "property": "team",
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
            "property": "team",
            "direction": "descending"
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
        try:
            name = r['properties']['name']['title'][0]['plain_text']
        except:
            continue
        try:
            course = r['properties']['course']['select']['name']
        except:
            course = None
        team = r['properties']['team']['select']['name']
        graduate_year = r['properties']['graduate_year']['select']['name']
        project = r['properties']['project']['select']['name'] if r['properties']['project']['select'] else None
        data.append({
            'name': name,
            'course': course,
            'team': team,
            'graduate_year': graduate_year,
            'project': project
        })
    return {
        'statusCode': 200,
        'body': data
    }
