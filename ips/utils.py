# pagalbiniu funkciju failas
import numpy as np
from scipy.optimize import minimize
from ips.models import db, Svyturelis, Vieta
from main.models import Darbuotojas
from datetime import datetime

async_mode = None
# grazina x,y koordinates pagal minimum 3 atstumus
def ips_xy(distances_to_station, stations_coordinates):
	def error(x, c, r):
		return sum([(np.linalg.norm(x - c[i]) - r[i]) ** 2 for i in range(len(c))])

	l = len(stations_coordinates)
	S = sum(distances_to_station) 
	W = [((l - 1) * S) / (S - w) for w in distances_to_station]
	# apytiksli vieta
	x0 = sum([W[i] * stations_coordinates[i] for i in range(l)])
	# optimizavimas naudojant Nelder-Mead metoda
	return minimize(error, x0, args=(stations_coordinates, distances_to_station), method='Nelder-Mead').x



# grazina atstumus nuo svyturelio iki visu esp32 stoteliu
def stot_dist(topic, mac_a, distance):
	from run import app
	with app.app_context():
		try:
			beacon = Svyturelis.query.filter_by(mac=mac_a).first()
			tt = str(topic[0][:-1])
			if tt == 'station1':
				beacon.station1 = int(distance)
			if tt == 'station2':
				beacon.station2 = int(distance)
			if tt == 'station3':
				beacon.station3 = int(distance)
			atstumai = [beacon.station1, beacon.station2, beacon.station3]
			db.session.add(beacon)
			db.session.commit()
		except Exception:
			return False
	return atstumai


# issaugoti buvimo vietos informacija i duomenu baze
def save_xy(mac_topic, data):
	from run import app
	with app.app_context():
		now = datetime.now()
		vieta = Vieta(data=now.strftime("%Y/%m/%d/, %H:%M:%S"), svyt_mac=mac_topic, x=data['x'], y=data['y'])
		db.session.add(vieta)
		db.session.commit()
# kol kas nenaudojama
def publish_database(vardas,pavarde,id, psw,pareigos):
	from run import app
	with app.app_context():
		d = Darbuotojas(vardas=vardas,pavarde=pavarde,elpastas=elpastas,id=id,slaptazodis=psw,pareigos=pareigos)
		db.session.add(d)
		db.session.commit()
		return {'data': d}

# palyginami ir grazinami vietos duomenys pagal nurodyta data
def filter_location_by_date(start_range, end_range, tabel):
	from run import app
	with app.app_context():
                zyma = Svyturelis.query.filter_by(tabelis=tabel).first()
                lokacijos = db.session.query(Vieta).filter(Vieta.data.between(start_range, end_range)).filter(Vieta.svyt_mac==zyma.mac).all()
                return lokacijos
