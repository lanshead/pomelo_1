import datetime
import time
from pymssql import connect
import requests
from obj_env.obj_classes import PositionComp
import time
from datetime import timedelta, datetime


def get_now_date():  # функция определения текущего времени и времени
    pattern = '%Y-%m-%dT21:00:00.000'  # паттерн для скуль запроса
    curtime = time.localtime()  # текущее время
    day1 = datetime(curtime.tm_year, curtime.tm_mon, curtime.tm_mday)  # формирование дататайма текущего дня
    return (day1 - timedelta(days=2)).strftime(pattern), (day1 - timedelta(days=1)).strftime(pattern), int(
        (day1 - timedelta(days=1)).timestamp())  # кортеж дататаймов текущего дня и предыдущего


def get_session_key(url, p):
    return requests.get(url, params=p).text  # функция получения ключа сессии



    # параметры необходимые для работы скрипта
def compare_positions(user='CCT',usr_pass='200318', db_address='10.10.4.4', db_login='sa', db_pass='qwEr12#4', db_name='dozor_2023_07_29'):
    database_connection = [db_address, db_login, db_pass, db_name]  # параметры коннекта к базе данных
    # системные параметры
    login_url = 'http://stat.navsvc.ru:7000/mon/login?'
    objects_url = 'http://stat.navsvc.ru:7000/mon/objects?'
    stat_url = 'http://stat.navsvc.ru:7000/mon/stat?'
    param_objects = {'server': 'hmao', 'user': user, 'password': usr_pass}
    date_for_query = get_now_date()
    session_key = get_session_key(login_url, param_objects)  # запрос ключа сессии

    for_work = eval(requests.get(objects_url, params={'session': session_key, 'params': '100,10002'}).text) #запрос объектов на сервисе статистики

    dict_of_instanse = {} #создание пустого словаря (ключ - objid, значение - экземпляр класса)
    for code, *oth, parameters in for_work:
        p = dict(parameters)
        if 10002 in p and int(p[10002]) > time.time() - 86400: #если время последней позиции есть в наборе данных и это время больше чем сегодняшнее число - 1 день.
            dict_of_instanse[int(code)] = PositionComp(int(code), p[100])

    #набор параметров к реквесту за статистикой
    params_for_stat = {'session': session_key,
                       'identity': 'name:[' + ','.join(map(lambda c: str(c.name), dict_of_instanse.values())) + ']',
                       'time': date_for_query[2], 'interval': '86400', 'params': '9001', 'options': '1'}
    for_work = []
    for_work = eval(requests.get(stat_url, params=params_for_stat).text) #запрос количества позиций на сервисе статистики
    for code, *oth, parameters in for_work:
        p = dict(parameters)
        if 9001 in p and code in dict_of_instanse: #если параметр есть в словаре и код объекта есть в словаре с классами(исключаем одинаковые имена из группового запроса к сервису статистики)
            dict_of_instanse[int(code)].add_stat_pos(p[9001])

    #запрос количества позиций по каждому из объектов из базы данных
    connection = connect(*database_connection)
    cursor = connection.cursor()
    for inst in dict_of_instanse.keys():
        cursor.execute(
            f"SELECT COUNT(*) from MONPOS where objid={inst} and gmt between '{date_for_query[0]}' and '{date_for_query[1]}'")  # этот шайтан выдает объект. Если его распаковать то внутри будет список кортеж.
        dict_of_instanse[inst].add_sql_pos(tuple(*cursor)[0])
    connection.close()
    warning_obj = [obj for obj in dict_of_instanse.values() if obj.eq_pos > 0]
    output = (sorted(warning_obj, key=lambda o: o.eq_pos), f'{len(warning_obj)} из {len(dict_of_instanse)}')
    return warning_obj, output
