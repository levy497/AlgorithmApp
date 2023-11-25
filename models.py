from __init__ import db
from datetime import datetime

class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128))

    def __repr__(self):
        return f'<Users {self.email}>'

class LoginHistory(db.Model):
    __tablename__ = 'login_history'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    ip_address = db.Column(db.String(45))  # Długość dla IPv6
    login_time = db.Column(db.DateTime, default=datetime.utcnow)
    device_info = db.Column(db.String(255))  # Dostosuj długość w razie potrzeby

    def __repr__(self):
        return f'<LoginHistory {self.email}>'
