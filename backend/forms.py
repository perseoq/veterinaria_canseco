from flask_wtf import FlaskForm
from wtforms import StringField, DateField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired
from backend.models import Owner, Pet

class AccesoLogin(FlaskForm):
    user = StringField('Inserta tu usuario', validators=[DataRequired()])
    passw = PasswordField('Inserta tu contraseña', validators=[DataRequired()])
    entrar = SubmitField('Entrar')

class InsertarOwner(FlaskForm):
    n = StringField('Inserta nombre', validators=[DataRequired()]) 
    d = StringField('Inserta direccion', validators=[DataRequired()])
    t = StringField('Inserta telefono', validators=[DataRequired()])
    c = StringField('Inserta correo', validators=[DataRequired()])
    submit = SubmitField('Insertar')



