from PIL import Image
import os
import time
import secrets
from flask import render_template, flash, redirect, url_for, session, request
from src.forms import Registration_Form, LogIn_Form, UpdateAccount_Form, PostForm, BuscadorForm, Add_colaboradorForm, ColaboradoresForm, Buscador2Form, PaqueteForm, EmpresaForm, ExamenForm
from src import app, bcrypt, tabla_estudios, tabla_usuarios, tabla_examenes, tabla_paquetes, tabla_empresas
# from flask_login import current_user, login_user
from bson.objectid import ObjectId
from math import ceil

# def acceso(template, title):
#     if 'user' in session:
#         return render_template(template, title=title, control_center=True)
#     else:
#         return redirect(url_for('login'))


@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
    form = BuscadorForm()
    if form.validate_on_submit():
        estudio = tabla_estudios.find_one({'token': form.token.data})

        return redirect(url_for('estudio', _id=estudio['_id']))
    return render_template('home.html', title='Home', legend='Holi', css=True, form=form)


@app.route("/about")
def about():
    return render_template('about.html', title='About', css=True)


@app.route("/historial", methods=['GET', 'POST'])
def historial():
    if 'user' in session:
        limit = 10
        page = request.args.get('page', 1, type=int)
        starting_id = tabla_estudios.find(
            {'creador': session['user']}).sort('_id', -1)
        count = tabla_estudios.count_documents({'creador': session['user']})
        total_pages = ceil(count / limit)
        mitad = ceil(total_pages/2)
        hola = tabla_estudios.find_one({'usuario': session['user']})
        estudios = []
        pages = []
        if hola:
            if page == 1 or page == total_pages:
                pages = []
                c = 0
                if mitad % 2 == 0:
                    print('impar')
                    for i in range(1, total_pages+1):
                        if c < 2 or c == total_pages-1 or c == total_pages-2 or c == mitad-2 or c == mitad or c == mitad-1:
                            pages.append(i)
                        else:
                            pages.append(None)
                        c += 1
                    print(total_pages)
                    print(c)
                    print(pages)
                else:
                    print('par')
                    for i in range(1, total_pages+1):
                        if c < 2 or c == total_pages-1 or c == total_pages-2 or c == mitad or c == mitad-1:
                            pages.append(i)
                        else:
                            pages.append(None)
                        c += 1
                    print(total_pages)
                    print(c)
                    print(pages)
            else:
                pages = []
                c = 0
                for i in range(1, total_pages+1):
                    if c == 0 or c == total_pages-1 or c == page or c == page-1 or c == page-2:
                        pages.append(i)
                    else:
                        pages.append(None)
                    c += 1
                print(pages)
            last_id = starting_id[(page-1)*limit]['_id']
            estudios = tabla_estudios.find({'usuario': session['user'], '_id': {
                '$lte': last_id}}).sort('_id', -1).limit(limit)
        if not(estudios):
            vacio_historial = True
        else:
            vacio_historial = False
        form = Buscador2Form()
        if form.validate_on_submit():
            return redirect(url_for('busqueda', campo=form.campo.data, criterio=form.criterio.data))
        return render_template('historial.html', title='Estudios', control_center=True, estudios=estudios, css=True, pages=pages, current_page=page, vacio_historial=vacio_historial, form=form)
    else:
        return redirect(url_for('login'))


