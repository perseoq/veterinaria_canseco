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

@vet.route('/owner/insert', methods=['GET', 'POST'])
@login_required
def add_owner():
    form_owner = InsertarOwner()
    if form_owner.validate_on_submit():
        nom = form_owner.n.data
        dir = form_owner.d.data
        tel = form_owner.t.data
        cor = form_owner.c.data
        add_owner = Owner(nombre=nom, direccion=dir, telefono=tel, correo=cor)
        db.session.add(add_owner)
        db.session.commit()
        return redirect(url_for('vet.add_owner'))
    return render_template('vet/insert_owner.html', form=form_owner)

if request.method == 'POST':
nombre = request.form['nombre']
user = request.form['usuario']
correo = request.form['email']