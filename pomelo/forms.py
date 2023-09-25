from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, TextAreaField
from wtforms.fields import TimeField, DateTimeField
from wtforms.widgets import TimeInput, DateInput
from wtforms.validators import DataRequired, Email, Length,InputRequired,Optional

class ReportTest1(FlaskForm):
    user = StringField('user', validators=[DataRequired()])
    usr_pass = StringField('usr_pass', validators=[DataRequired()])
    db_adress = StringField('db_adress', validators=[DataRequired()])
    db_login = StringField('db_login', validators=[DataRequired()])
    db_pass = StringField('db_pass', validators=[DataRequired()])
    db_name = StringField('db_name', validators=[DataRequired()])
    rp_descr = TextAreaField('rp_descr', validators=[DataRequired()])
    time_interval = TimeField('Выполнять каждые: ', validators=[Optional()], format='%H:%M', widget=TimeInput())
    tm_begin = TimeField('Начиная с: ', validators=[Optional()], format='%H:%M', widget=TimeInput())
    tm_end = TimeField('Заканчивая: ', validators=[Optional()], format='%H:%M', widget=TimeInput())
    dt_begin = DateTimeField('Начиная с: ', validators=[Optional()], format='%Y-%m-%d', widget=DateInput())
    dt_end = DateTimeField('Заканчивая: ', validators=[Optional()], format='%Y-%m-%d', widget=DateInput())
    create = SubmitField('Создать задачу')
    edit = SubmitField('Применить изменения')