@app.route("/historial/new", methods=['GET', 'POST'])
def new():
    if 'user' in session:
        form = PostForm()
        empresas = tabla_empresas.find({'creador': session['user']})
        paquetes = tabla_paquetes.find({'creador': session['user']})
        creador = tabla_usuarios.find_one({'usuario': session['user']})
        form.colaborador.choices = [(colaborador, colaborador) for colaborador in creador['colaboradores']]
        form.empresa.choices = [(empresa['nombre'], empresa['nombre']) for empresa in empresas]
        form.paquete.choices = [(paquete['nombre'], paquete['nombre']) for paquete in paquetes]
        if form.validate_on_submit():
            n_radiografias = 0
            n_tomografias = 0
            token = secrets.token_hex(3)
            if form.archivo1.data:
                archivo1, f_ext1 = save_picture(
                    form.archivo1.data, resize=False)
                n_radiografias += 1
            else:
                archivo1 = 'nada'
                f_ext1 = '.'
            if form.archivo2.data:
                archivo2, f_ext2 = save_picture(
                    form.archivo2.data, resize=False)
                n_radiografias += 1
            else:
                archivo2 = 'nada'
                f_ext2 = '.'
            if form.archivo3.data:
                archivo3, f_ext3 = save_picture(
                    form.archivo3.data, resize=False)
                n_radiografias += 1
            else:
                archivo3 = 'nada'
                f_ext3 = '.'
            if form.archivo4.data:
                archivo4, f_ext4 = save_picture(
                    form.archivo4.data, resize=False)
                n_radiografias += 1
            else:
                archivo4 = 'nada'
                f_ext4 = '.'
            if form.archivo5.data:
                archivo5, f_ext5 = save_picture(
                    form.archivo5.data, resize=False)
                n_radiografias += 1
            else:
                archivo5 = 'nada'
                f_ext5 = '.'
            if form.archivo6.data:
                archivo6, f_ext6 = save_picture(
                    form.archivo6.data, resize=False)
                n_tomografias += 1
            else:
                archivo6 = 'nada'
                f_ext6 = '.'
            if form.archivo7.data:
                archivo7, f_ext7 = save_picture(
                    form.archivo7.data, resize=False)
                n_tomografias += 1
            else:
                archivo7 = 'nada'
                f_ext7 = '.'
            if form.archivo8.data:
                archivo8, f_ext8 = save_picture(
                    form.archivo8.data, resize=False)
                n_tomografias += 1
            else:
                archivo8 = 'nada'
                f_ext8 = '.'
            if form.archivo9.data:
                archivo9, f_ext9 = save_picture(
                    form.archivo9.data, resize=False)
                n_tomografias += 1
            else:
                archivo9 = 'nada'
                f_ext9 = '.'
            estudio = {
                'usuario': session['user'],
                'creador': session['user'],
                'creador-imagen': session['image'],
                'titulo': form.titulo.data.upper(),
                'nombre_paciente': form.nombre_paciente.data.upper(),
                'apellido_paciente': form.apellido_paciente.data.upper(),
                'edad': form.edad.data,
                'cedula': form.cedula.data,
                'empresa': form.empresa.data.upper(),
                'nombre_doctor': form.nombre_doctor.data.upper(),
                'paquete':form.paquete.data.upper(),
                'contenido': form.contenido.data,
                'diagnostico': form.diagnostico.data,
                'comentarios': form.comentarios.data,
                'fecha': time.strftime("%d-%m-%Y"),
                'archivos': [(archivo1, '1', f_ext1), (archivo2, '2', f_ext2), (archivo3, '3', f_ext3), (archivo4, '4', f_ext4), (archivo5, '5', f_ext5), (archivo6, '6', f_ext6), (archivo7, '7', f_ext7), (archivo8, '8', f_ext8), (archivo9, '9', f_ext9)],
                'token': token,
                'n_radiografia': n_radiografias,
                'n_tomografia': n_tomografias,
                'colaboradores': form.colaborador.data
            }
            tabla_estudios.insert_one(estudio)
            flash('Estudio registrado correctamente', 'success')
            return redirect(url_for('new'))
        return render_template('create_post.html', title='Nuevo Estudio', control_center=True, form=form, css=True, legend='Nuevo Estudio')
    else:
        return redirect(url_for('login'))


@app.route("/consulta")
def consulta():
    if 'user' in session:
        return render_template('consulta.html', title='Consulta Virtual', control_center=True)
    else:
        return redirect(url_for('login'))


@app.route("/ia")
def ia():
    if 'user' in session:
        return render_template('ia.html', title='IA BETA', control_center=True)
    else:
        return redirect(url_for('login'))


@app.route("/login", methods=['GET', 'POST'])
def login():
    if 'user' in session:
        return redirect(url_for('index'))
    login = LogIn_Form()
    if login.validate_on_submit():
        user = tabla_usuarios.find_one({'usuario': login.username.data})
        if user and bcrypt.check_password_hash(user['password'], login.password.data):
            # login_user(user, remember=login.remember.data)
            flash('Inicio de sesion completado satisfactoriamente', 'success')
            session['user'] = user['usuario']
            session['email'] = user['email']
            if user['image'] != None:
                session['image'] = user['image']
            else:
                session['image'] = 'default.jpg'
            next_page = request.args.get('next')
            print(next_page)
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash(
                'No se pudo iniciar sesion, porfavor revise el usuario y contraseña', 'danger')
    return render_template('inicio_sesion.html', title='Inicio Sesion', form=login)


@app.route("/register", methods=['POST', 'GET'])
def register():
    if 'user' in session:
        return redirect(url_for('index'))
    register = Registration_Form()
    if register.validate_on_submit():
        hashed_pass = bcrypt.generate_password_hash(
            register.password.data).decode('utf-8')
        usuario = {'usuario': register.username.data,
                   'password': hashed_pass, 'email': register.email.data, 'image': 'default.jpg', 'colaboradores': ['nada']}
        paquete = {
            'nombre': 'ninguno'.upper(),
            'creador': register.username.data,
            'examenes': 'ninguno',
            'tarifa': 0
        }
        empresa = {
            'nombre': 'particular'.upper(),
            'paquetes': 'ninguno',
            'examenes': 'ninguno',
            'creador': register.username.data
        }
        tabla_empresas.insert_one(empresa)
        tabla_paquetes.insert_one(paquete)
        tabla_usuarios.insert_one(usuario)
        session['user'] = register.username.data
        session['email'] = register.email.data
        session['image'] = 'default.jpg'
        flash(
            f'Tu cuenta fue creada satisfactoriamente tu usuario es:{register.username.data}', 'success')
        return redirect(url_for('login'))
    return render_template('registro.html', title='Registro', form=register)


