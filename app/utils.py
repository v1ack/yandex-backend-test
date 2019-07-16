import json
import random


def generate_json(count):
    cities = ['Москва', 'Санкт-Петербург', 'Новосибирск', 'Екатеринбург', 'Нижний Новгород', 'Казань']
    streets = 'В список городов России включены все 1117 городов Российской Федерации с указанием численности \
    населения по данным предварительных итогов Всероссийской переписи населения 2010 года а также даты \
    их основания или первого упоминания в исторических источниках Города федерального значения и центры \
    столицы регионов выделены цветовой заливкой ячеек'.split()
    genders = ['male', 'female']
    return json.dumps({"citizens": [{
        "citizen_id": i,
        "town": random.choice(cities),
        "street": random.choice(streets),
        "building": str(random.randint(1, 1000)),
        "appartement": str(random.randint(1, 1000)),
        "name": "Иванов Иван Иванович",
        "birth_date": f'{random.randint(1, 28)}.{random.randint(1, 12)}.{random.randint(1970, 2018)}',
        "gender": random.choice(genders),
        "relatives": list(set([random.randint(1, 10) for _ in range(random.randint(0, 4))]))
    } for i in range(count)]})
