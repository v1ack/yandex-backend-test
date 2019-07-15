import json
from collections import Counter

from app import db


class Citizen(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    citizen_id = db.Column(db.String)
    town = db.Column(db.String)
    street = db.Column(db.String)
    building = db.Column(db.String)
    appartement = db.Column(db.String)
    name = db.Column(db.String)
    birth_date = db.Column(db.String)
    gender = db.Column(db.String)
    relatives = db.Column(db.String)
    import_id = db.Column(db.Integer)

    def get_dict(self):
        return json.dumps(dict(citizen_id=self.get_id(),
                               town=self.town,
                               street=self.street,
                               building=self.building,
                               appartement=self.appartement,
                               name=self.name,
                               birth_date=self.birth_date,
                               gender=self.gender,
                               relatives=[int(i.split('_')[0]) for i in json.loads(self.relatives)]))

    def birthdays_months(self):
        relatives = json.loads(self.relatives)
        months = Counter()
        for relative_id in relatives:
            birthday = Citizen.query.filter_by(citizen_id=relative_id).first().birth_date.split('.')[1]
            if birthday[0] == '0':
                birthday = birthday[1:]
            months[birthday] += 1
        return months

    def get_id(self):
        return int(self.citizen_id.split('_')[0])