def save_picture(form_picture, resize=True, tomografia=False):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    if resize:
        picture_path = os.path.join(
            app.root_path, 'static/profile-pic', picture_fn)
        output_size = (125, 125)
        i = Image.open(form_picture)
        i.thumbnail(output_size)
        i.save(picture_path)
    else:
        picture_path = os.path.join(
            app.root_path, 'static/estudio-pic', picture_fn)
        form_picture.save(picture_path)
    return picture_fn, f_ext


@app.route("/perfil", methods=['GET', 'POST'])
def perfil():
    if 'user' in session:
        profile = url_for('static', filename='profile-pic/'+session['image'])
        form = UpdateAccount_Form()
        if form.validate_on_submit():
            user = tabla_usuarios.find_one({'usuario': session['user']})
            colaboradores = user['colaboradores']
            if form.picture.data:
                if user['image'] != 'default.jpg':
                    picture_path = os.path.join(
                        app.root_path, 'static/profile-pic', user['image'])
                    os.remove(picture_path)
                picture_file, _ = save_picture(form.picture.data)
                session['image'] = picture_file
            cambios = {'usuario': form.username.data,
                       'email': form.email.data, 'image': session['image']}
            tabla_usuarios.update_one(
                {'usuario': session['user']}, {'$set': cambios})
            session['user'] = form.username.data
            session['email'] = form.email.data
            flash('Tus cambios se han actualizado', 'success')
            return redirect(url_for('perfil'))
        elif request.method == 'GET':
            form.username.data = session['user']
            form.email.data = session['email']
        usuario = tabla_usuarios.find_one({'usuario': session['user']})
        colaboradores = usuario['colaboradores']
        print(colaboradores)
        print(len(colaboradores))
        return render_template('perfil.html', title='Perfil', control_center=True, profile=profile, form=form, css=True)
    else:
        return redirect(url_for('login'))


@app.route("/Index", methods=['GET', 'POST'])
def index():
    if 'user' in session:
        estudios = tabla_estudios.find({'creador': session['user']})
        notificaciones = []
        for estudio in estudios:
            if estudio['titulo'] == '' or estudio['nombre_paciente'] == '' or estudio['apellido_paciente'] == '' or estudio['nombre_doctor'] == '' or estudio['apellido_doctor'] == '' or estudio['contenido'] == '' or estudio['diagnostico'] == '' or estudio['comentarios'] == '':
                notificaciones.append(estudio)
        if not(notificaciones):
            vacio_notificaciones = True
        else:
            vacio_notificaciones = False
        return render_template('notificaciones.html', title='Notificaciones ', control_center=True, css=True, notificaciones=notificaciones, vacio_notificaciones=vacio_notificaciones)
    else:
        return redirect(url_for('login'))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('home'))


@app.route("/historial/<_id>", methods=['GET', 'POST'])
def estudio(_id):
    estudio = tabla_estudios.find_one({'_id': ObjectId(_id)})
    creador = tabla_usuarios.find_one({'usuario': estudio['usuario']})
    if 'user' in session:
        if session['user'] == estudio['creador']:
            form = Add_colaboradorForm()
            form.l_colaborador.choices = [
                (colaborador, colaborador) for colaborador in creador['colaboradores'][1:]]
            # if form.validate_on_submit():
            print(request.args.to_dict())
            if request.args.to_dict():
                colaborador = request.args.to_dict()['l_colaborador']
                tabla_estudios.update_one({'_id': ObjectId(_id)}, {
                                          '$set': {'colaboradores': colaborador, 'compartir': 'compartido'}})
                flash('Colaborador Agregado Satisfactoriamente!', 'success')
            contador = len(creador['colaboradores'])
            if contador == 1 and creador['colaboradores'][0] == 'nada':
                sw_colab = False
            else:
                sw_colab = True
            print(sw_colab, contador, creador['colaboradores'])
            return render_template('estudio.html', title=estudio['titulo'], estudio=estudio, control_center=True, creador=creador, css=True, form=form, sw_colab=sw_colab)
        return render_template('estudio.html', title=estudio['titulo'], estudio=estudio, control_center=True, creador=creador, css=True)
    else:
        return render_template('estudio.html', title=estudio['titulo'], estudio=estudio, control_center=False, creador=creador, css=True)


