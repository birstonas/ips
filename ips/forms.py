from flask_wtf import FlaskForm
from wtforms import SubmitField, DateTimeField, IntegerField, SelectField
from wtforms.validators import DataRequired

# IPS puslapyje esanti datos forma -  Nuo Iki 
class Datos(FlaskForm):
    tabelioNr = IntegerField('Tabelio numeris', validators=[DataRequired()])
    updates = SelectField('Diena:', choices = [(1, 'Labas')], validators=[DataRequired()])
    pradzia = DateTimeField('Laiko pradžia', format='%H:%M', validators=[DataRequired()])
    pabaiga = DateTimeField('Laiko pabaiga', format='%H:%M', validators=[DataRequired()])
    rodyti = SubmitField('Rodyti')
