from .entities.User import User


class ModelUser():

    @classmethod
    # metodo de logueo
    def login(self, db,user):
        try:
            cursor = db.connection.cursor()
            
            sql= "SELECT user_id, name_user, status_user, e_mail,password_user, role_id, creation_date, update_date  FROM users WHERE e_mail = '{}'  AND status_user = '1' ".format(user.e_mail)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                
                user = User (row[0], row[1],row[2],row[3],User.check_password(row[4], user.password_user),row[5],row[6],row[7])
                
                return user
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
            
    # Metodo almacenar datos de usuario logueado    
    @classmethod
    def get_by_id(self, db, user_id):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT user_id, name_user, status_user, e_mail,password_user, role_id, creation_date, update_date  FROM users WHERE user_id = '{}'".format(user_id)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:

                
                return User(row[0], row[1],row[2],row[3],None,row[5],row[6],row[7])
            
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
        

    
    @staticmethod
    def obtener_cliente_por_id(db):
        cursor = db.connection.cursor()
        sql = "SELECT client_id, name_cli, status_cli, nit, creation_date, update_date FROM clients"
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
    