@app.route("/historial/<_id>/update", methods=['GET', 'POST'])
def actualizar_estudio(_id):
    estudio = tabla_estudios.find_one({'_id': ObjectId(_id)})
    form = PostForm()
    empresas = tabla_empresas.find({'creador': session['user']})
    paquetes = tabla_paquetes.find({'creador': session['user']})
    creador = tabla_usuarios.find_one({'usuario': session['user']})
    form.colaborador.choices = [(colaborador, colaborador) for colaborador in creador['colaboradores']]
    form.empresa.choices = [(empresa['nombre'], empresa['nombre']) for empresa in empresas]
    form.paquete.choices = [(paquete['nombre'], paquete['nombre']) for paquete in paquetes]
    if form.validate_on_submit():
        n_radiografias = 0
        n_tomografias = 0
        if form.archivo1.data:
            if estudio['archivos'][0][0] != 'nada':
                picture_path = os.path.join(
                    app.root_path, 'static/estudio-pic', estudio['archivos'][0][0])
                os.remove(picture_path)
            archivo1, f_ext1 = save_picture(form.archivo1.data, resize=False)
        else:
            archivo1, f_ext1 = estudio['archivos'][0][0], estudio['archivos'][0][2]
        if form.archivo2.data:
            if estudio['archivos'][1][0] != 'nada':
                picture_path = os.path.join(
                    app.root_path, 'static/estudio-pic', estudio['archivos'][1][0])
                os.remove(picture_path)
            archivo2, f_ext2 = save_picture(form.archivo2.data, resize=False)
        else:
            archivo2, f_ext2 = estudio['archivos'][1][0], estudio['archivos'][1][2]
        if form.archivo3.data:
            if estudio['archivos'][2][0] != 'nada':
                picture_path = os.path.join(
                    app.root_path, 'static/estudio-pic', estudio['archivos'][2][0])
                os.remove(picture_path)
            archivo3, f_ext3 = save_picture(form.archivo3.data, resize=False)
        else:
            archivo3, f_ext3 = estudio['archivos'][2][0], estudio['archivos'][2][2]
        if form.archivo4.data:
            if estudio['archivos'][3][0] != 'nada':
                picture_path = os.path.join(
                    app.root_path, 'static/estudio-pic', estudio['archivos'][3][0])
                os.remove(picture_path)
            archivo4, f_ext4 = save_picture(form.archivo4.data, resize=False)
        else:
            archivo4, f_ext4 = estudio['archivos'][3][0], estudio['archivos'][3][2]
        if form.archivo5.data:
            if estudio['archivos'][4][0] != 'nada':
                picture_path = os.path.join(
                    app.root_path, 'static/estudio-pic', estudio['archivos'][4][0])
                os.remove(picture_path)
            archivo5, f_ext5 = save_picture(form.archivo5.data, resize=False)
        else:
            archivo5, f_ext5 = estudio['archivos'][4][0], estudio['archivos'][4][2]
        if form.archivo6.data:
            if estudio['archivos'][5][0] != 'nada':
                picture_path = os.path.join(
                    app.root_path, 'static/estudio-pic', estudio['archivos'][5][0])
                os.remove(picture_path)
            archivo6, f_ext6 = save_picture(form.archivo6.data, resize=False)
        else:
            archivo6, f_ext6 = estudio['archivos'][5][0], estudio['archivos'][5][2]
        if form.archivo7.data:
            if estudio['archivos'][6][0] != 'nada':
                picture_path = os.path.join(
                    app.root_path, 'static/estudio-pic', estudio['archivos'][6][0])
                os.remove(picture_path)
            archivo7, f_ext7 = save_picture(form.archivo7.data, resize=False)
        else:
            archivo7, f_ext7 = estudio['archivos'][6][0], estudio['archivos'][6][2]
        if form.archivo8.data:
            if estudio['archivos'][7][0] != 'nada':
                picture_path = os.path.join(
                    app.root_path, 'static/estudio-pic', estudio['archivos'][7][0])
                os.remove(picture_path)
            archivo8, f_ext8 = save_picture(form.archivo8.data, resize=False)
        else:
            archivo8, f_ext8 = estudio['archivos'][7][0], estudio['archivos'][7][2]
        if form.archivo9.data:
            if estudio['archivos'][8][0] != 'nada':
                picture_path = os.path.join(
                    app.root_path, 'static/estudio-pic', estudio['archivos'][8][0])
                os.remove(picture_path)
            archivo9, f_ext9 = save_picture(form.archivo9.data, resize=False)
        else:
            archivo9, f_ext9 = estudio['archivos'][8][0], estudio['archivos'][8][2]

        archivos = [(archivo1, '1', f_ext1), (archivo2, '2', f_ext2), (archivo3, '3', f_ext3), (archivo4, '4', f_ext4),
                    (archivo5, '5', f_ext5), (archivo6, '6', f_ext6), (archivo7, '7', f_ext7), (archivo8, '8', f_ext8), (archivo9, '9', f_ext9)]
        for archivo in archivos:
            if archivo[0] != 'nada':
                if archivo[1] == '6' or archivo[1] == '7' or archivo[1] == '8':
                    n_tomografias += 1
                n_radiografias += 1
        cambios = {
            'usuario': session['user'],
            'titulo': form.titulo.data.upper(),
            'nombre_paciente': form.nombre_paciente.data.upper(),
            'apellido_paciente': form.apellido_paciente.data.upper(),
            'cedula': form.cedula.data,
            'empresa': form.empresa.data,
            'paquete': form.paquete.data,
            'edad': form.edad.data,
            'nombre_doctor': form.nombre_doctor.data.upper(),
            'contenido': form.contenido.data,
            'diagnostico': form.diagnostico.data,
            'comentarios': form.comentarios.data,
            'fecha': time.strftime("%d-%m-%Y"),
            'archivos': archivos,
            'n_radiografia': n_radiografias,
            'n_tomografia': n_tomografias,
            'colaboradores': form.colaborador.data
        }
        tabla_estudios.update_one(
            {'usuario': session['user']}, {'$set': cambios})
        flash('Cambios Realizados Satisfactoriamente!', 'success')
        return redirect(url_for('estudio', _id=estudio['_id']))
    elif request.method == 'GET':
        form.paquete.data = estudio['paquete']
        form.colaborador.data = estudio['colaboradores']
        form.apellido_paciente.data = estudio['apellido_paciente']
        form.edad.data = estudio['edad']
        form.cedula.data = estudio['cedula']
        form.empresa.data = estudio['empresa']
        form.comentarios.data = estudio['comentarios']
        form.contenido.data = estudio['contenido']
        form.diagnostico.data = estudio['diagnostico']
        form.nombre_doctor.data = estudio['nombre_doctor']
        form.nombre_paciente.data = estudio['nombre_paciente']
        form.titulo.data = estudio['titulo']
        form.archivo1.data = estudio['archivos'][0][0]
        form.archivo2.data = estudio['archivos'][1][0]
        form.archivo3.data = estudio['archivos'][2][0]
        form.archivo4.data = estudio['archivos'][3][0]
        form.archivo5.data = estudio['archivos'][4][0]
        form.archivo6.data = estudio['archivos'][5][0]
        form.archivo7.data = estudio['archivos'][6][0]
        form.archivo8.data = estudio['archivos'][7][0]
        form.archivo9.data = estudio['archivos'][8][0]
    return render_template('create_post.html', title='Actualizar Estudio', control_center=True, form=form, css=True, legend='Actualizar Estudio')


