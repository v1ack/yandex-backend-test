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

похоже понадобятся еще библиотеки для запуска сервера...
и еще надо sqlite на нормальную СУБД заменить, а то чо как лох

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

`POST /init`
Инициализация БД

`GET /generate/<int:count>`
Генерация JSON для импорта

### Установка и развертывание
(понятия не имею, честно)

### Запуск сервера
В главной папке репозитория открыть командную строку и выполнить `flask run`
(Да-да, хреновый способ, годится только для разработки, потом переделаю)

### Тесты
**tests.py** - тесты все 5 API + тесты на нагрузку (убрать декораторы, чтобы запустить)