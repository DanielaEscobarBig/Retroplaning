from .entities.Cliente import Cliente

class ModelCliente():


    @classmethod
    def get_clientes_por_proyecto(self, db, proyectos):
        try:
            # Extraer los IDs de los proyectos
            project_ids = [proyecto['project_id'] for proyecto in proyectos]
            
            if not project_ids:
                return []

            # Crear un string con los IDs de proyectos separados por comas
            ids_string = ','.join([str(proj_id) for proj_id in project_ids])
            sql = f"SELECT client_id, name_cli, status_cli, nit, creation_date, update_date FROM clients WHERE client_id IN (SELECT client_id FROM projects WHERE project_id IN ({ids_string}))"

            cursor = db.connection.cursor()
            cursor.execute(sql)
            datos = cursor.fetchall()

            clientes = []
            for fila in datos:
                cliente = {
                    'client_id': fila[0], 
                    'name_cli': fila[1], 
                    'status_cli': fila[2], 
                    'nit': fila[3],
                    'creation_date': fila[4],
                    'update_date': fila[5]
                }
                clientes.append(cliente)

            return clientes

        except Exception as ex:
            raise Exception(f"Error al obtener los clientes: {str(ex)}")