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
    add= InsertarOwner()
    if add.validate_on_submit(): #validamos datos
        n = add.n.data
        d= add.d.data
        t = add.t.data
        c = add.c.data
        add_owner = Owner(nombre=n,direccion=d,telefono=t,correo=c)
        db.session.add(add_owner)
        db.session.commit()
        return redirect(url_for('vet.add_owner'))
    return render_template('vet/insert_owner.html',form=add)

@vet.route('/view/owner')
def view_owner():
    view_owner = Owner.query.all()
    return render_template('vet/view_owner.html', datos=view_owner)

@vet.route('/borrar/<string:id>')
def borrar(id):
    elemento_a_borrar = Owner.query.get(id)
    db.session.delete(elemento_a_borrar)
    db.session.commit()
    return redirect(url_for('vet.view_owner')) 

@vet.route('/actualizar/<string:id>', methods=['GET', 'POST'])
def actualizar_owner(id):
    query = Owner.query.get(id)
    if request.method == 'POST':
        query.nombre = request.form['nombre']
        query.direccion = request.form['direccion']
        query.telefono= request.form['telefono']
        query.correo = request.form['correo']
        db.session.commit()
        return redirect(url_for('vet.view_owner'))
    return render_template('vet/actualizar_owner.html', datos=query)


   










