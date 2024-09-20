from flask import Flask, redirect, render_template, request, url_for, flash , jsonify
from flask_mysqldb import MySQL

from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from config import config
""" Import Modelos"""
from Models.ModelUser import ModelUser
from Models.ModelProject import ModelProject
from Models.ModelArea import ModelArea
from Models.ModelEvent import ModelEvent
from Models.ModelCliente import ModelCliente

""" Import Entities"""
from Models.entities.User import User
from Models.entities.Cliente import Cliente
from Models.entities.Area import Area
from Models.entities.Project import Project
from Models.entities.Event import Event

app = Flask (__name__)

csrf = CSRFProtect()
db = MySQL(app)
login_manager_app = LoginManager(app)

@login_manager_app.user_loader
def load_user(user_id):
    
    return ModelUser.get_by_id(db, user_id)





@app.route('/')
def index():
    return redirect (url_for('login'))


@app.route('/login', methods=['GET','POST'])
def login():

    if request.method == 'POST':
        
        user = User(0,"", "",request.form['e_mail'], request.form['password_user'], "", "" ,"")
        
        logged_user = ModelUser.login(db, user)
        if logged_user != None:
            if logged_user.password_user:
                login_user(logged_user)
                print(current_user.user_id)
                return redirect(url_for('protected'))
            else:
                flash("Invalid password...")
                return render_template('login.html')
        else:
            flash("User not found...")
            return render_template ('login.html')
    else: 
        return render_template ('login.html')              

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))





@app.route('/protected')
@login_required
def protected():
    # Obtener las áreas del líder
    areas = ModelArea.Traer_Areas_Lider(db, current_user)

    if areas:
        # Obtener los eventos relacionados con las áreas
        eventos = ModelEvent.Traer_Event_Lider(db, areas)

        if eventos:
            # Obtener los proyectos relacionados con los eventos
            proyectos = ModelProject.get_proyectos_por_usuario(db, eventos)

            if proyectos:
                # Obtener los clientes relacionados con los proyectos
                clientes = ModelCliente.get_clientes_por_proyecto(db, proyectos)

                if clientes:
                    # Agrupar áreas dentro de los eventos
                    eventos_con_areas = {}
                    for evento in eventos:
                        evento_id = evento['events_pro_id']
                        # Filtrar las áreas que pertenecen a este evento
                        areas_del_evento = [area for area in areas if area['events_pro_id'] == evento_id]
                        evento['areas'] = areas_del_evento  # Añadir las áreas al evento
                        eventos_con_areas[evento_id] = evento
                    
                    # Agrupar los eventos dentro de los proyectos
                    proyectos_con_eventos = {}
                    for proyecto in proyectos:
                        proyecto_id = proyecto['project_id']
                        # Filtrar los eventos que pertenecen a este proyecto
                        eventos_del_proyecto = [evento for evento in eventos if evento['project_id'] == proyecto_id]
                        proyecto['eventos'] = eventos_del_proyecto  # Añadir los eventos al proyecto
                        proyectos_con_eventos[proyecto_id] = proyecto

                    # Agrupar los proyectos dentro de los clientes
                    clientes_con_proyectos = {}
                    for cliente in clientes:
                        client_id = cliente['client_id']
                        # Filtrar los proyectos que pertenecen a este cliente
                        proyectos_del_cliente = [proyecto for proyecto in proyectos if proyecto['client_id'] == client_id]
                        cliente['proyectos'] = proyectos_del_cliente  # Añadir los proyectos al cliente
                        clientes_con_proyectos[client_id] = cliente  # Utilizar client_id como clave

                    # Enviar la estructura jerárquica a la vista
                    return render_template('protected.html', clientes=clientes_con_proyectos)
                else:
                    return render_template('error.html', mensaje="Error al obtener los clientes.")
            else:
                return render_template('error.html', mensaje="Error al obtener los proyectos.")
        else:
            return render_template('error.html', mensaje="Error al obtener los eventos.")
    else:
        return render_template('error.html', mensaje="Error al obtener las áreas.")
    

@app.route('/admin_view', methods=['GET', 'POST'])
@login_required
def admin_view():
      
    if current_user.role_id != 1:
        flash("Acceso denegado. Solo los administradores pueden acceder.")
        return redirect(url_for('protected'))

    if request.method == 'POST':
        # Procesar la creación o modificación de los elementos aquí
        # Obtener datos del formulario
        tipo_elemento = request.form.get('tipo_elemento')

        if tipo_elemento == "cliente":
            # Crear o modificar cliente
            cliente_id = request.form.get('cliente_id')
            nombre_cliente = request.form.get('nombre_cliente')
            nit = request.form.get('nit')
            status_cli = request.form.get('status_cli')
            # Lógica para crear o actualizar el cliente
        elif tipo_elemento == "usuario":
            # Crear o modificar usuario
            user_id = request.form.get('user_id')
            nombre_usuario = request.form.get('nombre_usuario')
            email = request.form.get('email')
            role_id = request.form.get('role_id')
            # Lógica para crear o actualizar el usuario
        
        flash('Elemento procesado correctamente')
        return redirect(url_for('admin_view'))
    
    # Si es una solicitud GET, mostrar el formulario vacío
    return render_template('admin_view.html')
    
        

def new_func():
    return User
    


def status_401(error):
    return redirect(url_for('login'))


def status_404(error):
    return "<h1>Página no encontrada</h1>", 404


if __name__ == '__main__':
    app.config.from_object(config['development'])
    csrf.init_app(app)
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)
    app.run()


if __name__ == '__main__':
    app.run(debug = True, port=4000) 
