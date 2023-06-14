from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Svyturelio duomenu bazes modelis
class Svyturelis(db.Model):
    id = db.Column(db.Integer, autoincrement=True)
    mac = db.Column(db.String(20),  primary_key=True, unique=True, nullable=False)
    station1 = db.Column(db.Integer, default=1, nullable=False)
    station2 = db.Column(db.Integer, default=1, nullable=False)
    station3 = db.Column(db.Integer, default=1, nullable=False)
    tabelis = db.Column(db.Integer, db.ForeignKey('darbuotojas.id'), default=1095)
    vietos = db.relationship('Vieta', backref='zyma', uselist=False)

    def __repr__(self):
        return f'<Svyturelis {self.mac} {self.station1} {self.station2} {self.station3}>'

# Vietos duomenu bazes modelis
class Vieta(db.Model):
    data = db.Column(db.DateTime, primary_key=True, autoincrement=False)
    x  = db.Column(db.Integer, default=1, nullable=False)
    y  = db.Column(db.Integer, default=1, nullable=False)
    svyt_mac = db.Column(db.String(20), db.ForeignKey('svyturelis.mac'))


    def __repr__(self):
        return f'<{self.svyt_mac} koordinatės {self.x} {self.y}>'
