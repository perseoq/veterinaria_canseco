from vendors.database import db
from flask_login import UserMixin

class Admin(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(50), nullable=False, unique=True)
    clave = db.Column(db.String(100), nullable=False)

class Owner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(300), nullable=False)
    direccion = db.Column(db.String(500), nullable=False)
    telefono = db.Column(db.String(200), nullable=False)
    correo = db.Column(db.String(300), nullable=False)
    mascota = db.relationship('Pet', backref='Owner')

class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(300), nullable=False)
    especie = db.Column(db.String(300), nullable=False)
    animal = db.Column(db.String(300), nullable=False)
    raza = db.Column(db.String(300), nullable=False)
    vacunas = db.relationship('Vaccines', backref='Pet')
    id_owner = db.Column(db.Integer, db.ForeignKey('owner.id'))

class Vaccines(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre= db.Column(db.String(300), nullable=False)
    fecha= db.Column(db.Date, nullable=False)
    caducidad= db.Column(db.Date, nullable=False)
    serie= db.Column(db.String(300), nullable=False)
    id_mascota = db.Column(db.Integer, db.ForeignKey('pet.id'))
