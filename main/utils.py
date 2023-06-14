from ips.models import db
from main.models import Darbuotojas
from app import bcrypt


# slaptazodzio keitimas, issaugoti slaptazodi hash formatu
def save_password(c_user,password):
    from run import app
    with app.app_context():
        user = Darbuotojas.query.filter_by(id=c_user.id).first()
        hash = bcrypt.generate_password_hash(password, 10).decode('utf-8')
        user.slaptazodis = hash
        db.session.add(user)
        db.session.commit()
