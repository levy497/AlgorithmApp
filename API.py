from functools import wraps

from flask import Blueprint, request, jsonify
import hashlib
import jwt
import datetime
import os
from PSO.ChartGenerator import ChartGenerator
from models import Users, LoginHistory
from __init__ import db
import user_agents  # Biblioteka do analizy informacji o urządzeniu użytkownika

api_bp = Blueprint('api', __name__)
SECRET_KEY = os.environ.get('SECRET_KEY') or 'tajny_domyślny_klucz' # Zastąp to bezpiecznym, tajnym kluczem

def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Brak dostępu: brak tokena'}), 403

        try:
            jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except:
            return jsonify({'error': 'Nieprawidłowy token'}), 401

        return f(*args, **kwargs)
    return decorated_function


@api_bp.route('/api/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Brakujący e-mail lub hasło'}), 400

    user = Users.query.filter_by(email=email).first()
    if user and user.password == hashlib.sha256(password.encode()).hexdigest():
        # Generowanie tokena JWT
        token = jwt.encode({
            'email': user.email,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, SECRET_KEY, algorithm="HS256")

        ip_address = request.remote_addr
        user_agent = user_agents.parse(request.headers.get('User-Agent'))
        device_info = f"{user_agent.browser.family} {user_agent.browser.version_string} / {user_agent.os.family} {user_agent.os.version_string} / {user_agent.device.family}"

        login_record = LoginHistory(email=email, ip_address=ip_address, device_info=device_info)
        db.session.add(login_record)
        db.session.commit()

        return jsonify({'success': True, 'token': token})
    else:
        return jsonify({'error': 'Nieprawidłowy e-mail lub hasło'}), 401

@api_bp.route('/api/run_pso', methods=['POST'])
@token_required
def run_pso():
    data = request.json
    function_choice = data['function']
    num_particles = int(data['num_particles'])
    maxiter = int(data['maxiter'])

    chart_generator = ChartGenerator()

    if function_choice == 'rosenbrock':
        cost_function = chart_generator.rosenbrock_function
    elif function_choice == 'drop_wave':
        cost_function = chart_generator.drop_wave_function
    else:
        return jsonify({'error': 'Nieprawidłowa funkcja'}), 400

    image_base64 = chart_generator.generuj_wykres(num_particles, maxiter, cost_function)
    return jsonify({'image': image_base64})