@app.route("/historial/<_id>/delete", methods=['POST'])
def borrar_estudio(_id):
    estudio = tabla_estudios.find_one({'_id': ObjectId(_id)})
    tabla_estudios.delete_one({'_id': ObjectId(_id)})
    for archivo in estudio['archivos']:
        if archivo[0] != 'nada':
            picture_path = os.path.join(
                app.root_path, 'static/estudio-pic', archivo[0])
            os.remove(picture_path)
    return redirect(url_for('historial'))


@app.route("/estadisticas/<user>/", methods=['GET', 'POST'])
def estadisticas(user):
    if 'user' in session:
        return render_template('estadisticas.html', title='Estadisticas', control_center=True, css = True)
    else:
        return redirect(url_for('login'))


@app.route("/colaboradores/", methods=['GET', 'POST'])
def colaboradores():
    if 'user' in session:
        profile = url_for('static', filename='profile-pic/'+session['image'])
        form = ColaboradoresForm()
        user = tabla_usuarios.find_one({'usuario': session['user']})
        colaboradores = user['colaboradores']
        if form.validate_on_submit():
            if form.colaborador.data:
                colaboradores.append(form.colaborador.data)
                tabla_usuarios.update_one({'usuario': session['user']}, {
                                          '$set': {'colaboradores': colaboradores}})
        if colaboradores[0] == 'nada' and len(colaboradores) <= 1:
            vacio_colaboradores = True
        else:
            vacio_colaboradores = False
            colaboradores = colaboradores[1:]
    return render_template('colaboradores.html', title='Colaboradores', control_center=True, css=True, form=form, colaboradores=colaboradores, vacio_colaboradores=vacio_colaboradores, profile=profile)


