# RESTful Python API
### Использованные библиотеки
##### Встроенные
- datetime
- json
- math - для перцентилей
- random - для генерации случайных импортов
- collections.Counter - счетчик

##### Сторонние
- [flask](https://palletsprojects.com/p/flask/ "flask") - framework для веб-приложений
- [SQLAlchemy](https://www.sqlalchemy.org "SQLAlchemy") (flask_sqlalchemy) - ORM для СУБД, что позваляет обращаться к записям из БД как к объектам
- [psycopg2](https://pypi.org/project/psycopg2/ "psycopg2") - драйвер для PostgreSQL
- [redis](https://github.com/andymccurdy/redis-py "redis") - клиент redis для python
- [Gunicorn](https://gunicorn.org "Gunicorn") - сервер

### Программы
- [PostgreSQL](https://www.postgresql.org "PostgreSQL") СУБД
- [redis](https://redis.io "https://redis.io") - база данных "ключ-значение", оказалась намного более эффективным решением для хранения месяцев рождения, чем база данных (скорость выросла в 25 раз)

### Методы API
`POST /imports`
Принимает на вход набор с данными о жителях в формате json и сохраняет его с уникальным идентификатором.

`PATCH /imports/<int:import_id>/citizens/<int:citizen_id>`
Изменяет информацию о жителе в указанном наборе данных. На вход подается JSON в котором можно указать любые данные о жителе (name, gender, birth_date, relatives, town, street, building, appartement), кроме citizen_id.

`GET /imports/<int:import_id>/citizens`
Возвращает список всех жителей для указанного набора данных

`GET /imports/<int:import_id>/citizens/birthdays`
Возвращает жителей и количество подарков, которые они будут покупать своим ближайшим родственникам (1-го порядка), сгруппированных по месяцам из указанного набора данных

`GET /imports/<int:import_id>/towns/stat/percentile/age`
Возвращает статистику по городам для указанного набора данных в разрезе возраста жителей: p50, p75, p99, где число - это значение перцентиля

`GET /generate/<int:count>`
Генерация JSON для импорта

`GET /init`
Инициализация БД

`GET /make_citizens_dust`
Полное и необратимое удаление ~~всего и вся~~ бызы данных

### Установка и развертывание
Установка всех зависимостей

    sudo apt-get install python3-pip postgresql postgresql-contrib libpq-dev redis-server
    pip3 install flask flask_sqlalchemy psycopg2-binary gunicorn redis
    git clone https://github.com/v1ack/yandex-backend-test.git
Далее необходимо установить пароль для postgres и создать БД для тестов

    sudo -u postgres psql
    alter user postgres with encrypted password 'postgres';
    create database tests;
    \q

### Запуск сервера
В папке приложения

    gunicorn -b 0.0.0.0:8080 app:app
После первого запуска необходимо инициализировать БД `GET /init`

_Чтобы это все само работало мне понадобилось очень много времени_

В папке `/etc/systemd/system` надо создать `gunicorn.service` со следующим содержанием

    [Unit]
    Description=gunicorn daemon
    After=network.target
    
    [Service]
    User=entrant
    WorkingDirectory=/home/entrant/yandex-backend-test
    ExecStart=/home/entrant/.local/bin/gunicorn --bind 0.0.0.0:8080 app:app
    ExecReload=/bin/kill -s HUP $MAINPID
    ExecStop=/bin/kill -s TERM $MAINPID
    PrivateTmp=true
    
    [Install]
    WantedBy=multi-user.target
Дальше открываем консоль и заставляем всё это работать

    sudo systemctl enable gunicorn.service
    sudo systemctl start gunicorn.service

### Тесты
**tests.py** - тесты всех 5 API + тесты на нагрузку (убрать декораторы, чтобы запустить)