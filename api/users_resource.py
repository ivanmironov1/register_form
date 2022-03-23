from flask import jsonify
from flask_restful import Resource, abort

from api.users_validator import parser
from data import db_session
from data.users import User


def get_users_or_abort(user_id):
    session = db_session.create_session()
    users = session.query(User).get(user_id)
    if not users:
        abort(404, message=f"User {user_id} not found")

    return users


class UsersResource(Resource):
    def get(self, user_id):
        users = get_users_or_abort(user_id)
        return jsonify({'user': users.to_dict(
            only=('name', 'surname', 'age', 'address', 'email', 'position', 'speciality', 'hashed_password'))})

    def delete(self, user_id):
        session = db_session.create_session()
        users = get_users_or_abort(user_id)
        session.delete(users)
        session.commit()
        return jsonify({'success': 'OK'})


class UsersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify({'users': [item.to_dict(
            only=('id', 'name', 'surname', 'age', 'address', 'email', 'position', 'speciality', 'hashed_password')) for item in users]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        user = User(
            name=args['name'],
            surname=args['surname'],
            age=args['age'],
            position=args['position'],
            speciality=args['speciality'],
            address=args['address'],
            email=args['email'],
        )
        user.set_password(args['hashed_password'])
        session.add(user)
        session.commit()
        return jsonify({'success': 'OK'})
