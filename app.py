import datetime

from flask import Flask, render_template, request, redirect, make_response, jsonify
from flask_login import login_user, LoginManager, login_required, logout_user, current_user

from data import db_session
from data.departments import Department
from data.jobs import Jobs
from data.users import User
from forms.add_department import AddDepartmentForm
from forms.add_job import AddJobForm
from forms.login import LoginForm
from forms.register import RegisterForm
from api import jobs_api
from api import users_api

from requests import get
from io import BytesIO
from PIL import Image

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
db_session.global_init("db/base.db")
app.register_blueprint(jobs_api.blueprint)
app.register_blueprint(users_api.blueprint)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route("/")
def index():
    session = db_session.create_session()
    jobs = session.query(Jobs).all()

    return render_template('list.html', jobs=jobs)


@app.route('/add_job', methods=['GET', 'POST'])
@login_required
def addjob():
    session = db_session.create_session()

    add_job_form = AddJobForm()
    if add_job_form.validate_on_submit():
        job = Jobs(
            team_leader_id=add_job_form.team_leader_id.data,
            job=add_job_form.job.data,
            work_size=add_job_form.work_size.data,
            collaborators=add_job_form.collaborators.data,
            is_finished=add_job_form.is_finished.data,
            start_date=datetime.datetime.now()
        )
        session.add(job)
        session.commit()

        return redirect("/")
    return render_template("add_job.html", form=add_job_form)


@app.route('/edit_job/<job_id>', methods=['GET', 'POST'])
@login_required
def edit_job(job_id):
    session = db_session.create_session()
    jobs = session.query(Jobs).all()
    add_job_form = AddJobForm()
    current_job = session.query(Jobs).filter(Jobs.id == int(job_id)).first()

    if current_user.id == 1 or current_user.id == current_job.team_leader_id:

        if add_job_form.validate_on_submit():
            current_job.team_leader_id = add_job_form.team_leader_id.data
            current_job.job = add_job_form.job.data
            current_job.work_size = add_job_form.work_size.data
            current_job.collaborators = add_job_form.collaborators.data
            current_job.is_finished = add_job_form.is_finished.data

            session.commit()

            return redirect("/")
        return render_template('edit_job.html', form=add_job_form, current_job=current_job)
    return render_template('list.html', jobs=jobs, message='Вы не имеете достаточно прав')


@app.route('/delete_job/<job_id>', methods=['GET', 'POST'])
@login_required
def delete_job(job_id):
    session = db_session.create_session()
    jobs = session.query(Jobs).all()
    current_job = session.query(Jobs).filter(Jobs.id == int(job_id)).first()

    if current_user.id == 1 or current_user.id == current_job.team_leader_id:
        session.delete(current_job)
        session.commit()
        return redirect("/")
    return render_template('list.html', jobs=jobs, message='Вы не имеете достаточно прав')


@app.route("/departments")
def departments_index():
    session = db_session.create_session()
    departments = session.query(Department).all()

    return render_template('department_list.html', departments=departments)


@app.route('/add_department', methods=['GET', 'POST'])
@login_required
def add_department():
    session = db_session.create_session()

    add_department_form = AddDepartmentForm()
    if add_department_form.validate_on_submit():
        department = Department(
            chief_id=add_department_form.team_leader_id.data,
            title=add_department_form.title.data,
            members=add_department_form.members.data,
            email=add_department_form.email.data
        )
        session.add(department)
        session.commit()

        return redirect("/departments")
    return render_template("add_department.html", form=add_department_form)


@app.route('/edit_department/<department_id>', methods=['GET', 'POST'])
@login_required
def edit_department(department_id):
    session = db_session.create_session()
    departments = session.query(Department).all()
    add_department_form = AddDepartmentForm()
    current_department = session.query(Department).filter(Department.id == int(department_id)).first()

    if current_user.id == 1 or current_user.id == current_department.chief_id:

        if add_department_form.validate_on_submit():
            current_department.chief_id = add_department_form.team_leader_id.data
            current_department.title = add_department_form.title.data
            current_department.members = add_department_form.members.data
            current_department.email = add_department_form.email.data

            session.commit()

            return redirect("/departments")
        return render_template('edit_department.html', form=add_department_form, current_department=current_department)
    return render_template('department_list.html', departments=departments, message='Вы не имеете достаточно прав')


@app.route('/delete_department/<department_id>', methods=['GET', 'POST'])
@login_required
def delete_department(department_id):
    session = db_session.create_session()
    departments = session.query(Department).all()
    current_department = session.query(Department).filter(Department.id == int(department_id)).first()

    if current_user.id == 1 or current_user.id == current_department.chief_id:
        session.delete(current_department)
        session.commit()
        return redirect("/departments")
    return render_template('department_list.html', departments=departments, message='Вы не имеете достаточно прав')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def get_form():
    session = db_session.create_session()
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            email=form.email.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data,
        )
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/login')

    return render_template('register.html', title='Регистрация', form=form)


@app.route('/users_show/<int:user_id>')
def users_show(user_id):
    user = get(f'http://127.0.0.1:5000/api/users/{user_id}').json()['user']
    print(user)
    user_name = user['name'] + ' ' + user['surname']

    toponym_to_find = user['hometown']
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": toponym_to_find,
        "format": "json"}

    response = get(geocoder_api_server, params=geocoder_params)

    if not response:
        # обработка ошибочной ситуации
        pass

    # Преобразуем ответ в json-объект
    json_response = response.json()
    # Получаем первый топоним из ответа геокодера.
    toponym = json_response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    # Координаты центра топонима:
    toponym_coodrinates = toponym["Point"]["pos"]
    # Долгота и широта:
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

    delta = "0.1"

    # Собираем параметры для запроса к StaticMapsAPI:
    map_params = {
        "ll": ",".join([toponym_longitude, toponym_lattitude]),
        "spn": ",".join([delta, delta]),
        "l": "map"
    }

    map_api_server = "http://static-maps.yandex.ru/1.x/"
    # ... и выполняем запрос
    response = get(map_api_server, params=map_params)
    with open('static/map.png', 'wb') as file:
        file.write(response.content)

    return render_template('nostalgy.html', user_name=user_name, hometown=toponym_to_find)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)
