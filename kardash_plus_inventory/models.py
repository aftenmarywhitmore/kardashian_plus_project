from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate 
import uuid 
from flask_marshmallow import Marshmallow
from werkzeug.security import generate_password_hash 
import secrets
from datetime import datetime
from flask_login import UserMixin, LoginManager

db = SQLAlchemy()
login_manager = LoginManager() 
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    first_name = db.Column(db.String(150), nullable = True, default = '') 
    last_name = db.Column(db.String(150), nullable = True, default = '') 
    email = db.Column(db.String(150), nullable = False) 
    password = db.Column(db.String, nullable = True, default = "")
    g_auth_verify = db.Column(db.Boolean, default = False)
    token = db.Column(db.String, default = "", unique = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    kardashian = db.relationship('Kardashian', backref='owner', lazy=True)

    def __init__(self, email, first_name = '', last_name = '', id = '', password = '', token = '', g_auth_verify = False):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token(24) 
        self.g_auth_verify = g_auth_verify 

    def set_token(self, length):
        return secrets.token_hex(length) 

    def set_id(self):
        return str(uuid.uuid4()) #creates a random id for us so we don't have to do it? Idk what this is...google later https://docs.python.org/3/library/uuid.html

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash 
        #what in the motherlickin frick is going on

    def __repr__(self):
        return f"User {self.email} has been added to the database!"


class Kardashian(db.Model):
    id = db.Column(db.String, primary_key = True)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    relationship_to_kardashians = db.Column(db.String(150))
    industry = db.Column(db.String(150))
    net_worth = db.Column(db.Numeric(precision=10, scale=2))
    age = db.Column(db.Numeric(precision=3, scale=2))
    birthday = db.Column(db.String(100))
    known_for = db.Column(db.String(100))
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    def __init__(self, first_name, last_name, relationship_to_kardashians, industry, net_worth, age, birthday, known_for, user_token, id = ''):
        self.id = self.set_id()
        self.first_name = first_name 
        self.last_name = last_name
        self.relationship_to_kardashians = relationship_to_kardashians
        self.industry = industry
        self.net_worth = net_worth
        self.age = age
        self.birthday = birthday
        self.known_for = known_for 
        self.user_token = user_token

    def __repr__(self):
        return f"The following Kardashian has been added: {self.first_name} {self.last_name}"

    def set_id(self):
        return secrets.token_urlsafe()

class KardashianSchema(ma.Schema):
    class Meta:
        fields = ['id', 'first_name', 'last_name', 'relationship_to_kardashians', 'industry', 'net_worth', 'age', 'birthday', 'known_for']


kardashian_schema = KardashianSchema()
kardashians_schema = KardashianSchema(many = True)
