from flask import Flask, render_template, url_for, request, Blueprint, flash, redirect
from main.forms import LoginForm, NaujasSlaptazodisForma
from main.models import Darbuotojas
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user, login_user, logout_user, login_required
from main.utils import save_password
from app import bcrypt, mail
from flask_mail import Message

main = Blueprint('main', __name__, template_folder='templates', static_folder='ips.static')

# pagrindinis puslapis
@main.route('/')
def index():
    return render_template('index.html', title='Pagrindinis puslapis')

# pagalbos puslapis
@main.route('/pagalba', methods = ['GET','POST'])
def pagalba():
#jeigu POST metodas, paimami formos duomenys
    if request.method == 'POST':
        siuntejas = request.form.get('fname')
        tabelis = request.form.get('ltabelis')
        tema = request.form.get('tema')
        turinys = request.form.get('uzklausa')
    #issiunciamas email
        try:
            msg = Message(turinys, recipients=[siuntejas])
            msg.body = f"Vardas: {siuntejas}\n Tabelio nr.: {tabelis}\nKlausimas: {uzklausa}"
            msg.send(msg)
            flash('Užklausa pateikta. Atsakysime kaip galėdami greičiau.')
            return redirect(url_for('main.pagalba'))
        except:
            flash('Išsiųsti užklausos nepavyko. Bandykite dar kartą arba skambinkite nurodytu telefono numeriu.')
            return redirect(url_for('main.pagalba'))
    return render_template('pagalba.html', title='Techninė pagalba')

# darbuotojo puslapis
@main.route('/darbuotojas', methods=['GET', 'POST'])
@login_required
def darbuotojas():
    form = NaujasSlaptazodisForma()
    if form.validate_on_submit():
        slapt1 = request.form.get('slapt1')
        slapt2 = request.form.get('slapt2')
        if slapt1 == slapt2:
            save_password(current_user, slapt1)
            flash('Slaptažodis sėkmingai pakeistas')
        else:
            flash('Slaptažodžiai nesutampa')
    return render_template('darbuotojas.html', title='Darbuotojo puslapis', forma=form)

# prisijungimo puslapis
@main.route('/login', methods=['GET', 'POST'])
def login():
    form  = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    if form.validate_on_submit():
        try:
            tabelis = request.form.get('tabelioNr')
            psw = request.form.get('slaptazodis')
            prisiminti = True if request.form.get('prisiminti') else False
            user = Darbuotojas.query.filter_by(id=tabelis).first()
            if user:
                if user.slaptazodis == psw or bcrypt.check_password_hash(user.slaptazodis, psw):
                    login_user(user)
                    flash('Sekmingai prisijungėte.')
                    return redirect(url_for('ips.sistema'))
                else:
                    flash('Blogi prisijungimo duomenys.')
                    return redirect(url_for('main.login'))
        except Exception as e: flash(e, "Klaida")
    return render_template('login.html', title='Prisijungimo puslapis', form=form)


# atsijungimo kelias
@main.route("/atsijungti")
@login_required
def logout():
    logout_user()
    flash('Sėkmingai atsijungėte.')
    return redirect(url_for('main.index'))
