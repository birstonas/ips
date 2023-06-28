from flask import Flask, Blueprint
from flask_mqtt import Mqtt
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_mail import Mail
login_manager = LoginManager()

migrate = Migrate()
bcrypt = Bcrypt()
mail = Mail()

#nustatymai
def create_app(debug=False):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '##'
    app.config['MQTT_BROKER_URL'] = 'localhost'
    app.config['MQTT_USERNAME'] = 'paulius'
    app.config['MQTT_PASSWORD'] = '##'
    app.config['MQTT_BROKER_PORT'] = 1883
    app.config['MQTT_TLS_ENABLED'] = False
    app.config['TEMPLATES_AUTO_RELOAD'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://'
    app.config['SQLALCHEY_TRACK_MODIFICATIONS'] = False
#el.pašto nustatymai
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = '4654'
    app.config['MAIL_USERNAME'] = '##pakeisti###'
    app.config['MAIL_PASSWORD'] = '##pakeisti###'
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True


    from ips.routes import ips
    from main.routes import main
    app.register_blueprint(ips, url_prefix='/ips')
    app.register_blueprint(main, url_prefix='/')
    with app.app_context():
        from ips.models import db
        from ips.routes import mqtt
        mqtt.init_app(app)
        db.init_app(app)
        migrate.init_app(app, db)
        login_manager.init_app(app)
        bcrypt.init_app(app)
        mail.init_app(app)

    return app
