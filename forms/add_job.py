from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, IntegerField, BooleanField
from wtforms.validators import DataRequired


class AddJobForm(FlaskForm):
    job = StringField('Название работы', validators=[DataRequired()])
    team_leader_id = IntegerField('Руководитель работ', validators=[DataRequired()])
    work_size = IntegerField('Объем работ', validators=[DataRequired()])
    collaborators = StringField('Участники', validators=[DataRequired()])
    is_finished = BooleanField('Работа завершена')

    submit = SubmitField('Добавит')
