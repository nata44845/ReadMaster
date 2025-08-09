from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect
db = SQLAlchemy()


def repr(self):
    mapper = inspect(self).mapper
    ent = []
    for col in mapper.column_attrs:
        ent.append("{0}={1}".format(col.key, getattr(self, col.key)))
    return "<{0}(".format(self.__class__.__name__) + ", ".join(ent) + ")>"


db.Model.__repr__ = repr


class AuthLog(db.Model):
    __tablename__ = 'auth_log'

    id = db.Column(db.Integer, primary_key=True)
    time_in = db.Column(db.DateTime, nullable=True,
                        server_default=db.FetchedValue())
    login = db.Column(db.String(32), nullable=False)

    def __init__(self, login=None):
        self.login = login

class Client(db.Model):
    __tablename__ = 'clients'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Enum('Потенциальный', 'Рабочий'), nullable=True)
    city = db.Column(db.String(32), nullable=True)
    segment = db.Column(db.String(32), nullable=True)
    company_name = db.Column(db.String(255), nullable=False)
    site = db.Column(db.String(64), nullable=True)
    email = db.Column(db.String(64), nullable=True)
    comments = db.Column(db.Text, nullable=True)
    create_date = db.Column(db.DateTime, nullable=True)
    last_update = db.Column(db.DateTime, nullable=True)
    loyalty = db.Column(db.Enum('Лояльный', 'Нелояльный'), nullable=True)
    activity = db.Column(db.String(64), nullable=True)

    def __init__(self, user_id=None, status=None, city=None, segment=None,
                 company_name=None, site=None, email=None, comments=None,
                 create_date=None, last_update=None, loyalty=None,
                 activity=None):
        self.user_id = user_id
        self.status = status
        self.city = city
        self.segment = segment
        self.company_name = company_name
        self.site = site
        self.email = email
        self.comments = comments
        self.loyalty = loyalty
        self.activity = activity

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(32), nullable=False)
    passw = db.Column(db.String(32), nullable=False)
    exten = db.Column(db.Integer, nullable=True)
    prefix = db.Column(db.String(2), nullable=True)
    role = db.Column(db.Enum('manager', 'ruk', 'boss'), nullable=False)
    ruk_id = db.Column(db.Integer, nullable=True)
    name = db.Column(db.String(64), nullable=True)

    def __init__(self, login=None, passw=None, exten=None, prefix=None,
                 role=None, ruk_id=None, name=None):
        self.login = login
        self.passw = passw
        self.exten = exten
        self.prefix = prefix
        self.role = role
        self.ruk_id = ruk_id
        self.name = name

    def check_exist(login, exten):
        if exten:
            # OR c помощью |
            return User.query.filter(
                (User.login == login) | (User.exten == exten)).first()

        else:
            return User.query.filter_by(login=login).first()
