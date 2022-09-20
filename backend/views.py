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

'''
# @vet.route('/view/owner/<int:num_page>', methods=['GET', 'POST'])
@vet.route('/view/owner')
@login_required
# def view_owner(num_page):
def view_owner():
    view_owner = Owner.query.all()
    # from sqlalchemy import desc, asc
    # variable = Owner.query.order_by(desc('id')).paginate(per_page=10, page=num_page, error_out=False)
    # var = variable
    return render_template('vet/view_owner.html', datos=view_owner)
'''
from sqlalchemy import desc, asc
@vet.route('/view/owner/<int:num_page>', methods=['GET', 'POST'])
@login_required
def view_owner(num_page):
    view_owner = Owner.query.order_by(desc('id')).paginate(per_page=5, page=num_page, error_out=False)
    return render_template('vet/view_owner.html', datos=view_owner, num_page=1)
  

@vet.route('/borrar/<string:id>')
@login_required
def borrar(id):
    elemento_a_borrar = Owner.query.get(id)
    db.session.delete(elemento_a_borrar)
    db.session.commit()
    return redirect(url_for('vet.view_owner')) 

@vet.route('/actualizar/<string:id>', methods=['GET', 'POST'])
@login_required
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

@vet.route('/pet/insert', methods=['GET', 'POST'])
@login_required
def inserta_pet():
    get_data = Owner.query.all()
    if request.method == 'POST':
        no = request.form['nom']
        es = request.form['esp']
        an = request.form['ani']
        ra = request.form['raz']
        io = request.form['ido']
        ins_pet = Pet(nombre=no, especie=es, animal=an, raza=ra, id_owner=io)
        db.session.add(ins_pet)
        db.session.commit()
        return redirect(url_for('vet.view_pet'))
    return render_template('vet/pet/inserta_pet.html', owner_list=get_data)
   
@vet.route('/ver_mascota/<int:num_page>', methods=['GET', 'POST'])
@login_required
def view_pet(num_page):
    ver_mascota = db.session.query(Owner, Pet).select_from(Owner).join(Pet).paginate(per_page=5, page=num_page, error_out=False)
    # view_pet = Pet.query.order_by(desc('id')).paginate(per_page=5, page=num_page, error_out=False).items
    return render_template('vet/pet/view_pet.html', query=ver_mascota, num_page=1)


@vet.route('/mascota/borrar/<string:id>')
@login_required
def delete_pet(id):
    borrar_mascota = Pet.query.get(id)
    db.session.delete(borrar_mascota)
    db.session.commit()
    return redirect(url_for('vet.view_pet')) 

@vet.route('/pet/actualizar/<string:id>', methods=['GET', 'POST'])
@login_required
def actualizar_pet(id):
    get_data = Owner.query.all()
    mascota = Pet.query.get(id)
    if request.method == 'POST':
        mascota.nombre = request.form['nom']
        mascota.especie = request.form['esp']
        mascota.animal = request.form['ani']
        mascota.raza = request.form['raz']
        mascota.id_owner = request.form['ido']
        db.session.commit()
        return redirect(url_for('vet.view_pet'))
    return render_template('vet/pet/actualiza_pet.html', owner_list=get_data, mascota=mascota)


@vet.route('/vaccines/insert', methods=['GET', 'POST'])
@login_required
def inserta_vaccines():
    get_data = Pet.query.all()
    if request.method == 'POST':
        nomb = request.form['nombr']
        fe = request.form['fec']
        ca = request.form['cad']
        se = request.form['ser']
        idp = request.form['idpe']
        ins_vaccines = Vaccines(nombre=nomb, fecha=fe, caducidad=ca, serie=se, id_mascota=idp)
        db.session.add(ins_vaccines)
        db.session.commit()
        return redirect(url_for('vet.view_vaccines'))
    return render_template('vet/vaccines/inserta_vaccines.html', pet_list=get_data )


@vet.route('/ver_vaccines/<int:num_page>', methods=['GET', 'POST'])
@login_required
def view_vaccines(num_page):
    ver_vacunas = db.session.query(Pet,Vaccines).select_from(Pet).join(Vaccines).paginate(per_page=5, page=num_page, error_out=False)
    return render_template('vet/vaccines/view_vaccines.html', datos=ver_vacunas,num_page=1)



@vet.route('/vaccines/borrar/<string:id>')
@login_required
def delete_vaccines(id):
    borrar_vaccines = Vaccines.query.get(id)
    db.session.delete(borrar_vaccines)
    db.session.commit()
    return redirect(url_for('vet.view_vaccines')) 

@vet.route('/vaccines/actualizar/<string:id>', methods=['GET', 'POST'])
@login_required
def actualizar_vaccines(id):
    get_data = Pet.query.all()
    vaccines = Vaccines.query.get(id)
    if request.method == 'POST':
        vaccines.nombre = request.form['nombr']
        vaccines.fecha = request.form['fec']
        vaccines.caducidad = request.form['cad']
        vaccines.serie = request.form['ser']
        vaccines.id_mascota = request.form['idpe']
        db.session.commit()
        return redirect(url_for('vet.view_vaccines'))
    return render_template('vet/vaccines/actualiza_vaccines.html', pet_list=get_data, datos=vaccines)
