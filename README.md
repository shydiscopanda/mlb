## Second Tetration

Simple Django app to calculate the second tetration of any number between -100 000 & 100 000

---
### Quick Start

Run *(will be available at http://localhost:8000/)*

    docker-compose up
    
    
Create Admin user

    docker exec -it << container id >> bash
    
    python manage.py createsuperuser 

--- 

#### Useful Links 

app admin *(requires admin user login)*

http://localhost:8000/admin/


view workers  

http://localhost:8000/django-rq/