@app.route('/busqueda/<criterio>/<campo>', methods=['GET', 'POST'])
def busqueda(criterio, campo):
    if 'user' in session:
        limit = 10
        if criterio == 'edad' or criterio == 'cedula' :
            campo = int(campo)
        else:
            campo = campo.upper()
        starting_id = tabla_estudios.find(
            {"$and": [{'creador': session['user']}, {criterio: campo}]}).sort('_id', -1)
        page = request.args.get('page', 1, type=int)
        count = tabla_estudios.count_documents(
            {"$and": [{'creador': session['user']}, {criterio: campo}]})
        total_pages = ceil(count / limit)
        mitad = ceil(total_pages/2)
        hola = tabla_estudios.find_one(
            {"$and": [{'creador': session['user']}, {criterio: campo}]})
        estudios = []
        pages = []
        print(hola)
        print(count)
        if hola:
            if page == 1 or page == total_pages:
                pages = []
                c = 0
                if mitad % 2 == 0:
                    print('impar')
                    for i in range(1, total_pages+1):
                        if c < 2 or c == total_pages-1 or c == total_pages-2 or c == mitad-2 or c == mitad or c == mitad-1:
                            pages.append(i)
                        else:
                            pages.append(None)
                        c += 1
                    print(total_pages)
                    print(c)
                    print(pages)
                else:
                    print('par')
                    for i in range(1, total_pages+1):
                        if c < 2 or c == total_pages-1 or c == total_pages-2 or c == mitad or c == mitad-1:
                            pages.append(i)
                        else:
                            pages.append(None)
                        c += 1
                    print(total_pages)
                    print(c)
                    print(pages)
            else:
                pages = []
                c = 0
                for i in range(1, total_pages+1):
                    if c == 0 or c == total_pages-1 or c == page or c == page-1 or c == page-2:
                        pages.append(i)
                    else:
                        pages.append(None)
                    c += 1
                print(pages)
            last_id = starting_id[(page-1)*limit]['_id']
            estudios = tabla_estudios.find({"$and": [{criterio: campo, 'creador': session['user']}], '_id': {
                '$lte': last_id}}).sort('_id', -1).limit(limit)
        if not(estudios):
            vacio_busqueda = True
        else:
            vacio_busqueda = False
        return render_template('busqueda.html', title='Busqueda', control_center=True, estudios=estudios, css=True, pages=pages, current_page=page, vacio_busqueda=vacio_busqueda, criterio=criterio, campo=campo, count=count)
    else:
        return redirect(url_for('login'))


@app.route("/estudios_compartidos", methods=['GET', 'POST'])
def estudios_compartidos():
    if 'user' in session:
        limit = 10
        page = request.args.get('page', 1, type=int)
        starting_id = tabla_estudios.find({'$or': [{'colaboradores': session['user']}, {'$and': [
                                          {'creador': session['user']}, {'compartir': {'$exists': True}}]}]}).sort('_id', -1)
        count = tabla_estudios.count_documents({'$or': [{'colaboradores': session['user']}, {
                                               '$and': [{'creador': session['user']}, {'compartir': {'$exists': True}}]}]})
        total_pages = ceil(count / limit)
        mitad = ceil(total_pages/2)
        hola = tabla_estudios.find_one({'$or': [{'colaboradores': session['user']}, {
                                       '$and': [{'creador': session['user']}, {'compartir': {'$exists': True}}]}]})
        estudios = []
        pages = []
        if hola:
            if page == 1 or page == total_pages:
                pages = []
                c = 0
                if mitad % 2 == 0:
                    print('impar')
                    for i in range(1, total_pages+1):
                        if c < 2 or c == total_pages-1 or c == total_pages-2 or c == mitad-2 or c == mitad or c == mitad-1:
                            pages.append(i)
                        else:
                            pages.append(None)
                        c += 1
                    print(total_pages)
                    print(c)
                    print(pages)
                else:
                    print('par')
                    for i in range(1, total_pages+1):
                        if c < 2 or c == total_pages-1 or c == total_pages-2 or c == mitad or c == mitad-1:
                            pages.append(i)
                        else:
                            pages.append(None)
                        c += 1
                    print(total_pages)
                    print(c)
                    print(pages)
            else:
                pages = []
                c = 0
                for i in range(1, total_pages+1):
                    if c == 0 or c == total_pages-1 or c == page or c == page-1 or c == page-2:
                        pages.append(i)
                    else:
                        pages.append(None)
                    c += 1
                print(pages)
            last_id = starting_id[(page-1)*limit]['_id']
            estudios = tabla_estudios.find({'$or': [{'colaboradores': session['user']}, {'$and': [{'creador': session['user']}, {
                                           'compartir': {'$exists': True}}]}], '_id': {'$lte': last_id}}).sort('_id', -1).limit(limit)
        if not(estudios):
            vacio_historial = True
        else:
            vacio_historial = False
        form = Buscador2Form()
        if form.validate_on_submit():
            return redirect(url_for('busqueda_compartida', campo=form.campo.data, criterio=form.criterio.data))
        return render_template('historial_compartido.html', title='Estudios Compartidos', control_center=True, estudios=estudios, css=True, pages=pages, current_page=page, vacio_historial=vacio_historial, form=form)
    else:
        return redirect(url_for('login'))


