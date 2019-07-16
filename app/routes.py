from flask import request, jsonify, abort
from app import app, db
from app.models import Citizen
from datetime import date
from app.utils import *


@app.route('/', methods=['GET', 'POST'])
def index():
    return 'seems to be working, lol'


@app.route('/imports', methods=['POST'])
def imports():
    # Принимает на вход набор с данными о жителях в формате json и сохраняет его с уникальным идентификатором.
    if not request.json or 'citizens' not in request.json:
        abort(400)
    citizens_count = Citizen.query.count()
    import_id = Citizen.query.filter_by(id=citizens_count - 1).one().import_id + 1 if citizens_count else 1
    for citizen in request.json['citizens']:
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
    citizen = Citizen.query.filter_by(citizen_id=f'{citizen_id}_{import_id}').first()
    if 'town' in request.json:
        citizen.town = request.json['town']
    if 'street' in request.json:
        citizen.street = request.json['street']
    if 'building' in request.json:
        citizen.building = request.json['building']
    if 'appartement' in request.json:
        citizen.appartement = request.json['appartement']
    if 'name' in request.json:
        citizen.name = request.json['name']
    if 'birth_date' in request.json:
        citizen.birth_date = request.json['birth_date']
    if 'gender' in request.json:
        citizen.gender = request.json['gender']
    if 'relatives' in request.json:
        citizen.relatives = json.dumps(request.json['relatives'])
    return jsonify(citizen.get_dict()), 200


@app.route('/imports/<int:import_id>/citizens', methods=['GET'])
def get_info(import_id):
    # Возвращает список всех жителей для указанного набора данных
    citizens = Citizen.query.filter_by(import_id=import_id)
    return jsonify({'data': [i.get_dict() for i in citizens]}), 200


@app.route('/imports/<int:import_id>/citizens/birthdays', methods=['GET'])
def birthdays(import_id):
    # Возвращает жителей и количество подарков, которые они будут покупать своим
    # ближайшим родственникам (1-го порядка), сгруппированных по месяцам из
    # указанного набора данных.
    citizens = Citizen.query.filter_by(import_id=import_id)
    months = {f'{i}': [] for i in range(1, 13)}
    for citizen in citizens:
        birthdays_months = citizen.birthdays_months()
        for k, v in birthdays_months.items():
            months[k].append({"citizen_id": citizen.get_id(), "presents": v})
    return jsonify({"data": months}), 200


@app.route('/imports/<int:import_id>/towns/stat/percentile/age', methods=['GET'])
def statistic(import_id):
    # Возвращает статистику по городам для указанного набора данных в разрезе
    # возраста жителей: p50, p75, p99, где число - это значение перцентиля
    citizens = Citizen.query.filter_by(import_id=import_id)
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


@app.route('/generate/<int:count>', methods=['GET'])
def generate(count):
    # Генерация JSON для импорта
    return generate_json(count)
