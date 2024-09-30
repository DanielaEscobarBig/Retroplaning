from .entities.Project import Project


class ModelProject():
    @classmethod
    def get_proyectos_por_usuario(self, db, eventos):   
    
        try:
            # Extraer los project_id de los eventos
            project_ids = [str(evento['project_id']) for evento in eventos]

            if not project_ids:
                return []
            
            

            # Crear un string con los IDs separados por comas
            ids_string = ','.join(project_ids)
            
            sql = f"SELECT project_id, name_project, status_project, user_id,client_id, creation_date, update_date FROM projects WHERE project_id IN ({ids_string})"

            cursor = db.connection.cursor()
            cursor.execute(sql)  # Ya no es necesario pasar parámetros
            datos = cursor.fetchall()
            

            user_ids = [str(user[3]) for user in datos]

            if not user_ids:
                return []
            
            uids_user = ','.join(user_ids)

            
            

            consulta_usuario = f"SELECT user_id, name_user  FROM users WHERE user_id IN ({uids_user})"
            cursor = db.connection.cursor()
            cursor.execute(consulta_usuario)  
            datos_usuario = cursor.fetchall()
            

            proyectos = []
            for fila in datos:
                proyecto = {
                    'project_id': fila[0], 'name_project': fila[1], 
                    'status_project': fila[2], 
                    'user_id': fila[3], 'client_id': fila[4], 
                    'creation_date': fila[5], 'update_date': fila[6]

                }
            
                for item in datos_usuario:
                    if proyecto['user_id'] == item[0]:
                        proyecto['name_user'] = item[1]  # name_user
                    
                
                    




                proyectos.append(proyecto)
            

            return proyectos
        except Exception as ex:
            raise Exception(ex)
        
    @staticmethod
    def obtener_proyectos_para_admin(db, project_id):
        cursor = db.connection.cursor()
        sql = f"SELECT project_id, name_project, status_project, user_id,client_id, creation_date, update_date FROM projects WHERE project_id IN ({project_id})"
        cursor.execute(sql)
        proyectos = cursor.fetchall()
        for fila in proyectos:
            proyecto = {
                    'project_id': fila[0], 'name_project': fila[1], 
                    'status_project': fila[2], 
                    'user_id': fila[3], 'client_id': fila[4], 
                    'creation_date': fila[5], 'update_date': fila[6]

                }
            return proyecto 

    @classmethod
    def actualizar_proyecto(db, id_project, nombre_proyecto, estado_proyecto, user_id, client_id):
    # Crear consulta SQL para actualizar el proyecto
        cursor = db.connection.cursor()
        sql = """ UPDATE projects 
        SET name_project = %s, status_project = %s, user_id = %s, client_id = %s, update_date = NOW()
        WHERE project_id = %s
    """
        
        
        valores = (nombre_proyecto, estado_proyecto, user_id, client_id, id_project)

        try:
            # Ejecutar la consulta
            cursor.execute(sql, valores)
            db.commit()
            
            

        except Exception as error:
            print(f"Error al actualizar el proyecto: {error}")
            db.rollback()  # Revertir los cambios en caso de error

        
            