@app.route('/busqueda_compartida/<criterio>/<campo>', methods=['GET', 'POST'])
def busqueda_compartida(criterio, campo):
    if 'user' in session:
        limit = 10
        if criterio == 'edad' or criterio == 'cedula':
            campo = int(campo)
        starting_id = tabla_estudios.find({'$or': [{'$and': [{'colaboradores': session['user']}, {criterio: campo}]}, {
                                          '$and': [{'creador': session['user']}, {'compartir': {'$exists': True}}, {criterio: campo}]}]}).sort('_id', -1)
        page = request.args.get('page', 1, type=int)
        count = tabla_estudios.count_documents({'$or': [{'$and': [{'colaboradores': session['user']}, {criterio: campo}]}, {
                                               '$and': [{'creador': session['user']}, {'compartir': {'$exists': True}}, {criterio: campo}]}]})
        total_pages = ceil(count / limit)
        mitad = ceil(total_pages/2)
        hola = tabla_estudios.find_one({'$or': [{'$and': [{'colaboradores': session['user']}, {criterio: campo}]}, {
                                       '$and': [{'creador': session['user']}, {'compartir': {'$exists': True}}, {criterio: campo}]}]})
        estudios = []
        pages = []
        print(hola)
        print(count)
        if hola:
            if page == 1 or page == total_pages:
                pages = []
                c = 0
                if mitad % 2 == 0:
                    print('impar')
                    for i in range(1, total_pages+1):
                        if c < 2 or c == total_pages-1 or c == total_pages-2 or c == mitad-2 or c == mitad or c == mitad-1:
                            pages.append(i)
                        else:
                            pages.append(None)
                        c += 1
                    print(total_pages)
                    print(c)
                    print(pages)
                else:
                    print('par')
                    for i in range(1, total_pages+1):
                        if c < 2 or c == total_pages-1 or c == total_pages-2 or c == mitad or c == mitad-1:
                            pages.append(i)
                        else:
                            pages.append(None)
                        c += 1
                    print(total_pages)
                    print(c)
                    print(pages)
            else:
                pages = []
                c = 0
                for i in range(1, total_pages+1):
                    if c == 0 or c == total_pages-1 or c == page or c == page-1 or c == page-2:
                        pages.append(i)
                    else:
                        pages.append(None)
                    c += 1
                print(pages)
            last_id = starting_id[(page-1)*limit]['_id']
            estudios = tabla_estudios.find({'$or': [{'$and': [{'colaboradores': session['user']}, {criterio: campo}]}, {'$and': [{'creador': session['user']}, {'compartir': {'$exists': True}}, {criterio: campo}]}], '_id': {
                '$lte': last_id}}).sort('_id', -1).limit(limit)
        if not(estudios):
            vacio_busqueda = True
        else:
            vacio_busqueda = False
        return render_template('busqueda_compartida.html', title='Busqueda', control_center=True, estudios=estudios, css=True, pages=pages, current_page=page, vacio_busqueda=vacio_busqueda, criterio=criterio, campo=campo, count=count)
    else:
        return redirect(url_for('login'))


@app.route('/nuevo-examen', methods=['GET', 'POST'])
def new_examen():
    if 'user' in session:
        form = ExamenForm()
        if form.validate_on_submit():
            examen = {
                'nombre': form.nombre_examen.data.upper(),
                'creador': session['user'],
                'tarifa': form.tarifa.data
            }
            tabla_examenes.insert_one(examen)
            flash('Examen creado satisfactoriamente', 'success')
        examenes = tabla_examenes.find(
            {'creador': session['user']}).sort("nombre", 1)
        form.nombre_examen.data = ''
        form.tarifa.data = 0
        return render_template('examen.html', title='Examenes', control_center=True, css=True, form=form, examenes=examenes)
    else:
        return redirect(url_for('login'))


@app.route('/nuevo-paquete', methods=['GET', 'POST'])
def new_paquete():
    if 'user' in session:
        examenes = tabla_examenes.find(
            {'creador': session['user']}).sort("nombre", 1)
        form = PaqueteForm()
        form.l_examenes.choices = [
            (examen['nombre'], examen['nombre']) for examen in examenes]
        if form.validate_on_submit():
            paquete = {
                'nombre': form.nombre_paquete.data.upper(),
                'creador': session['user'],
                'examenes': form.l_examenes.data,
                'tarifa': form.tarifa.data
            }
            tabla_paquetes.insert_one(paquete)
            flash('Paquete creado satisfactoriamente', 'success')
        form.nombre_paquete.data = ''
        return render_template('new_paquete.html', title='Paquetes', control_center=True, css=True, form=form, legend = 'Nuevo Paquete')
    else:
        return redirect(url_for('login'))


