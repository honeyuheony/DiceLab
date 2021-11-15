## 🎲 Dice Lab

### DICELAB Introduce Page

한국기술교육대학교 컴퓨터공학부의 DICELAB의 연구 및 활동 현황을 소개하는 페이지입니다.

연구원들의 활동이 담긴 Notion DB를 주기적으로 Web Server와 동기화하여 최신연구동향을 보여줄 수 있도록 개발했습니다.  

# **⚙️ Development Environment**
|Part|Version|
|------|---|
|**WAS**|Python 3.8.5 + **Django** 3.0 + Redis + Bootstrap(with Django Templates)
|**Database**|**Sqlite3**
|**Notion API**|2021-08-16

[제목 없음](https://www.notion.so/268e3507701144f1ad4b7f39fec57f06)

# 📖 **Manual**

### **Django Web Server**

1. Git Clone
    
    `git clone https://github.com/honeyuheony/DiceLab.git`
    
2. 가상 환경 생성 및 종속 세팅
    
    `python -m venv [가상환경 명]`
    
    window : 
    
    `source [가상환경 명]/Scripts/activate` 
    
    mac : 
    
    `source [가상환경 명]/bin/activate`
    
    `pip install -r requirements.txt`
    
3. Migration
    
    `python manage.py createsuperuser "username"`
    
    `python manage.py makemigrations`
    
    `python manage.py migrate`
    
    `python manage.py runserver`
    

### Celery setting (with redis)

1. Run redis
    
    `redis-server`
    
2. Run Celery-Beat
    
    Start new Terminal and Set venv
    
    `python -m venv [가상환경 명]`
    window : 
    
    `celery -A [Project Name] -l info -B gevent`
    
    mac : 
    
    `celery -A [Project Name] worker -l info -B` 
    

<aside>
💡 1시간 간격으로 Notion DB와 Django server가 동기화 됩니다.

</aside>

# **✋ Part**

### Woo-yeol :

- Design model
- Design View at Course, Project, Publication, Seminar
- Design Templates at Main(header, footer), Member, Seminal
- Make search feature at Seminal

### honeyuheony :

- Notion API Background reload
- Design View at News, Professor, Member, School
- Design Templates at News, Professor, School, Project, Publication
