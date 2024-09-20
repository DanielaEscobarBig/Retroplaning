class Project():
    def __init__ (self,project_id, name_project, status_project, user_id,client_id, creation_date, update_date  ) -> None:
        self.project_id = project_id
        self.name_project = name_project
        self.status_project = status_project
        self.user_id = user_id
        self.client_id = client_id
        self.creation_date = creation_date
        self.update_date = update_date
  

    
    def get_id(self):
           return (self.project_id)


