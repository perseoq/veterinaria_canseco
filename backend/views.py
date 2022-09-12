from flask import Blueprint, render_template, redirect, url_for, request
from backend.forms import AccesoLogin, InsertarOwner
from backend.models import Admin, Owner, Pet, Vaccines
from flask_login import login_required, login_user, logout_user
from vendors.database import db

vet = Blueprint('vet', __name__)


@vet.route('/', methods=['GET', 'POST'])
def iniciar_sesion():
    formulario_login = AccesoLogin()
    if formulario_login.validate_on_submit():
        admin = Admin.query.filter_by(usuario=formulario_login.user.data, clave=formulario_login.passw.data).first()
        if admin:
            login_user(admin)
            return redirect(url_for('vet.veterinaria'))
        return redirect(url_for('vet.iniciar_sesion'))
    return render_template('login/login.html', data=formulario_login)

@vet.route('/close')
@login_required
def close():
    logout_user()
    return redirect(url_for('vet.iniciar_sesion'))

@vet.route('/principal')
@login_required
def veterinaria():
    queries = db.session.query(Owner, Pet, Vaccines).select_from(Owner).join(Pet).join(Vaccines).all() 
    return render_template('panel/admin.html', queries=queries)

# ACCIONES DE OWNER

@vet.route('/owner/insert', methods=['GET','POST'])
@login_required
def add_owner():
    if request.method == 'POST':
        nom = request.form['nombre']
        dir = request.form['direccion']
        tel = request.form['telefono']
        cor = request.form['correo']
        add_owner = Owner(nombre=nom,direccion=dir,telefono=tel,correo=cor)
        db.session.add(add_owner)
        db.session.commit()
        return redirect(url_for('vet.add_owner'))
    return render_template('vet/insert_owner.html')

@vet.route('/pet/insert', methods=['GET','POST'])
@login_required
def add_pet():
    if request.method == 'POST':
        nom = request.form['nombre']
        es = request.form['especie']
        ani = request.form['animal']
        ra = request.form['raza']
        va = request.form['vacunas']
        add_pet = Pet(nombre=nom,especie=es,animal=ani,raza=ra,vacunas=va)
        db.session.add(add_pet)
        db.session.commit()
        return redirect(url_for('vet.add_pet'))
    return render_template('vet/insert_pet.html')

@vet.route('/vaccines/insert', methods=['GET','POST'])
@login_required
def add_vaccines():
    if request.method == 'POST':
        nom = request.form['nombre']
        fe = request.form['fecha']
        ca = request.form['caducidad']
        se = request.form['serie']
        add_vaccines = Vaccines(nombre=nom,fecha=fe,caducidad=ca,serie=se)
        db.session.add(add_vaccines)
        db.session.commit()
        return redirect(url_for('vet.add_vaccines'))
    return render_template('vet/insert_vaccines.html')