from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField, Form, FormField, TextField, SelectMultipleField, SelectField, MultipleFileField, widgets
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from src import tabla_usuarios, tabla_estudios
from flask import session


class ColaboradoresForm(FlaskForm):
    colaborador = StringField(
        'Ingresa el usuario el cual deseas agregar:')
    revisar = SubmitField('Revisar colaborador')

    def validate_colaborador(self, colaborador):
        user = tabla_usuarios.find_one({'usuario': colaborador.data})
        if not(user):
            raise ValidationError(
                'Este usuario no existe. Porfavor ingrese otro.')


class Registration_Form(FlaskForm):
    username = StringField('Usuario', validators=[
                           DataRequired(message='Ingrese un usuario porfavor'), Length(min=6, max=20, message='El usuario debe tener minimo 6 caracteres')])
    email = StringField('Email', validators=[DataRequired(
        message='Ingrese un email porfavor'), Email(message='No es un correo valido ')])
    password = PasswordField('Contraseña', validators=[
                             DataRequired(message='Ingrese una contraseña porfavor')])
    confirm_password = PasswordField('Confirme Contraseña', validators=[
                                     DataRequired(message='Confirme su contraseña porfavor'), EqualTo('password', message='Las contraseñas ingresadas no son las mismas')])
    submit = SubmitField('Ingrese')

    def validate_username(self, username):
        user = tabla_usuarios.find_one({'usuario': username.data})
        if user:
            raise ValidationError(
                'Este usuario no esta disponibles. Porfavor ingrese otro.')

    def validate_email(self, email):
        email = tabla_usuarios.find_one({'email': email.data})
        if email:
            raise ValidationError(
                'Este email ya esta registrado. Porfavor inicie sesion o recupere su contraseña')


class LogIn_Form(FlaskForm):
    username = StringField('Usuario', validators=[
                           DataRequired(), Length(min=6, max=20)])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    remember = BooleanField('  Recordar mi usuario')
    submit = SubmitField('Inicia Sesion')


class UpdateAccount_Form(FlaskForm):
    username = StringField('Usuario', validators=[
                           DataRequired(), Length(min=6, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Actualizar la foto',
                        validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Actualizar')

    def validate_username(self, username):
        if session['user'] != username.data:
            user = tabla_usuarios.find_one({'usuario': username.data})
            if user:
                raise ValidationError(
                    'Este usuario no esta disponibles. Porfavor ingrese otro.')

    def validate_email(self, email):
        if session['email'] != email.data:
            email = tabla_usuarios.find_one({'email': email.data})
            if email:
                raise ValidationError(
                    'Este email ya esta registrado. Porfavor inicie sesion o recupere su contraseña')


class PostForm(FlaskForm):
    paquete = SelectField('Escoge un paquete')
    titulo = SelectMultipleField('Examen(es) a realizar:')
    noExamen = StringField('EXAMENES NO REALIZADOS')
    cedula = IntegerField('*Cedula:')
    empresa = SelectField('Empresa:')
    colaborador = SelectField('Area:')
    nombre_paciente = StringField(
        '*Nombre del paciente:')
    apellido_paciente = StringField(
        '*Apellido del paciente:')
    edad = IntegerField('*Edad del paciente:')
    nombre_doctor = StringField(
        'Nombre Completo Del Doctor:')
    contenido = TextAreaField('Sintomas')
    diagnostico = TextAreaField('Diagnostico Presuntivo')
    comentarios = TextAreaField('Comentarios/Sugerencias')
    archivo1 = FileField('Radiografia 1', validators=[
        FileAllowed(['jpg', 'png', 'jpeg', 'tif'])])
    archivo2 = FileField('Radiografia 2', validators=[
        FileAllowed(['jpg', 'png', 'jpeg', 'tif'])])
    archivo3 = FileField('Radiografia 3', validators=[
        FileAllowed(['jpg', 'png', 'jpeg', 'tif'])])
    archivo4 = FileField('Radiografia 4', validators=[
        FileAllowed(['jpg', 'png', 'jpeg', 'tif'])])
    archivo5 = FileField('Radiografia 5', validators=[
        FileAllowed(['jpg', 'png', 'jpeg', 'tif'])])
    archivo6 = FileField('Tomografia1 DICOM', validators=[
        FileAllowed(['DCM', 'jpg', 'png', 'dcm'])])
    archivo7 = FileField('Tomografia2 DICOM', validators=[
        FileAllowed(['DCM', 'png', 'jpg', 'dcm'])])
    archivo8 = FileField('Tomografia3 DICOM', validators=[
        FileAllowed(['DCM', 'jpg', 'png', 'dcm'])])
    archivo9 = FileField('Archivos varios', validators=[FileAllowed(['pdf'])])
    submit = SubmitField('Agregar Estudio')


class BuscadorForm(FlaskForm):
    token = StringField('Ingrese el codigo de tu estudio',
                        validators=[DataRequired()])
    submit = SubmitField('Buscar estudio')

    def validate_token(self, token):
        estudio_token = tabla_estudios.find_one({'token': token.data})
        if not(estudio_token):
            raise ValidationError(
                'Esta clave no existe. Porfavor ingrese otra.')


class Buscador2Form(FlaskForm):
    criterio = SelectField('Buscar por:', choices=[('apellido_paciente', 'Apellido'), (
        'cedula', 'Cédula'), ('empresa', 'Empresa'), ('fecha', 'Fecha'), ('token', '#Estudio')])
    campo = StringField(DataRequired())
    submit = SubmitField('Buscar')


class Add_colaboradorForm(FlaskForm):
    l_colaborador = SelectField('Colaborador')
    submit = SubmitField('Agregar Colaborador')


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class PaqueteForm(FlaskForm):
    nombre_paquete = StringField(
        'Nombre del Paquete', validators=[DataRequired()])
    l_examenes = MultiCheckboxField('Examenes', validators=[DataRequired()])
    tarifa = IntegerField('Tarifa del paquete(dolares americanos)')
    submit = SubmitField('Agregar Paquete')


class EmpresaForm(FlaskForm):
    nombre_empresa = StringField(
        'Nombre de la Empresa', validators=[DataRequired()])
    l_examenes = MultiCheckboxField('Examenes', validators=[DataRequired()])
    l_paquetes = SelectMultipleField('Paquetes', validators=[DataRequired()])
    submit = SubmitField('Agregar Empresa')


class ExamenForm(FlaskForm):
    nombre_examen = StringField(
        'Nombre del examen', validators=[DataRequired()])
    tarifa = IntegerField(
        'Tarifa del examen(dolares americanos)', validators=[DataRequired()])
    submit = SubmitField('Agregar Examen')
