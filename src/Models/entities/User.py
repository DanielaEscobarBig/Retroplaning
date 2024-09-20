from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin

class User(UserMixin):
    def __init__ (self,user_id, name_user, status_user, e_mail,password_user, role_id, creation_date, update_date  ) -> None:
        self.user_id = user_id
        self.name_user = name_user
        self.status_user = status_user
        self.e_mail = e_mail
        self.password_user = password_user
        self.role_id = role_id
        self.creation_date = creation_date
        self.update_date = update_date
    @classmethod
    def check_password (self, hashed_password, password_user):
        return check_password_hash (hashed_password, password_user) 
    
    def get_id(self):
           return (self.user_id)
    
    #print (generate_password_hash("4321"))

