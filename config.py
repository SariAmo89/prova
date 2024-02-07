from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_property
import os
from datetime import datetime
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin
from flask_bootstrap import Bootstrap
from enum import Enum

class MsgCat(Enum):
    OK = "success"
    ERR = "danger"
    WARN = "warning"
    INFO = "info"

app = Flask(__name__, static_folder = '../static', template_folder='../templates') # Variable app mit Info vom Flask Proyekt

#Konfiguration der Datenbank
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #app nicht bei jeder Änderung an der DB informieren
db = SQLAlchemy(app)
migrate = Migrate(app, db)

#Konfiguration von Flask-Login
login = LoginManager(app)
login.login_view = 'login'
login.login_message = "Bitte melden Sie sich an, um diese Seite aufzurufen"
login.login_message_category = MsgCat.ERR.value

#Konfiguration von Flask-Bootstrap
bootstrap = Bootstrap(app)

#Konfiguration der Datei-Ablage
app.config['UPLOAD_FOLDER'] = os.path.join(app.static_folder, 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 8 * 1024 * 1024 #max. 8 MByte

#Konfiguration für CSRF-Protection (Security-feature; wird benötigt, sobald man per Browser Daten im Backend ändern möchte)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
csrf = CSRFProtect(app)
csrf.init_app(app)


#Zuordnung User zu User-Rollen
class UserRole(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey("role.id"), primary_key=True)

#Definition der User-Rollen
class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(40), nullable=False, unique=True)
    desc = db.Column(db.String(40), nullable=False)

    users = db.relationship("User", secondary="user_role", back_populates="roles")

#Definition der Model-Klassen
#-User
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    roles = db.relationship('Role', secondary='user_role', back_populates='users')
    pflanzen = db.relationship('Pflanze', backref='publisher', lazy='dynamic')
    
    @hybrid_property
    def is_admin(self):
        return self.has_role('admin')

    def __repr__(self):
        return '<User {}>'.format(self.username)
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    def has_role(self, role):
        return bool(
            Role.query
            .join(Role.users)
            .filter(User.id == self.id)
            .filter(Role.name == role)
            .count() == 1
        )

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

#-Pflanze
class Pflanze(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=True)
    wissenschaft_name = db.Column(db.String(40), nullable=True)
    familie = db.Column(db.String(40), nullable=True)
    vegetationszone = db.Column(db.String(40), nullable=True)
    will_sonne = db.Column(db.String(40), nullable=True)
    gefahr = db.Column(db.String(40), nullable=True)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))