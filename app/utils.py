import math
import random


def generate_dict_for_json(count):
    cities = ['Москва', 'Санкт-Петербург', 'Новосибирск', 'Екатеринбург', 'Нижний Новгород', 'Казань']
    streets = 'список городов России включены все 1117 городов Российской Федерации указанием численности \
    населения по данным предварительных итогов Всероссийской переписи населения 2010 года также даты \
    их основания или первого упоминания исторических источниках Города федерального значения центры \
    столицы регионов выделены цветовой заливкой ячеек'.split()
    names = 'Авдей Аверкий Авксентий Агафон Александр Алексей Альберт Альвиан Анатолий Андрей Антон Антонин Анфим \
    Аристарх Аркадий Арсений Артём Артур Архипп Афанасий'.split()
    genders = ['male', 'female']

    def rand_day():
        rand = str(random.randint(1, 28))
        return rand if len(rand) - 1 else '0' + rand

    def rand_month():
        rand = str(random.randint(1, 12))
        return rand if len(rand) - 1 else '0' + rand

    return {"citizens": [{
        "citizen_id": i,
        "town": random.choice(cities),
        "street": random.choice(streets),
        "building": str(random.randint(1, 1000)),
        "appartement": random.randint(1, 1000),
        "name": random.choice(names),
        "birth_date": f'{rand_day()}.{rand_month()}.{random.randint(1970, 2018)}',
        "gender": random.choice(genders),
        "relatives": list(set([random.randint(0, count - 1) for _ in range(random.randint(0, 4))]))
    } for i in range(count)]}


def percentile(N, percent, key=lambda x: x):
    """
    Source: http://code.activestate.com/recipes/511478-finding-the-percentile-of-the-values/
    Find the percentile of a list of values.

    @parameter N - is a list of values. Note N MUST BE already sorted.
    @parameter percent - a float value from 0.0 to 1.0.
    @parameter key - optional key function to compute value from each element of N.

    @return - the percentile of the values
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
