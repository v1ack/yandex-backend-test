from collections import Counter
from datetime import date
from sqlalchemy.orm import load_only

from app import db


class Citizen(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    citizen_id = db.Column(db.Integer)
    town = db.Column(db.String)
    street = db.Column(db.String)
    building = db.Column(db.String)
    appartement = db.Column(db.Integer)
    name = db.Column(db.String)
    birth_date = db.Column(db.Date)
    gender = db.Column(db.String)
    relatives = db.Column(db.ARRAY(db.Integer))
    import_id = db.Column(db.Integer)

    def __init__(self, citizen_id, town, street, building, appartement, name, birth_date, gender, relatives, import_id):
        self.citizen_id = citizen_id
        self.town = town
        self.street = street
        self.building = building
        self.appartement = appartement
        self.name = name
        day, month, year = map(int, birth_date.split('.'))
        self.birth_date = date(year, month, day)
        self.gender = gender
        self.relatives = relatives
        self.import_id = import_id

    def get_dict(self):
        return dict(citizen_id=self.citizen_id,
                    town=self.town,
                    street=self.street,
                    building=self.building,
                    appartement=self.appartement,
                    name=self.name,
                    birth_date=self.birth_date.strftime('%d.%m.%Y'),
                    gender=self.gender,
                    relatives=self.relatives)

    def birthdays_months(self):
        months = Counter()
        for relative_id in self.relatives:
            birthday = str(Citizen.query.filter_by(citizen_id=relative_id, import_id=self.import_id).options(
                load_only('birth_date')).first().birth_date.month)
            months[birthday] += 1
        return months

    def get_age(self, today=date.today()):
        years = today.year - self.birth_date.year
        if today.month < self.birth_date.month or \
                (today.month == self.birth_date.month and today.day < self.birth_date.day):
            years -= 1
        return years
