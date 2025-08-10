from flask import Flask, render_template, g, session, request, redirect, \
    url_for, flash
import os.path
from flask_bootstrap import Bootstrap
from forms import FormAddAdmin, FormAddUser
from logging.handlers import RotatingFileHandler
from logging import Formatter
import logging
import time
from sqlalchemy.sql.expression import func
from sqlalchemy.sql import text
from datetime import timedelta
from models import db, User, AuthLog
from datetime import datetime

app = Flask(__name__)

# -----------------------------------------------------------------------------
# config.DevelopmentConfig или config.ProductionConfig
# -----------------------------------------------------------------------------

app.config.from_object('config.ProductionConfig')
app.jinja_env.trim_blocks = True  # Очищает пустые строки
app.jinja_env.lstrip_blocks = True  # Очищает пробелы
app.jinja_env.add_extension('jinja2.ext.loopcontrols')  # range, continue в тпл
db.init_app(app)
bootstrap = Bootstrap(app)
app.permanent_session_lifetime = timedelta(days=3650)

# -----------------------------------------------------------------------------
# Включение, отключение и ротация логов.
# -----------------------------------------------------------------------------

handler = RotatingFileHandler(app.config['LOGFILE'],
                              maxBytes=1000000, backupCount=1)
handler.setLevel(logging.DEBUG)
handler.setFormatter(Formatter('%(asctime)s %(levelname)s: %(message)s '
                               '[in %(pathname)s:%(lineno)d]'))
# logging.disable(logging.CRITICAL)  # Расскоментарь это для прекращения логов
app.logger.addHandler(handler)


# -----------------------------------------------------------------------------
# Хуки и Функции
# -----------------------------------------------------------------------------


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.before_request
def before_request():
    g.date_today = time.strftime('%Y%m%d')
    session.permanent = True
    g.user_id = session.get('user_name', None)
    g.role = session.get('role', None)
    g.start = time.time()
    if ('user_name' not in session and request.endpoint != 'login'
            and not request.path.startswith('/static/')):
        return redirect(url_for('login'))

    if g.user_id:
        if not g.user_id.isdigit() and '/crm/' in request.path:
            flash('CRM только для менеджеров!', 'danger')
            return redirect(request.referrer)  # Возвращаем  откуда он пришел
        if g.role != 'boss' and '/boss/' in request.path:
            return redirect(request.referrer)


@app.after_request
def add_header(response):
    """Запрещаяем всяческое кеширование из-за IE и json и модальных окон"""
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.teardown_request
def teardown_request(exception=None):
    diff = time.time() - g.start
    if '_ajax' not in request.path:
        app.logger.debug('Время загрузки: %s => %s', request.path, diff)


# -----------------------------------------------------------------------------
#  Роуты общие для всех
# -----------------------------------------------------------------------------

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():  # Авторизация
    if request.method == 'POST':
        f = request.form
        row = User.query.filter_by(login=f['usern'], passw=f['passw']).first()
        if row:

            me = AuthLog(row.login)  # Пишем в базу время входа юзера
            db.session.add(me)
            db.session.commit()

            session['role'] = row.role
            if row.role == 'boss':
                session['user_name'] = row.login
                return redirect(url_for('area_boss_index'))
            if row.role == 'ruk':
                session['user_name'] = row.login
                return redirect(url_for('area'))
            if row.role == 'manager':
                session['user_name'] = str(row.exten)
                return redirect(url_for('area_crm'))
        else:
            return redirect(url_for('login'))
    return render_template("login.html")


@app.route('/logout/')
def logout():
    session.pop('user_name', None)
    session.pop('role', None)
    return redirect(url_for('login'))

# -----------------------------------------------------------------------------
# Роуты Админ
# -----------------------------------------------------------------------------

@app.route('/admin/')
def area_boss_index():  # Главная страница босса
    rows = User.query.order_by(User.login).all()
    return render_template('boss_index.html', rows=rows)


