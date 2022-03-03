from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, IntegerField, BooleanField, EmailField
from wtforms.validators import DataRequired


class AddDepartmentForm(FlaskForm):
    title = StringField('Название департамента', validators=[DataRequired()])
    team_leader_id = IntegerField('Руководитель работ', validators=[DataRequired()])
    members = StringField('Участники', validators=[DataRequired()])
    email = EmailField('Почта департамента', validators=[DataRequired()])

    submit = SubmitField('Добавить')
