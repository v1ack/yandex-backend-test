import json
from collections import Counter
from datetime import date

from app import db


class Citizen(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    citizen_id = db.Column(db.String)
    town = db.Column(db.String)
    street = db.Column(db.String)
    building = db.Column(db.String)
    appartement = db.Column(db.String)
    name = db.Column(db.String)
    birth_date = db.Column(db.Date)
    gender = db.Column(db.String)
    relatives = db.Column(db.String)
    import_id = db.Column(db.Integer)

    def __init__(self, citizen_id, town, street, building, appartement, name, birth_date, gender, relatives, import_id):
        self.citizen_id = f'{citizen_id}_{import_id}'
        self.town = town
        self.street = street
        self.building = building
        self.appartement = appartement
        self.name = name
        day, month, year = map(int, birth_date.split('.'))
        self.birth_date = date(year, month, day)
        self.gender = gender
        self.relatives = json.dumps([f'{i}_{import_id}' for i in relatives])
        self.import_id = import_id

    def get_dict(self):
        return json.dumps(dict(citizen_id=self.get_id(),
                               town=self.town,
                               street=self.street,
                               building=self.building,
                               appartement=self.appartement,
                               name=self.name,
                               birth_date=self.birth_date.strftime('%d.%m.%Y'),
                               gender=self.gender,
                               relatives=[int(i.split('_')[0]) for i in json.loads(self.relatives)]))

    def birthdays_months(self):
        relatives = json.loads(self.relatives)
        months = Counter()
        for relative_id in relatives:
            birthday = str(Citizen.query.filter_by(citizen_id=relative_id).first().birth_date.month)
            months[birthday] += 1
        return months

    def get_id(self):
        return int(self.citizen_id.split('_')[0])

    def get_age(self, today=date.today()):
        # TODO Тут довольно странная фигня. Может быть неточно. Возможно стоит переделать...
        delta = today - self.birth_date
        return int(delta.days // 365.25)
