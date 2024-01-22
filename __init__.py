from datetime import timedelta

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

import pymysql
from API import api_bp

db = SQLAlchemy()
pymysql.install_as_MySQLdb()

def create_app():

    app = Flask(__name__)
    app.register_blueprint(api_bp)

    # Konfiguracja aplikacji
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'tajny_domyślny_klucz'
    db_username = os.environ.get('DB_USERNAME')
    db_password = os.environ.get('DB_PASSWORD')
    db_name = os.environ.get('DB_NAME')
    db_host = os.environ.get('DB_HOST')  # lub inny host, jeśli baza danych jest zdalna
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{db_username}:{db_password}@{db_host}/{db_name}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SESSION_PERMANENT'] = False


    # Inicjalizacja SQLAlchemy
    db.init_app(app)

    # Rejestracja Blueprintów
    from routes import bp as main_bp
    app.register_blueprint(main_bp)

    # Inne konfiguracje, jeśli są potrzebne

    return app
