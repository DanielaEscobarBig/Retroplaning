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

            proyectos = []
            for fila in datos:
                proyecto = {
                    'project_id': fila[0], 'name_project': fila[1], 
                    'status_project': fila[2], 
                    'user_id': fila[3], 'client_id': fila[4], 
                    'creation_date': fila[5], 'update_date': fila[6]
                }
                proyectos.append(proyecto)

            return proyectos

        except Exception as ex:
            raise Exception(ex)
            