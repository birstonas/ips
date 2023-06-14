from flask import redirect, request
from datetime import datetime
from ips.models import db
from app import login_manager
from flask_login import UserMixin

# funkcija reikalinga prijungti vartotoja prie sistemos
@login_manager.user_loader
def load_user(user_id):
    return Darbuotojas.query.get(int(user_id))

# nukreipimas prisijungti
@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/login?next=' + request.path)

# darbuotojo duomenu bazes modelis
class Darbuotojas(db.Model, UserMixin):
    __tablename__ = 'darbuotojas'
    id = db.Column(db.Integer, unique=True, primary_key=True, autoincrement=False, nullable=False)
    vardas = db.Column(db.String(20), nullable=False)
    pavarde = db.Column(db.String(20), nullable=False)
    elpastas = db.Column(db.String(80), nullable=False)
    slaptazodis = db.Column(db.Text, nullable=False)
    sukurta_data = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    pareigos = db.Column(db.String(60))
    zyma = db.relationship('Svyturelis', backref='darbuotojas', lazy=True)

    def __repr__(self):
        return f'<Darbuotojas {self.firstname} {lastname}, {id}>'
