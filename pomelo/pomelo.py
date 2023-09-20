# lanshead import
import datetime
import pickle
import sqlite3
import os
import hashlib
import json

import flask
from flask_apscheduler import APScheduler
from sourcescript import compare_count_pos
from forms import ReportTest1
from FDataBase import FDataBase
from flask import Flask, render_template, request, flash, redirect, url_for, session, abort, g

# from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
# from obj_env.scheduler_configs import SchedulerConfigs

count_test2 = 0  # for test
DATABASE = '/tmp/flsk_website.db'
DEBUG = True
SECRET_KEY = 'aete%#@%aglaghlsdhl124215%#@%#gdlsgl'


# USERNAME = 'admin'
# PASSWORD = '123'
class SchedulerConfigs:  # на настоящий момент не работает с данными конфигурациями, настройка и добавление jobs осуществляется по средствам точечной нотации scheduler.___
    JOBS = [
        {
            "id": "scheduler_test1",
            "func": "pomelo:scheduler_test1",
            "args": ("pomelo",),
            "trigger": "interval",
            "seconds": 24 * 60 * 3600,
        }
    ]
    # SCHEDULER_JOBSTORES = {"default": SQLAlchemyJobStore(url="sqlite://")}
    # SCHEDULER_EXECUTORS = {"default": {"type": "threadpool", "max_workers": 20}}
    SCHEDULER_ALLOWED_HOSTS = ['*']
    # SCHEDULER_API_ENABLED = True


app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'flsk_website.db')))


# функция для исполнения шедулером
def scheduler_test1(test1):
    print('LALALA', test1)


def scheduler_test2():
    # добавить джоб при добавлении задачи на сайте и проверить дальнейшее её выполнение.
    global count_test2
    count_test2 += 1
    print(f'Шедулером выполнена #{count_test2} заглушка компарекоунтпос в {datetime.datetime.now()}')


def create_job_compare_count_pos(tsk_name):
    with app.app_context():
        db = get_db()
        dbase = FDataBase(db)
        config = json.loads(dbase.getConfigTest1(tsk_name)[0]['configs'])
        job = compare_count_pos.compare_positions(user=config['user'],
                                                  usr_pass=config['usr_pass'],
                                                  db_address=config['db_adress'],
                                                  db_login=config['db_login'],
                                                  db_pass=config['db_pass'],
                                                  db_name=config['db_name'])
        dbase.addJob(tsk_name, job[0], job[1])
    print(f'Я шедулер, я лупанул компарекоунт в {datetime.datetime.now()}, результат смотри в таблице БД jobs')


# забираем конфиг задания из БД
def config_rep_test1(tsk_name):
    db = get_db()
    dbase = FDataBase(db)
    return json.loads(dbase.getConfigTest1(tsk_name)[0][0])


# >>>Навигация по сайту
@app.route('/')
def index():
    if 'userLogged' not in session:
        return render_template('login.html', h1='Авторизация')
    db = get_db()
    dbase = FDataBase(db)
    actions = dbase.fromActions()
    configs = {}
    for task in actions:
        configs[f'{task[1]}'] = json.loads(task[6])
    return render_template('index.html', h1='Задачи', actions=actions, configs=configs)

@app.route('/table_jobs', methods=["POST", "GET"])
def table_jobs():
    if 'userLogged' not in session:
        return render_template('login.html', h1='Авторизация')
    db = get_db()
    dbase = FDataBase(db)
    jobs = dbase.tableJobs()
    return render_template('table_jobs.html', h1='TABLE JOBS', jobs=jobs)



@app.route('/upload/<id>')
def upload(id):
    db = get_db()
    dbase = pickle.loads(FDataBase(db).getBLOB(id)[0]['output'])
    filename = f'uploads/CCP_id={id}_{datetime.datetime.now().strftime("%m_%d_%Y_%H_%M_%S")}.txt'
    with open(filename, 'w', encoding='utf-8') as f:
        [f.write(str(temp)) for temp in dbase]
        f.close()
    return flask.send_file(filename, as_attachment=True)



@app.route('/login', methods=["POST", "GET"])
def login():
    if 'userLogged' in session:
        return redirect(url_for('profile', username=session['userLogged']))
    elif request.method == 'POST':
        db = get_db()  # коннект к базе
        dbase = FDataBase(db).getLogPass(
            request.form['username'])  # получение из базы значения пользователя и его хеш-пароля в виде [dict()]
        if dbase:  # eсли dbase нашла пользователя
            if hashlib.scrypt(request.form['pass'].encode(), salt='mysalt'.encode(), n=8, r=512, p=4, dklen=32).hex() == \
                    dbase[0]['_pass']:  # хешируем введенный пароль и сравниваем тем хешем, который есть взят из базы
                session['userLogged'] = request.form[
                    'username']  # заполняем значение сессии о том, что пользователь авторизован
                return redirect(url_for('index', username=session[
                    'userLogged']))  # перенаправляем пользователя на страницу профиля
            flash('Ошибка ввода логина и/или пароля', category='error')
        else:
            flash('Ошибка ввода логина и/или пароля', category='error')
    return render_template('login.html', h1='Авторизация')  # возвращаем страницу авторизации.


