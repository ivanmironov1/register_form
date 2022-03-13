from data import db_session
from data.users import User

db_session.global_init("../db/base.db")
session = db_session.create_session()

user = User()
user.surname = "Kiril"
user.name = "Petrov"
user.age = 90
user.position = "middle"
user.hometown = 'Чемошур'
user.speciality = "research engineer"
user.address = "module_2"
user.email = "petrov@mars.org"
user.set_password('qwerty123')
session.add(user)
session.commit()
