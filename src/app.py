from flask import Flask, redirect, render_template, request, url_for, flash , jsonify, session
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
                    
                    session['clientes'] = clientes
                        

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




@app.route('/admin_view')
def admin_view():
    lista_clientes = ModelUser.obtener_cliente_por_id(db)  
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
                    
                    session['clientes'] = clientes
                        

                    # Enviar la estructura jerárquica a la vista
                    return render_template('admin_view.html', lista_clientes=lista_clientes, clientes=clientes_con_proyectos)
                else:
                    return render_template('error.html', mensaje="Error al obtener los clientes.")
            else:
                return render_template('error.html', mensaje="Error al obtener los proyectos.")
        else:
            return render_template('error.html', mensaje="Error al obtener los eventos.")
    else:
        return render_template('error.html', mensaje="Error al obtener las áreas.")
    

@app.route('/admin_crear')
def admin_crear():
    return render_template('admin_crear.html')


@app.route('/formulario_modificar_proyecto/<int:id_project>', methods=['GET', 'POST'])
def formulario_modificar_proyecto(id_project):

    proyecto = ModelProject.obtener_proyectos_para_admin(db,id_project)

    if request.method == 'POST':
        nombre_proyecto = request.form['name_project']
        estado_proyecto = request.form['status_project'] 
        client_id = request.form['client_id']
        user_id = request.form['user_id']
       
        ModelProject.actualizar_proyecto(id_project, nombre_proyecto, estado_proyecto, user_id, client_id)


    # Mostramos el formulario con los datos actuales del proyecto
    return render_template('formulario_modificar_proyecto.html', proyecto=proyecto)



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
