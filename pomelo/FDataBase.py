import sqlite3
import math
import time
import pickle
from datetime import datetime as dt


class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def getLogPass(self, input_log):
        '''Получение логина и пароля из соответствующе таблицы БД для аутентификации пользователей'''
        sql = f'''SELECT _user, _pass FROM users WHERE _user = "{input_log}"'''
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res: return [dict(i) for i in res]
        except sqlite3.Error as e:
            print("Ошибка чтения из БД" + str(e))
        return []

    def fromReports(self):
        '''Получение всех наименований отчетов из соответствующе таблицы БД'''
        sql = '''SELECT * FROM reports'''
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            return res
        except sqlite3.Error as e:
            print("Ошибка чтения из БД " + str(e))
        return {}

    def addTask(self, task_name, report, report_name, configs, isactive, descript=None):
        '''Добавление задачи в соответствующую таблицу БД'''
        try:
            t_create = math.floor(time.time())# переменную отформатировать в строку и записать отдельным column в БД???
            self.__cur.execute("INSERT INTO actions VALUES(NULL,?,?,?,?,?,?,?,?)", (task_name,  report, report_name, t_create, dt.fromtimestamp(t_create).strftime("%d.%m.%Y, %H:%M:%S"), configs, isactive, descript))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления статьи в БД "+str(e))
            return False
        return True

    def addJob(self, task_name, warning_obj, output):
        try:
            t_create = math.floor(time.time())
            self.__cur.execute("INSERT INTO jobs VALUES(NULL,?,?,?,?)", (task_name, t_create, str(warning_obj), pickle.dumps(output)))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления статьи в БД "+str(e))
            return False
        return True

    def fromActions(self):
        '''Получение всех задач из соответствующей таблицы БД'''
        # наподумать: класс используется дважды для формирования списка АКТИВНЫХ и ВЫПОЛНЕННЫХ задач,
        # и в дальнейшем фильтруется в index.html . Необходимо ли сделать два класса, где первый будет
        # выгружать только активные задачи из таблицы БД, а второй только выполненные.
        sql = '''SELECT * FROM actions'''
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            return res
        except sqlite3.Error as e:
            print("Ошибка чтения из БД " + str(e))
        return {}

    def getConfigTest1(self, tsk_name):

        sql = f'''SELECT configs FROM actions WHERE task_name="{tsk_name}"'''
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            return res
        except sqlite3.Error as e:
            print("Ошибка чтения из БД" + str(e))
        return []

    def chekTaskName(self, tsk_name):
        '''Используется для проверки уникальности наименования новой создаваемой задачи перед добавлением в ДБ.'''
        sql = f'''SELECT task_name FROM actions WHERE task_name="{tsk_name}"'''
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            return res
        except sqlite3.Error as e:
            print("Ошибка чтения из БД" + str(e))
        return []

    def tableJobs(self):
        ''''''
        sql = '''SELECT id, task_name, job_time, warning_obj FROM jobs'''
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            return res
        except sqlite3.Error as e:
            print("Ошибка чтения из БД" + str(e))
        return []

    def getBLOB(self, id):
        ''''''
        sql = f'''SELECT output FROM jobs WHERE id="{id}"'''
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            return res
        except sqlite3.Error as e:
            print("Ошибка чтения из БД" + str(e))
        return []


    def deactiveJob(self, tsk_name):
        '''Деакцивация задачи для выполнения работы'''
        sql = f'UPDATE actions SET isActive = 0 WHERE task_name="{tsk_name}"'
        try:
            self.__cur.execute(sql)
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка чтения из БД" + str(e))
        return []