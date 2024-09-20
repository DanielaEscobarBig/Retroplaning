from .entities.Event import Event
class ModelEvent():



    # Metodo almacenar eventos Lider   
    @classmethod
    def Traer_Event_Lider(self, db, areas):
        try:
            # Verificar el tipo de 'areas' para asegurarse de que es una lista de diccionarios
            if not isinstance(areas, list):
                raise ValueError("'areas' no es una lista.")
            
            if not all(isinstance(area, dict) for area in areas):
                raise ValueError("Cada elemento en 'areas' debería ser un diccionario.")

            # Extraer los event_pro_id de las áreas que tienen esa clave
            event_ids = [area['events_pro_id'] for area in areas if 'events_pro_id' in area]

            if not event_ids:
                return []

            # Crear un string con los IDs separados por comas
            ids_string = ','.join(map(str, event_ids))
            sql = f"SELECT events_pro_id, name_events_pro, status_events_pro, project_id, creation_date, update_date FROM events_pro WHERE events_pro_id IN ({ids_string})"

            cursor = db.connection.cursor()
            cursor.execute(sql)
            datos = cursor.fetchall()

            eventos = []
            for fila in datos:
                evento = {
                    'events_pro_id': fila[0], 'name_events_pro': fila[1], 
                    'status_events_pro': fila[2], 'project_id': fila[3],
                    'creation_date': fila[4], 'update_date': fila[5]
                }
                eventos.append(evento)

            return eventos
                             
        except Exception as ex:
            raise Exception(ex)
        