@app.route('/nueva-empresa', methods=['GET', 'POST'])
def new_empresa():
    if 'user' in session:
        examenes = tabla_examenes.find(
            {'creador': session['user']}).sort("nombre", 1)
        paquetes = tabla_paquetes.find(
            {'creador': session['user']}).sort("nombre", 1)
        form = EmpresaForm()
        form.l_paquetes.choices = [
            (paquete['nombre'], paquete['nombre']) for paquete in paquetes]
        form.l_examenes.choices = [
            (examen['nombre'], examen['nombre']) for examen in examenes]
        if form.validate_on_submit():
            empresa = {
                'nombre': form.nombre_empresa.data.upper(),
                'paquetes': form.l_paquetes.data,
                'examenes': form.l_examenes.data,
                'creador': session['user']
            }
            tabla_empresas.insert_one(empresa)
            flash('Empresa creada satisfactoriamente', 'success')
        return render_template('new_empresa.html', title='Empresa', control_center=True, css=True, form=form, legend = 'Nueva Empresa')
    else:
        return redirect(url_for('login'))


@app.route('/paquetes', methods=['GET', 'POST'])
def paquetes():
    if 'user' in session:
        paquetes = []
        busqueda = tabla_paquetes.find_one({'creador': session['user']})
        if busqueda:
            paquetes = tabla_paquetes.find({'creador': session['user']}).sort("_id", -1)
            return render_template('paquetes.html', title='Paquetes', control_center=True, css=True, paquetes=paquetes, vacio_paquetes = False)
        else:
            return render_template('paquetes.html', title='Paquetes', control_center=True, css=True, paquetes=paquetes, vacio_paquetes = True)
    else:
        return redirect(url_for('login'))


@app.route('/empresas', methods=['GET', 'POST'])
def empresas():
    if 'user' in session:
        empresas = []
        busqueda = tabla_empresas.find_one({'creador': session['user']})
        if busqueda:
            empresas = tabla_empresas.find({'creador': session['user']}).sort("_id", -1)
            return render_template('empresas.html', title='Empresas', control_center=True, css=True, empresas=empresas, vacio_empresas = False)
        else:
            return render_template('empresas.html', title='Empresas', control_center=True, css=True, empresas=empresas, vacio_empresas = True)
            
    else:
        return redirect(url_for('login'))

@app.route("/paquetes/<_id>/delete", methods=['POST'])
def borrar_paquete(_id):
    tabla_paquetes.delete_one({'_id': ObjectId(_id)})
    return redirect(url_for('paquetes'))

@app.route("/empresas/<_id>/delete", methods=['POST'])
def borrar_empresa(_id):
    tabla_empresas.delete_one({'_id': ObjectId(_id)})
    return redirect(url_for('empresas'))

@app.route("/paquetes/<_id>/update", methods=['GET', 'POST'])
def actualizar_paquete(_id):
    paquete = tabla_paquetes.find_one({'_id': ObjectId(_id)})
    examenes = tabla_examenes.find({'creador': session['user']})
    form = PaqueteForm()
    form.l_examenes.choices = [(examen['nombre'], examen['nombre']) for examen in examenes]
    if form.validate_on_submit():
        cambios = {
            'creador': session['user'],
            'nombre': form.nombre_paquete.data.upper(),
            'examenes': form.l_examenes.data,
            'tarifa': form.tarifa.data
        }
        tabla_paquetes.update_one(
            {'creador': session['user']}, {'$set': cambios})
        flash('Cambios Realizados Satisfactoriamente!', 'success')
        return redirect(url_for('paquetes'))
    elif request.method == 'GET':
        form.nombre_paquete.data = paquete['nombre']
        form.l_examenes.data = paquete['examenes']
        form.tarifa.data = paquete['tarifa']
    return render_template('new_paquete.html', title='Actualizar Paquete', control_center=True, form=form, css=True, legend = 'Actualizar Paquete')

@app.route("/empresas/<_id>/update", methods=['GET', 'POST'])
def actualizar_empresa(_id):
    empresa = tabla_empresas.find_one({'_id': ObjectId(_id)})
    form = EmpresaForm()
    examenes = tabla_examenes.find({'creador': session['user']})
    paquetes = tabla_paquetes.find({'creador': session['user']})
    form.l_examenes.choices = [(examen['nombre'], examen['nombre']) for examen in examenes]
    form.l_paquetes.choices = [(paquete['nombre'], paquete['nombre']) for paquete in paquetes]
    if form.validate_on_submit():
        cambios = {
            'creador': session['user'],
            'nombre': form.nombre_empresa.data.upper(),
            'examenes': form.l_examenes.data,
            'paquetes': form.l_paquetes.data
        }
        tabla_empresas.update_one(
            {'creador': session['user']}, {'$set': cambios})
        flash('Cambios Realizados Satisfactoriamente!', 'success')
        return redirect(url_for('empresas'))
    elif request.method == 'GET':
        form.nombre_empresa.data = empresa['nombre']
        form.l_examenes.data = empresa['examenes']
        form.l_paquetes.data = empresa['paquetes']
    return render_template('new_empresa.html', title='Actualizar Empresa', control_center=True, form=form, css=True, legend = 'Actualizar Empresa')

