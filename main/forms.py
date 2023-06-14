from flask_wtf import FlaskForm
from wtforms import IntegerField, BooleanField, PasswordField, SubmitField
from wtforms.validators import DataRequired

# prisijungimo forma
class LoginForm(FlaskForm):
    tabelioNr = IntegerField('Tabelio numeris', validators=[DataRequired()])
    slaptazodis = PasswordField('Slaptažodis', validators=[DataRequired()])
    prisiminti = BooleanField('Prisiminti mane')
    submit = SubmitField('Prisijungti')
# slaptazodzio keitimo forma
class NaujasSlaptazodisForma(FlaskForm):
    slapt1 = PasswordField('Naujas slaptažodis:', validators=[DataRequired()])
    slapt2 = PasswordField('Pakartoti slaptažodį', validators=[DataRequired()])
    keisti = SubmitField('Keisti')