@app.route('/area/boss/add/new/ruk/', methods=['GET', 'POST'])
def area_boss_add_new_ruk():  # Добавление нового рука
    form = FormAddRuk()
    if request.method == 'POST' and form.validate_on_submit():
        if User.check_exist(form.login.data, None):
            flash('Ошибка! Юзер с таким логином уже существует!', 'danger')
        else:
            me = User(form.login.data, form.passw.data, None, None, 'ruk', None,
                      form.name.data)
            db.session.add(me)
            db.session.commit()
            flash('Руководитель успешно создан!', 'success')
            return redirect(url_for('area_boss_index'))

    return render_template('boss_add_ruk.html', form=form)


@app.route('/area/boss/add/new/manager/', methods=['GET', 'POST'])
def area_boss_add_new_manager():  # Добавление нового менеджера
    form = FormAddManager()
    # Динамически формируем список руков из базы
    form.ruk_id.choices = [(str(a.id), a.login) for a in User.query.filter_by(
        role='ruk').order_by(User.login).all()]
    form.ruk_id.choices.insert(0, ("", "Выберите руководителя"))

    if request.method == 'POST' and form.validate_on_submit():
        if User.check_exist(form.login.data, form.exten.data):
            flash('Ошибка! Такой логин или внтр. номер существует!', 'danger')
        else:
            me = User(form.login.data, form.passw.data, form.exten.data,
                      form.prefix.data, 'manager', form.ruk_id.data,
                      form.name.data)
            db.session.add(me)
            db.session.commit()
            flash('Менеджер успешно создан!', 'success')
            return redirect(url_for('area_boss_index'))

    return render_template('boss_add_manager.html', form=form)


@app.route('/area/boss/del/user/<int:_id_>/')
def area_boss_del_user(_id_):  # Удаление любых типов юзеров
    User.query.filter(User.id == _id_).delete()
    db.session.commit()
    flash('Юзер успешно удален!', 'info')
    return redirect(url_for('area_boss_index'))


@app.route('/area/boss/edit/ruk/<int:_id_>/', methods=['GET', 'POST'])
def area_boss_edit_ruk(_id_):  # В модальном окне редактируем менеджера
    form = FormAddRuk()
    if request.method == 'POST' and form.validate_on_submit():
        User.query.filter_by(id=_id_).update(
            {'passw': form.passw.data, 'name': form.name.data})
        db.session.commit()
        flash('Изменения приняты!', 'success')
        return redirect(url_for('area_boss_index'))

    obj = User.query.filter_by(id=_id_).first()
    form = FormAddRuk(obj=obj)
    return render_template("boss_edit_ruk.html", form=form, _id_=str(_id_))


@app.route('/area/boss/edit/manager/<int:_id_>/', methods=['GET', 'POST'])
def area_boss_edit_manager(_id_):  # В модальном окне редактируем менеджера
    if request.method == 'POST':
        f = request.form
        User.query.filter_by(id=_id_).update({'passw': f['passw'],
                                              'name': f['name'],
                                              'prefix': f['prefix'],
                                              'ruk_id': f['ruk_id']})
        db.session.commit()
        flash('Изменения приняты!', 'success')
        return redirect(url_for('area_boss_index'))

    obj = User.query.filter_by(id=_id_).first()
    form = FormAddManager(obj=obj)
    # Динамически формируем список менеджеров из базы
    form.ruk_id.choices = [(str(a.id), a.login) for a in User.query.filter_by(
        role='ruk').order_by(User.login).all()]
    form.ruk_id.choices.insert(0, ("", "Выберите руководителя"))
    return render_template("boss_edit_manager.html", form=form, _id_=str(_id_))


# -----------------------------------------------------------------------------
# Crm
# -----------------------------------------------------------------------------

@app.route('/crm/')
def area_crm():
    return render_template("crm_index.html")

@app.route('/help/')
def area_help():
    return render_template("area_help.html")


if __name__ == "__main__":
        # app.debug = True
        app.run(host='0.0.0.0')
