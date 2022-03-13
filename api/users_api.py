import flask
from flask import jsonify, request

from data import db_session
from data.users import User

blueprint = flask.Blueprint(
    'marsone_user_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/users')
def get_users():
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    return jsonify(
        {
            'users':
                [item.to_dict(only=(
                    'id', 'name', 'surname',
                    'age', 'position',
                    'speciality', 'address',
                    'email', 'hashed_password',
                    'modified_date', 'hometown')
                )
                    for item in users]
        }
    )


@blueprint.route('/api/users/<int:user_id>', methods=['GET'])
def get_one_job(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    print(user)
    if not user:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'user': user.to_dict(only=(
                'id', 'name', 'surname',
                'age', 'position',
                'speciality', 'address',
                'email', 'hashed_password',
                'modified_date', 'hometown')
            )
        }
    )


@blueprint.route('/api/users', methods=['POST'])
def create_job():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['id', 'name', 'surname',
                  'age', 'position',
                  'speciality', 'address',
                  'email', 'hashed_password',
                  'modified_date', 'hometown']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()

    if db_sess.query(User).filter(User.id == request.json["id"]).first() is not None:
        return jsonify({'error': 'Id already exists'})

    user = User(
        id=request.json['id'],
        name=request.json['name'],
        surname=request.json['surname'],
        age=request.json['age'],
        position=request.json['position'],
        speciality=request.json['speciality'],
        address=request.json['address'],
        hometown=request.json['hometown'],
        email=request.json['email'],
        modified_date=request.json['modified_date']
    )
    user.set_password(request.json['hashed_password'])
    db_sess.add(user)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_job(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'Not found'})

    db_sess.delete(user)
    db_sess.commit()

    return jsonify(
        {
            'user': user.to_dict(only=(
                'id', 'name', 'surname',
                'age', 'position',
                'speciality', 'address',
                'email', 'hashed_password',
                'modified_date', 'hometown')
                                 )
        }
    )


@blueprint.route('/api/jobs/<int:user_id>', methods=['PUT'])
def edit_job(user_id):
    if not request.json:
        return jsonify({'error': 'Empty request'})

    if not all(key in request.json for key in
               ['id', 'name', 'surname',
                'age', 'position',
                'speciality', 'address',
                'email', 'hashed_password',
                'modified_date', 'hometown']):

        return jsonify({'error': 'Bad request'})

    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)

    if not db_sess.query(User).get(user_id):
        return jsonify({'error': f'There is no object with id {user_id}'})

    user.id = request.json['id'],
    user.name = request.json['name'],
    user.surname = request.json['surname'],
    user.age = request.json['age'],
    user.position = request.json['position'],
    user.speciality = request.json['speciality'],
    user.address = request.json['address'],
    user.email = request.json['email'],
    user.hometown = request.json['hometown'],
    user.modified_date = request.json['modified_date']
    user.set_password(request.json['hashed_password'])

    db_sess.commit()
    return jsonify({'success': 'OK'})
