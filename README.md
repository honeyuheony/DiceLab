# 🎲**DICE LAB - HomePage**
**[Link](https://www.dicelab.kr)** 2021-08-04 ~ 2022-01-29 

### DICELAB Introduce Page

한국기술교육대학교 컴퓨터공학부의 DICELAB의 연구 및 활동 현황을 소개하는 페이지입니다.
연구원들의 활동이 담긴 Notion DB 데이터를 신속하게 전달하기 위해
Notion DB 데이터를 Web Server와 주기적으로 동기화하는 비동기 큐 작업을 구현하여
최신연구동향을 1시간마다 갱신해 제공할 수 있도록 개발했습니다.

# **✋ Part**

### [Woo-yeol](https://github.com/Woo-yeal)

- Design model
- Design View at Course, Project, Publication, Seminar
- Design Templates at Main(header, footer), Member, Seminal
- Make search feature at Seminal

### [honeyuheony](https://github.com/honeyuheony)

- Synchronize database with Notion api
- Design View at News, Professor, Member, School
- Design Templates at News, Professor, School, Project, Publication

# 🖥 Project Example
<div align="center"><img src="./DiceLab.gif" width='800px'></div>

# **⚙️ Development Environment**

<h2 align="center">📚 Tech Stack </h2>
<p align="center">
  <img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54"/></a>&nbsp 
 <img src="https://img.shields.io/badge/django-092E20?style=for-the-badge&logo=django&logoColor=white"></a>&nbsp   
<br>
  <img src="https://img.shields.io/badge/bootstrap-%23563D7C.svg?style=for-the-badge&logo=bootstrap&logoColor=white"></a>&nbsp  
  <img src="https://img.shields.io/badge/html5-E34F26?style=for-the-badge&logo=html5&logoColor=white"></a>&nbsp  
  <img src="https://img.shields.io/badge/css-1572B6?style=for-the-badge&logo=css3&logoColor=white"></a>&nbsp
  <img src="https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E"/></a>&nbsp
  <img src="https://img.shields.io/badge/jquery-0769AD?style=for-the-badge&logo=jquery&logoColor=white"></a>&nbsp 
  <br>
  <img src="https://img.shields.io/badge/amazonaws-232F3E?style=for-the-badge&logo=amazonaws&logoColor=white"></a>&nbsp
  <img src="https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white"></a>&nbsp
  <img src="https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white"></a>&nbsp
  <img src="https://img.shields.io/badge/AWS-%23FF9900.svg?style=for-the-badge&logo=amazon-aws&logoColor=white"></a>&nbsp
  <br>
  <img src="https://img.shields.io/badge/Notion-%23000000.svg?style=for-the-badge&logo=notion&logoColor=white"></a>&nbsp
  <img src="https://img.shields.io/badge/github-181717?style=for-the-badge&logo=github&logoColor=white"></a>&nbsp
  <img src="https://img.shields.io/badge/github-181717?style=for-the-badge&logo=github&logoColor=white"></a>&nbsp
  <img src="https://img.shields.io/badge/git-F05032?style=for-the-badge&logo=git&logoColor=white"></a>&nbsp
 </p>

|Part|Version|
|------|---|
|**Front-End**|Django Templates + Bootstrap
|**Back-End**|Back : Python 3.8.5 + Django 3.0 + Redis  
|**Database**|Sqlite3
|**Notion API**|Version : 2021-08-16
|**Distribution**|AWS-LightSail

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
