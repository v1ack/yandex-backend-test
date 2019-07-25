from flask import request, jsonify, abort
from sqlalchemy.orm import load_only
from app import app, db, redis
from app.models import Citizen
from datetime import date
from app.utils import *
import re
from sqlalchemy.orm.exc import NoResultFound


@app.route('/', methods=['GET', 'POST'])
def index():
    return 'seems to be working, lol'


@app.route('/imports', methods=['POST'])
def imports():
    # Принимает на вход набор с данными о жителях в формате json и сохраняет его с уникальным идентификатором.
    if not request.json or 'citizens' not in request.json:
        abort(400)
    citizens_count = Citizen.query.count()
    import_id = Citizen.query.filter_by(id=citizens_count - 1).options(
        load_only("import_id")).one().import_id + 1 if citizens_count else 1
    for citizen in request.json['citizens']:
        if isinstance(citizen['citizen_id'], int) and \
                re.match(r'^\w{2,}', citizen['town']) and \
                re.match(r'^\w{2,}', citizen['street']) and \
                re.match(r'^(\w|\d)', citizen['building']) and \
                isinstance(citizen['appartement'], int) and \
                re.match(r'^\w{2,}', citizen['name']) and \
                re.match(r'^(\d{2}[.]){2}\d{4}$', citizen['birth_date']) and \
                re.match(r'^(male|female)$', citizen['gender']):
            db.session.add(Citizen(citizen_id=citizen["citizen_id"],
                                   town=citizen['town'],
                                   street=citizen['street'],
                                   building=citizen['building'],
                                   appartement=citizen['appartement'],
                                   name=citizen['name'],
                                   birth_date=citizen['birth_date'],
                                   gender=citizen['gender'],
                                   relatives=citizen['relatives'],
                                   import_id=import_id))
        else:
            db.session.rollback()
            abort(400)
    db.session.commit()
    return jsonify({'data': {'import_id': import_id}}), 201


@app.route('/imports/<int:import_id>/citizens/<int:citizen_id>', methods=['PATCH'])
def edit_info(import_id, citizen_id):
    # Изменяет информацию о жителе в указанном наборе данных.
    # На вход подается JSON в котором можно указать любые данные о
    # жителе (name, gender, birth_date, relatives, town, street,
    # building, appartement), кроме citizen_id .
    if not request.json:
        abort(400)
    try:
        citizen = Citizen.query.filter_by(citizen_id=citizen_id, import_id=import_id).one()
    except NoResultFound:
        abort(400)
    try:
        if 'town' in request.json:
            if re.match(r'^\w{2,}', request.json['town']):
                citizen.town = request.json['town']
            else:
                raise ValueError
        if 'street' in request.json:
            if re.match(r'^\w{2,}', request.json['street']):
                citizen.street = request.json['street']
            else:
                raise ValueError
        if 'building' in request.json:
            if re.match(r'^(\w|\d)', request.json['building']):
                citizen.building = request.json['building']
            else:
                raise ValueError
        if 'appartement' in request.json:
            if isinstance(request.json['appartement'], int):
                citizen.appartement = request.json['appartement']
            else:
                raise ValueError
        if 'name' in request.json:
            if re.match(r'^\w{2,}', request.json['name']):
                citizen.name = request.json['name']
            else:
                raise ValueError
        if 'birth_date' in request.json:
            if re.match(r'^(\d{2}[.]){2}\d{4}$', request.json['birth_date']):
                day, month, year = map(int, request.json['birth_date'].split('.'))
                citizen.birth_date = date(year, month, day)
                redis.set(f'{citizen_id}_{import_id}', month)
            else:
                raise ValueError
        if 'gender' in request.json:
            if re.match(r'^(male|female)$', request.json['gender']):
                citizen.gender = request.json['gender']
            else:
                raise ValueError
        if 'relatives' in request.json:
            citizen.relatives = request.json['relatives']
    except ValueError:
        db.session.rollback()
        abort(400)
    db.session.commit()
    return jsonify(citizen.get_dict()), 200


@app.route('/imports/<int:import_id>/citizens', methods=['GET'])
def get_info(import_id):
    # Возвращает список всех жителей для указанного набора данных
    citizens = Citizen.query.filter_by(import_id=import_id)
    if not citizens.count():
        abort(400)
    return jsonify({'data': [i.get_dict() for i in citizens]}), 200


@app.route('/imports/<int:import_id>/citizens/birthdays', methods=['GET'])
def birthdays(import_id):
    # Возвращает жителей и количество подарков, которые они будут покупать своим
    # ближайшим родственникам (1-го порядка), сгруппированных по месяцам из
    # указанного набора данных.
    citizens = Citizen.query.filter_by(import_id=import_id)
    count = citizens.count()
    if not count:
        abort(400)
    months = {f'{i}': [] for i in range(1, 13)}
    for citizen in citizens:
        birthdays_months = citizen.birthdays_months()
        for k, v in birthdays_months.items():
            months[k].append({"citizen_id": citizen.citizen_id, "presents": v})
    return jsonify({"data": months}), 200


@app.route('/imports/<int:import_id>/towns/stat/percentile/age', methods=['GET'])
def statistic(import_id):
    # Возвращает статистику по городам для указанного набора данных в разрезе
    # возраста жителей: p50, p75, p99, где число - это значение перцентиля
    citizens = Citizen.query.filter_by(import_id=import_id)
    if not citizens.count():
        abort(400)
    cities = {}
    today = date.today()
    for citizen in citizens:
        cities[citizen.town] = cities.get(citizen.town, []) + [citizen.get_age(today)]
    cities = {city: sorted(ages) for city, ages in cities.items()}
    data = [{"town": city,
             "p50": percentile(ages, 0.5),
             "p75": percentile(ages, 0.75),
             "p99": percentile(ages, 0.99)} for city, ages in cities.items()]
    return jsonify({'data': data}), 200


@app.route('/init', methods=['GET'])
def init_db():
    # Инициализация БД, например после удаления
    db.create_all()
    return 'done'


@app.route('/make_citizens_dust', methods=['GET'])
def delete_all():
    # Удаление базы, полное и необратимое
    db.drop_all()
    redis.flushdb()
    return 'done, lol'


@app.route('/generate/<int:count>', methods=['GET'])
def generate(count):
    # Генерация JSON для импорта
    return jsonify(generate_dict_for_json(count))
