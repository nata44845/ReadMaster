from flask_wtf import FlaskForm as Form
from wtforms import StringField, SubmitField, SelectField, IntegerField, \
    TextAreaField, DateField, HiddenField
from wtforms.validators import DataRequired,  URL
from wtforms import validators

class FormAddLogin(Form):
    login = StringField(
        'Логин', render_kw={
            "pattern": "[a-zA-Z0-9-]+",
            "placeholder": 'Для логина подходят цифры или латинские буквы'},
        validators=[DataRequired()])
    passw = StringField('Пароль', validators=[DataRequired()])
    name = StringField('Имя', render_kw={"placeholder": "Например, Иван Котов"})


class FormAddAdmin(FormAddLogin):
    submit = SubmitField('Сохранить')


class FormAddUser(FormAddLogin):
    admin = SelectField('Администратор', validators=[DataRequired()])
    submit = SubmitField('Сохранить')
