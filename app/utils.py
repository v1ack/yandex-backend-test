import random


def generate_dict_for_json(count, error_line=-1, relations_count=None):
    """
    Генерация словаря для импорта
    :param int count: количество людей
    :param int error_line: строка с ошибкой
    :param int relations_count: количество отношений
    :return: словарь
    """
    if relations_count is None:
        relations_count = random.randint(count // 2, count * 4)
    cities = ['Москва', 'Санкт-Петербург', 'Новосибирск', 'Екатеринбург', 'Нижний Новгород', 'Казань']
    streets = 'список городов России включены все 1117 городов Российской Федерации указанием численности \
    населения по данным предварительных итогов Всероссийской переписи населения 2010 года также даты \
    их основания или первого упоминания исторических источниках Города федерального значения центры \
    столицы регионов выделены цветовой заливкой ячеек'.split()
    names = 'Авдей Аверкий Авксентий Агафон Александр Алексей Альберт Альвиан Анатолий Андрей Антон Антонин Анфим \
    Аристарх Аркадий Арсений Артём Артур Архипп Афанасий'.split()
    surnames = 'КАБАКОВ КАБАНЕЦ КАБАНОВ КАБАНОВИЧ КАБАНЬКОВ КАБИН КАБИЦКИЙ КАБЛУКОВ КАВЕЛИН КАВЕРЗИН КАВЕРЗНЕВ КАВЕРИН \
    КАВЕРНЫЙ КАВРАЙСКИЙ КАГАН КАГАНЕР КАГАНОВ КАГАНОВИЧ КАГАНОВСКИЙ КАГАНСКИЙ КАГАНЦЕВ КАДАШОВ КАДИГРОБ КАДИМОВ КАДКИН \
    КАДНИКОВ КАДОМСКИЙ КАДОМЦЕВ КАДОЧНИКОВ КАДУЛИН КАДЫГРОБ КАДЫКОВ КАДЫРОВ КАДЫШЕВ КАЕКИН КАЕХТИН КАЗАК'.split()
    genders = ['male', 'female']

    def rand_day():
        rand = str(random.randint(1, 28))
        return rand if len(rand) - 1 else '0' + rand

    def rand_month():
        rand = str(random.randint(1, 12))
        return rand if len(rand) - 1 else '0' + rand

    citizens = [{
        "citizen_id": i,
        "town": random.choice(cities),
        "street": random.choice(streets),
        "building": str(random.randint(1, 1000)),
        "appartement": random.randint(1, 1000) if error_line != i else 'error-is-here',
        "name": f'{random.choice(names)} {random.choice(surnames)}',
        "birth_date": f'{rand_day()}.{rand_month()}.{random.randint(1970, 2018)}',
        "gender": random.choice(genders),
        "relatives": []
    } for i in range(count)]
    for _ in range(relations_count):
        a, b = random.randint(0, count - 1), random.randint(0, count - 1)
        if a not in citizens[b]['relatives'] and b != citizens[a]['citizen_id']:
            citizens[a]['relatives'].append(b)
            citizens[b]['relatives'].append(a)
    return {"citizens": citizens}
