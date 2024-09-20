class Area():
    def __init__ (self,area_id,  status_area, assigned_date,delivery_date, events_pro_id, creation_date, update_date, area_type_id, user_id,orden ) -> None:
        self.area_id = area_id
        self.status_area = status_area
        self.assigned_date = assigned_date
        self.delivery_date = delivery_date
        self.events_pro_id = events_pro_id
        self.creation_date = creation_date
        self.update_date = update_date
        self.area_type_id = area_type_id
        self.user_id = user_id
        self.orden = orden
        
    
    def get_id(self):
           return (self.area_id)
