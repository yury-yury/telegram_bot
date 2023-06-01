The TodoList application 
provides opportunities to work with meetings, 
with goals and track progress on them.

python3.10, Django, Postgres

Как запустить:
    склонировать репозиторий (git clone git@github.com:yury-yury/todolist_lesson_33.git)
    создать виртуальное окружение (python3 -m venv venv)
    активировать виртуальное окружение(source venv/bin/activate)
    установить зависимости(pip install -r requirements.txt)
    создать и заполнить файл .env ( SECRET_KEY = 'django-insecure-*79sfgn-qssreox)n#+h&^cz5lo^0)v@+x2e0glv$4lp2r4wis'
                                    DEBUG = True
                                    DB_ENGINE=django.db.backends.postgresql
                                    DB_NAME=todolist
                                    DB_USER=postgres
                                    DB_PASSWORD=postgres
                                    DB_HOST=localhost
                                    DB_PORT=5434)
    выполнить миграции данных (./manager.py migrate)
    запустить сервер Django (./manager.py runserver)
    создать суперпользователя для приложения (./manager.py createsuperuser)
    перейти в браузере по адресу (http://127.0.0.1:8000/admin/)
    должна выйти панель администрирования Django
    ввести учетные данные суперпользователя
    проверить что у модели User существует запись с параметрами суперпользователя.
