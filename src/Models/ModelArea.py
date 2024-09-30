from .entities.Area import Area


class ModelArea():

    # Metodo almacenar las areas del usuario Lider
    @classmethod
    def Traer_Areas_Lider (self, db, current_user):
        try:
            if current_user.role_id == 3: 

                cursor = db.connection.cursor()
                sql = "SELECT area_id,  status_area, assigned_date,delivery_date, events_pro_id, creation_date, update_date, name_area, user_id,orden FROM areas WHERE user_id = '{}'" .format(current_user.user_id)
                cursor.execute(sql)
                datos = cursor.fetchall()
                areas = []
                for fila in datos:
                    area = {'area_id': fila[0], 'status_area': fila[1], 'assigned_date': fila[2], 'delivery_date': fila[3], 'events_pro_id': fila[4], 'creation_date': fila[5], 'update_date': fila[6], 'name_area': fila[7], 'user_id': fila[8], 'orden': fila[9]}
                    areas.append(area)
                    
                return areas
            else: 
                if current_user.role_id == 1: 

                    cursor = db.connection.cursor()
                    sql = "SELECT area_id,  status_area, assigned_date,delivery_date, events_pro_id, creation_date, update_date, name_area, user_id,orden FROM areas " 
                    cursor.execute(sql)
                    datos = cursor.fetchall()
                    areas = []
                    for fila in datos:
                        area = {'area_id': fila[0], 'status_area': fila[1], 'assigned_date': fila[2], 'delivery_date': fila[3], 'events_pro_id': fila[4], 'creation_date': fila[5], 'update_date': fila[6], 'name_area': fila[7], 'user_id': fila[8], 'orden': fila[9]}
                        areas.append(area)
                        
                    return areas
 
                
        except Exception as ex:
            return "Error : False"
