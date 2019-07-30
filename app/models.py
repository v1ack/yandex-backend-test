import re
from collections import Counter
from datetime import date
import math
from sqlalchemy import event

from app import db, redis


class Citizen(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    citizen_id = db.Column(db.Integer)
    _town = db.Column(db.String, name='town')
    _street = db.Column(db.String, name='street')
    _building = db.Column(db.String, name='building')
    _appartement = db.Column(db.Integer, name='appartement')
    _name = db.Column(db.String, name='name')
    _birth_date = db.Column(db.Date, name='birth_date')
    _gender = db.Column(db.String, name='gender')
    _relatives = db.Column(db.ARRAY(db.Integer), name='relatives')
    import_id = db.Column(db.Integer)

    def __init__(self, citizen_id, town, street, building, appartement, name, birth_date, gender, relatives, import_id):
        self.citizen_id = citizen_id
        self.town = town
        self.street = street
        self.building = building
        self.appartement = appartement
        self.name = name
        self.birth_date = birth_date
        self.gender = gender
        self.relatives = relatives
        self.import_id = import_id

    @property
    def town(self):
        return self._town

    @town.setter
    def town(self, town):
        if re.search(r'[\w]+', town):
            self._town = town
        else:
            raise ValueError

    @property
    def street(self):
        return self._street

    @street.setter
    def street(self, street):
        if re.search(r'[\w\d]+', street):
            self._street = street
        else:
            raise ValueError

    @property
    def building(self):
        return self._building

    @building.setter
    def building(self, building):
        if re.search(r'[\w\d]+', building):
            self._building = building
        else:
            raise ValueError

    @property
    def appartement(self):
        return self._appartement

    @appartement.setter
    def appartement(self, appartement):
        if isinstance(appartement, int):
            self._appartement = appartement
        else:
            raise ValueError

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if re.search(r'\w+ \w+', name):
            self._name = name
        else:
            raise ValueError

    @property
    def gender(self):
        return self._gender

    @gender.setter
    def gender(self, gender):
        if re.match(r'^(male|female)$', gender):
            self._gender = gender
        else:
            raise ValueError

    @property
    def birth_date(self):
        return self._birth_date

    @birth_date.setter
    def birth_date(self, birth_date):
        if re.match(r'^(\d{2}[.]){2}\d{4}$', birth_date):
            self._birth_date = date(*map(int, reversed(birth_date.split('.'))))
        else:
            raise ValueError

    @property
    def relatives(self):
        return self._relatives

    @relatives.setter
    def relatives(self, relatives):
        if isinstance(relatives, list):
            self._relatives = relatives
        else:
            raise ValueError

    def del_birthday(self):
        redis.delete(f'{self.citizen_id}_{self.import_id}')

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
            birthday = redis.get(f'{relative_id}_{self.import_id}')
            months[birthday] += 1
        return months

    def get_age(self, today=date.today()):
        years = today.year - self.birth_date.year
        if today.month < self.birth_date.month or \
                (today.month == self.birth_date.month and today.day < self.birth_date.day):
            years -= 1
        return years


@event.listens_for(db.session, "before_flush")
def track_instances_before_flush(session, context, instances):
    modified_instances = session.info.setdefault("modified_instances", set())
    for obj in session.new:
        if isinstance(obj, Citizen):
            modified_instances.add(obj)
    for obj in session.dirty:
        if session.is_modified(obj) and isinstance(obj, Citizen):
            modified_instances.add(obj)


@event.listens_for(db.session, "before_commit")
def set_pending_changes_before_commit(session):
    session.flush()
    modified_instances = session.info.get("modified_instances", set())
    del session.info["modified_instances"]
    for obj in modified_instances:
        redis.set(f'{obj.citizen_id}_{obj.import_id}', obj._birth_date.month)


def percentile(N, percent, key=lambda x: x):
    """
    Source: http://code.activestate.com/recipes/511478-finding-the-percentile-of-the-values/
    Find the percentile of a list of values.

    :param list N: - is a list of values. Note N MUST BE already sorted.
    :param float percent: - a float value from 0.0 to 1.0.
    :param key - optional key function to compute value from each element of N.
    :return - the percentile of the values
    """
    if not N:
        return None
    k = (len(N) - 1) * percent
    f = math.floor(k)
    c = math.ceil(k)
    if f == c:
        return key(N[int(k)])
    d0 = key(N[int(f)]) * (c - k)
    d1 = key(N[int(c)]) * (k - f)
    return d0 + d1
