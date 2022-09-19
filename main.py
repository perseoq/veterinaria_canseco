from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from vendors.database import db
from vendors.config import DevConfig

app = Flask(__name__)
app.config.from_object(DevConfig)
SQLAlchemy(app)

from backend.views import vet
app.register_blueprint(vet)

from flask_login import LoginManager
login = LoginManager()
login.init_app(app)
login.login_view = 'login'

@app.teardown_appcontext
def shutdown_database_conection(exception=None):
    db.session.remove()

from backend.models import Admin
@login.user_loader
def load_admin_or_user(id):
    admin = Admin.query.get(int(id))
    # varible = Tabla.query.get(int(id))
    if admin:
        return admin
    '''
    else:
        return variable
    '''    


with app.app_context():
    db.create_all()