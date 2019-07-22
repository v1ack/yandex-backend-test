from app import *
from app.models import Citizen
from app.utils import generate_dict_for_json
import unittest
from random import randint
from flask import json


class UnitTest(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/tests'
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_index(self):
        response = self.app.get('/')
        assert response.data == b'seems to be working, lol'
        assert response.status_code == 200

    def test_imports(self):
        random_json = json.dumps(generate_dict_for_json(10))
        random_json2 = json.dumps(generate_dict_for_json(100))
        response = self.app.post('/imports', content_type='application/json', data=random_json)
        assert response.get_json()['data']['import_id'] == 1
        assert response.status_code == 201
        response = self.app.post('/imports', content_type='application/json', data=random_json2)
        assert response.get_json()['data']['import_id'] == 2
        assert response.status_code == 201

    def test_get_import(self):
        random_json = json.dumps(generate_dict_for_json(20))
        self.app.post('/imports', content_type='application/json', data=random_json)
        response = self.app.get('/imports/1/citizens')
        assert sorted(response.get_json()['data'], key=lambda x: x['citizen_id']) == sorted(
            json.loads(random_json)['citizens'], key=lambda x: x['citizen_id'])

    def test_patch(self):
        random_json = json.dumps(generate_dict_for_json(20))
        self.app.post('/imports', content_type='application/json', data=random_json)
        citizen_id = randint(1, 10)
        self.app.patch(f'/imports/1/citizens/{citizen_id}', content_type='application/json',
                       data='{"town":"Керчь","street":"Иосифа Бродского"}')
        citizen = Citizen.query.filter_by(citizen_id=citizen_id, import_id=1).one()
        assert citizen.town == 'Керчь'
        assert citizen.street == 'Иосифа Бродского'

    def test_birthdays(self):
        random_dict = generate_dict_for_json(10)
        dates = ['06.02.1984',
                 '06.11.2012',
                 '01.06.1972',
                 '12.12.1996',
                 '18.04.1982',
                 '15.02.1993',
                 '01.09.2005',
                 '27.10.2002',
                 '21.08.1984',
                 '24.02.2016']
        relatives = [[7],
                     [0, 3, 5],
                     [],
                     [0, 9],
                     [1],
                     [],
                     [0, 9, 2],
                     [0, 6],
                     [9, 4],
                     []]
        for i in range(10):
            random_dict['citizens'][i].update({'birth_date': dates[i], 'relatives': relatives[i]})
        self.app.post('/imports', content_type='application/json', data=json.dumps(random_dict))
        response = self.app.get('/imports/1/citizens/birthdays').get_json()['data']
        assert response['1'] == []
        assert response['7'] == []
        assert response['4'][0]['citizen_id'] == 8
        assert response['12'][0]['presents'] == 1
        # assert response.get_json() == json.loads(right)

    def test_stat(self):
        random_dict = generate_dict_for_json(10)
        dates = ['06.02.1984',
                 '06.11.2012',
                 '01.06.1972',
                 '12.12.1996',
                 '18.04.1982',
                 '15.02.1993',
                 '01.09.2005',
                 '27.10.2002',
                 '21.08.1984',
                 '24.02.2016']
        cities = ['Москва'] * 5 + ['Санкт-Петербург'] * 5
        for i in range(10):
            random_dict['citizens'][i].update({'birth_date': dates[i], 'town': cities[i]})
        right = '{"data":[{"p50":35,"p75":37,"p99":46.6,"town":"\u041c\u043e\u0441\u043a\u0432\u0430"},{"p50":16,' \
                '"p75":26,"p99":33.68,"town":"\u0421\u0430\u043d\u043a\u0442-\u041f\u0435\u0442\u0435\u0440\u0431' \
                '\u0443\u0440\u0433"}]}'
        self.app.post('/imports', content_type='application/json', data=json.dumps(random_dict))
        response = self.app.get('/imports/1/towns/stat/percentile/age')
        assert response.get_json() == json.loads(right)

    @unittest.skip
    def test_import_10000(self):
        random_json = json.dumps(generate_dict_for_json(10000))
        response = self.app.post('/imports', content_type='application/json', data=random_json)
        assert response.get_json()['data']['import_id'] == 1
        assert response.status_code == 201

    @unittest.skip
    def test_output_10000(self):
        random_json = json.dumps(generate_dict_for_json(10000))
        self.app.post('/imports', content_type='application/json', data=random_json)
        response = self.app.get('/imports/1/citizens')
        assert response.status_code == 200
        assert sorted(response.get_json()['data'], key=lambda x: x['citizen_id']) == sorted(
            json.loads(random_json)['citizens'], key=lambda x: x['citizen_id'])

    @unittest.skip
    def test_birthdays_10000(self):
        random_json = json.dumps(generate_dict_for_json(10000))
        self.app.post('/imports', content_type='application/json', data=random_json)
        response = self.app.get('/imports/1/citizens/birthdays')
        assert response.status_code == 200

    @unittest.skip
    def test_stat_10000(self):
        random_json = json.dumps(generate_dict_for_json(10000))
        self.app.post('/imports', content_type='application/json', data=random_json)
        response = self.app.get('/imports/1/towns/stat/percentile/age')
        assert response.status_code == 200


if __name__ == '__main__':
    unittest.main()
