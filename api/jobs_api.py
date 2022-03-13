import flask
from flask import jsonify, request

from data import db_session
from data.jobs import Jobs

blueprint = flask.Blueprint(
    'marsone_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/jobs')
def get_jobs():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return jsonify(
        {
            'jobs':
                [item.to_dict(only=('id',
                                    'team_leader_id',
                                    'job', 'work_size',
                                    'collaborators',
                                    'start_date',
                                    'end_date',
                                    'is_finished')
                              )
                 for item in jobs]
        }
    )


@blueprint.route('/api/jobs/<int:job_id>', methods=['GET'])
def get_one_job(job_id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).get(job_id)
    if not job:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'job': job.to_dict(only=('id',
                                     'team_leader_id',
                                     'job', 'work_size',
                                     'collaborators',
                                     'start_date',
                                     'end_date',
                                     'is_finished')
                               )
        }
    )


@blueprint.route('/api/jobs', methods=['POST'])
def create_job():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ["id", 'team_leader_id', 'job', 'work_size', 'collaborators', 'is_finished']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()

    if db_sess.query(Jobs).filter(Jobs.id == request.json["id"]).first() is not None:
        return jsonify({'error': 'Id already exists'})

    job = Jobs(
        id=request.json["id"],
        team_leader_id=request.json['team_leader_id'],
        job=request.json['job'],
        work_size=request.json['work_size'],
        collaborators=request.json['collaborators'],
        is_finished=request.json['is_finished']
    )
    db_sess.add(job)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).get(job_id)
    if not job:
        return jsonify({'error': 'Not found'})

    db_sess.delete(job)
    db_sess.commit()

    return jsonify(
        {
            'job': job.to_dict(only=('id',
                                     'team_leader_id',
                                     'job', 'work_size',
                                     'collaborators',
                                     'start_date',
                                     'end_date',
                                     'is_finished')
                               )
        }
    )


@blueprint.route('/api/jobs/<int:job_id>', methods=['PUT'])
def edit_job(job_id):
    if not request.json:
        return jsonify({'error': 'Empty request'})

    if not all(key in request.json for key in
                 ["id", 'team_leader_id', 'job', 'work_size', 'collaborators', 'is_finished']):
        return jsonify({'error': 'Bad request'})

    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).get(job_id)

    if not db_sess.query(Jobs).get(job_id):
        return jsonify({'error': f'There is no object with id {job_id}'})

    job.job = request.json['job']
    job.team_leader_id = request.json['team_leader_id']
    job.work_size = request.json['work_size']
    job.collaborators = request.json['collaborators']
    job.is_finished = request.json['is_finished']

    db_sess.commit()
    return jsonify({'success': 'OK'})