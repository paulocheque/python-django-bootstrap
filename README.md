{{ project_name }}
=======================

    pip install django==1.7

    mkdir {{ project_name }} ; django-admin.py startproject --template https://github.com/paulocheque/python-django-bootstrap/zipball/master --extension py,md,rst --name app_menu.html,index.html,Rakefile,Procfile {{ project_name }} {{ project_name }} --verbosity 3

    virtualenv env -p python2.7
    source env/bin/activate
    pip install -r requirements.txt
    pip install -r requirements-dev.txt
    python manage.py migrate
    python manage.py createsuperuser
    python manage.py runserver
    open http://localhost:8000

    sudo python manage.py runserver 0.0.0.0:80


Accout templates:
-------------------


https://github.com/paulocheque/django-allauth/tree/master/allauth/templates