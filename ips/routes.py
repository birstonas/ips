from flask import Flask, render_template, url_for, request, Blueprint, flash, redirect
from flask_mqtt import Mqtt
import json
from ips.models import db
from main.models import Darbuotojas
from flask_socketio import SocketIO, emit
from ips.device import Device, mac_adresai, stot_xy, xy_riba
from ips.utils import ips_xy, stot_dist, save_xy, filter_location_by_date, publish_database
import numpy as np
from scipy.optimize import minimize
from ips.models import db, Svyturelis
from flask_login import login_required
from ips.forms import Datos


async_mode = None
mqtt = Mqtt() 
socketio = SocketIO(async_mode=async_mode, engineio_logger=True, logger=True, always_connect=True)
stop_loop = False # ciklo busena
n_stations = 4 # esp32 stoteliu skaičius -1 (gateways)

ips = Blueprint('ips', __name__, template_folder='templates', static_folder='static')

@ips.route('/stop', methods=['POST'])
def stop():
    global stop_loop
    stop_loop = True
    return 0

@ips.route('/start', methods=['POST'])
def start():
    global stop_loop
    stop_loop = False
    return 0

# pagrindinis IPS puslapis 
@ips.route('/', methods = ['GET', 'POST'])
@login_required
def sistema():
    global stop_loop
    darbuotojai = []
    event = 'xy_coordinates'
# jeigu POST metodas, is formos  gauname data ir pasirinkta darbuotoja
    if request.method == 'POST':
        try:
            darbuotojas = request.form.get('darbuotojas')
            nuo_diena = request.form.get('diena')
            nuo_valanda = request.form.get('appt')
            iki_diena = request.form.get('diena2')
            iki_valanda = request.form.get('appt2')
            tabelis = darbuotojas[:5]
            nuo = nuo_diena + ' ' + nuo_valanda
            iki = iki_diena + ' ' + iki_valanda
            lokacijos = filter_location_by_date(nuo, iki, tabelis)
#isvedame visus duomenis i naudotojo sasaja
            for koordinates in lokacijos:
                data = dict(
                    x = koordinates.x,
                    y = koordinates.y,
                    darbuotojas = tabelis+"i",
                    color = "blue",
                    ribos = 1,
                    greitis = 0.1,
            )
                ribos(event, data)
                if stop_loop:
                    break

        except Exception as e: flash(e, "Klaida")
# stebimu asmenu sarasas
    for i in range(len(mac_adresai)):
        try:
            darb_svyturelis = Svyturelis.query.filter_by(mac=mac_adresai[i]).first()
            darbuotojai.append(darb_svyturelis.darbuotojas)
        except Exception: flash("Vienas arba daugiau MAC adresų neturi priskirto darbuotojo, susisiekite su administratoriumi")

    return render_template('sistema.html', title='IPS sistema', darbuotojai=darbuotojai)

@ips.route('/<topic>/<msg>/<rssi>')
def publish_mqtt(topic,msg,rssi):
    mqtt.publish(topic+'/'+msg,rssi)
    return {'data': msg}

#prideti darbuotoja i duomenu baze
@ips.route('/<vardas>/<pavarde>/<elpastas>/<id>/<psw>/<pareigos>')
def publish_db(vardas,pavarde,id, psw,pareigos):
    d = publish_database(vardas,pavarde,id, psw,pareigos)
    return {'data': d}

@socketio.on('connect')
def on_socket_connect ():
#prenumeruoti zinutes pagal visus ivestus MAC adresus
    for i in range(n_stations):
        for m in range(len(mac_adresai)):
            mqtt.subscribe("station"+str(i)+"/"+mac_adresai[m])
    print ('Prisijungta prie SocketIO kliento.')

# kodas vykdomas kas kart esant naujai zinutei
@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    event = 'xy_coordinates'
    mac_topic = message.topic[9:] # tik mac adresas, nes temos vardo nereikia
    from run import app
    with app.app_context():
        darb_svyturelis = Svyturelis.query.filter_by(mac=mac_topic).first()
        darb = darb_svyturelis.darbuotojas.id
    target = Device(mac_topic,int(message.payload.decode()))
    distance = target.calculate_distance()
    stotele = message.topic[:9],
    dist_array = stot_dist(stotele,mac_topic, distance) # atstumai nuo visu ESP32 irenginiu
    if dist_array:
        koordinates = ips_xy(dist_array,stot_xy) #atstumai konvertuojami i koordinates
    else:
        koordinates = [100,10]

    data = dict(
        x = koordinates[0],
        y = koordinates[1],
        darbuotojas = darb,
        color = "red",
        ribos = 1,
        greitis = 1,
    )
    save_xy(mac_topic, data) # vieta saugoma i duomenu baze
    ribos(event, data) # patikrinimas ar zmogus patalpos ribose ir isvedama i ekrana


@mqtt.on_connect()
def on_mqtt_connect (client, userdata, flags, rc):
    print ('Prisijungta prie MQTT brokerio.')

# patikinimas ar gautos koordinates yra stebimos patalpos zonoje
def ribos(eventas, data):
    x = data['x']
    y = data['y']
    x_riba = True if xy_riba[0][0] < x < xy_riba[0][1] else False
    y_riba = True if xy_riba[1][0] < y < xy_riba[1][1] else False
    patalpoje = True if False not in [x_riba, y_riba] else False
    if patalpoje == False:
        data['ribos'] = 0
    socketio.emit(eventas, data=data)
    socketio.sleep(data['greitis'])
