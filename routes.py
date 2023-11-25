from flask import Blueprint, render_template, request, session, jsonify, redirect, url_for
import hashlib
import user_agents  # Biblioteka do analizy informacji o urządzeniu użytkownika
from sqlalchemy.exc import IntegrityError
from PSO.ChartGenerator import ChartGenerator
from __init__ import db
from models import Users, LoginHistory
import matplotlib
matplotlib.use('Agg')  # Ustawienie backendu na 'Agg', który jest 'headless'



bp = Blueprint('main', __name__)


def is_user_logged_in():
    return session.get('logged_in', False)

@bp.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store'
    return response


@bp.route('/run_pso', methods=['POST'])
def run_pso():
    if not is_user_logged_in():
        return redirect(url_for('main.login'))
    data = request.json
    function_choice = data['function']

    chart_generator = ChartGenerator()

    if function_choice == 'rosenbrock':
        cost_function = chart_generator.rosenbrock_function
    elif function_choice == 'drop_wave':
        cost_function = chart_generator.drop_wave_function


    num_particles = int(data['num_particles'])
    maxiter = int(data['maxiter'])

    image_base64 = chart_generator.generuj_wykres(num_particles, maxiter, cost_function)

    return jsonify({'image': image_base64})


@bp.route('/')
def index():
    user_logged_in = session.get('logged_in', False)
    user_email = session.get('email', '')
    return render_template('index.html', user_logged_in=user_logged_in, user_email=user_email)



@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        try:
            new_user = Users(email=email, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            return jsonify({'success': True})

        except IntegrityError:
            db.session.rollback()
            return jsonify({'error': 'Użytkownik z takim adresem e-mail już istnieje.'}), 400

    return render_template('register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            return jsonify({'error': 'Brakujący e-mail lub hasło'}), 400

        user = Users.query.filter_by(email=email).first()
        if user and user.password == hashlib.sha256(password.encode()).hexdigest():
            session['logged_in'] = True
            session['email'] = email

            ip_address = request.remote_addr
            user_agent = user_agents.parse(request.headers.get('User-Agent'))
            device_info = f"{user_agent.browser.family} {user_agent.browser.version_string} / {user_agent.os.family} {user_agent.os.version_string} / {user_agent.device.family}"

            login_record = LoginHistory(email=email, ip_address=ip_address, device_info=device_info)
            db.session.add(login_record)
            db.session.commit()

            return jsonify({'success': True})


        return jsonify({'error': 'Nieprawidłowy e-mail lub hasło'}), 401

    return render_template('login.html')

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.index'))
