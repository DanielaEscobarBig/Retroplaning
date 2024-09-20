class Event():
    def __init__ (self,events_pro_id, name_events_pro, status_events_pro, project_id, creation_date, update_date  ) -> None:
        self.events_pro_id = events_pro_id
        self.name_events_pro = name_events_pro
        self.status_events_pro = status_events_pro
        self.project_id = project_id
        self.creation_date = creation_date
        self.update_date = update_date

    
    def get_id(self):
           return (self.events_pro_id)