@app.route("/add_task", methods=["POST", "GET"])
def addTask():
    '''Рендерит страницу для указания наименования и выбора отчета. При нажатии кнопки "Далее" редиректит на
    страницу соответствующую отчета для заполнения дополнительных параметров'''
    if 'userLogged' not in session:
        abort(401)
    db = get_db()
    dbase = FDataBase(db)
    if request.method == "POST":
        if not dbase.chekTaskName(request.form['task_name']) and len(request.form['task_name']) > 4 and request.form['report_name'] == 'test1':
            session['task_name'] = request.form['task_name']  # сохраняем в сессии имя отчета
            return redirect(url_for('report_for_test1'))
        else:
            flash('Ошибка добавления статьи', category='error')
    return render_template('add_task.html', h1='Добавить задачу', reports=dbase.fromReports())


@app.route('/report_for_test1', methods=['GET', 'POST'])
def report_for_test1():
    '''Заполнение данных для конкретного отчета.'''
    if 'userLogged' not in session:
        abort(401)

    db = get_db()
    dbase = FDataBase(db)
    form = ReportTest1()
    if form.validate_on_submit():
        configs = {'user': request.form['user'],
                   'usr_pass': request.form['usr_pass'],
                   'db_adress': request.form['db_adress'],
                   'db_login': request.form['db_login'],
                   'db_pass': request.form['db_pass'],
                   'db_name': request.form['db_name'],
                   'time_interval': request.form['time_interval'],
                   'tm_begin': request.form['tm_begin'],
                   'dt_begin': request.form['dt_begin'],
                   'tm_end': request.form['tm_end'],
                   'dt_end': request.form['dt_end']
                   }
        dbase.addTask(session['task_name'], 'test1', 'compare_count_pos.py', json.dumps(configs), isactive=1,
                      descript=request.form['rp_descr'])
        # готовим данные для cron из формы
        hour_interval, minute_interval = configs['time_interval'].split(':')
        hour_begin, minute_begin = configs['tm_begin'].split(':')
        year_begin, month_begin, day_begin = configs['dt_begin'].split('-')
        hour_end, minute_end = configs['tm_end'].split(':')
        year_end, month_end, day_end = configs['dt_end'].split('-')

        if int(hour_interval) == 0:
            for_hour_cron = f'{hour_begin}-{hour_end}'
        else:
            for_hour_cron = f'{hour_begin}-{hour_end}/{hour_interval}'
        if int(minute_interval) == 0:
            for_minute_cron = f'{minute_begin}-{minute_end}'
        else:
            for_minute_cron = f'{minute_begin}-{minute_end}/{minute_interval}'
        # добавляем job из формы
        task_name = session['task_name']
        scheduler.add_job(id=f'job_{session["task_name"]}', func=create_job_compare_count_pos,
                          args=(task_name,),
                          trigger='cron',
                          year=f'{year_begin}-{year_end}',
                          month=f'{month_begin}-{month_end}',
                          day=f'{day_begin}-{day_end}',
                          hour=for_hour_cron,
                          minute=for_minute_cron)
        print(scheduler.get_jobs())
        return redirect(url_for('index'))
    # print(form.validate_on_submit(), request.form['time_interval'], request.form['tm_begin'], request.form['dt_begin'], request.form['tm_end'], request.form['dt_end'], sep='\n')
    return render_template('report_for_test1.html', h1='Задача для test1', form=form)


@app.route('/test1', methods=['GET', 'POST'])
def create_now():
    if 'userLogged' not in session:
        abort(401)
    db = get_db()
    dbase = FDataBase(db)
    tsk_name = [v for v in request.args.values()][0]
    config = json.loads(dbase.getConfigTest1(tsk_name)[0]['configs'])
    job = compare_count_pos.compare_positions(user=config['user'],
                                              usr_pass=config['usr_pass'],
                                              db_address=config['db_adress'],
                                              db_login=config['db_login'],
                                              db_pass=config['db_pass'],
                                              db_name=config['db_name'])
    dbase.addJob(tsk_name, job[0], job[1])
    return render_template('job_output.html', h1='Задача выполнена', output=job[1])


@app.route('/jobs', methods=["POST", "GET"])
def jobs():
    if 'userLogged' not in session:
        abort(401)
    if request.method == 'POST':
        scheduler.delete_job(request.form['id'])
        db = connect_db()
        dbase = FDataBase(db)
        dbase.deactiveJob(request.form['id'])

    j = scheduler.get_jobs()
    return render_template('jobs.html', h1='Действующие задания', jobs= j)


@app.route("/profile/<username>")
def profile(username):
    if 'userLogged' not in session or session['userLogged'] != username:
        abort(401)
    db = get_db()
    dbase = FDataBase(db)
    return render_template('index.html', h1='Задачи', actions=dbase.fromActions())


@app.route("/logout")
def logout():
    if 'userLogged' in session:
        session.clear()
    abort(401)


# >>>Взаимодействие с БД
def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


def create_db():
    '''function for create DB'''
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


def get_db():
    '''connect to DB, if it is not installed'''
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


@app.teardown_appcontext
def close_db(error):
    '''close DB, if it is installed'''
    if hasattr(g, 'link_db'):
        g.link_db.close()


# >>>Обработки ошибок
@app.errorhandler(404)
def pageNotFound(error):
    return render_template('page404.html', h1='Страница не найдена'), 404


@app.errorhandler(401)
def pageNotAutorized(error):
    return render_template('page401.html', h1='Вы не авторизованы'), 401


if __name__ == '__main__':
    app.config.from_object(SchedulerConfigs)
    scheduler = APScheduler()
    scheduler.add_job(id='no_web_test1', func=scheduler_test1, args=('ARRR',), trigger='cron', day="*")
    scheduler.init_app(app)
    scheduler.start()
    app.run(
        debug=True)  # use_reloader позволяет выполнить задачу без дублей ( при необходимости см. описание параметра)

