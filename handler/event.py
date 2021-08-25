from werkzeug.utils import import_string
from model.event import Event


class EventHandler:

    def __init__(self):

        self.event_ds = {
            "event_value": None,
            "event_message": None,
            "event_status": None,
        }

        self.event = Event()
    
    def get_model_id(self, table_name, item_name) -> int:

        return getattr(
            import_string(
                f"model.{table_name}." + table_name[0].uppercase() + table_name[1:]),
            f"get_{table_name}_id"
        )(item_name)

    def add_current_event(self, event_data):

        for key in event_data.keys():

            self.event_ds[key] = event_data.get(key)
        
        #How to get the fk_id?
        self.event.add_event(
            event_data["monitoring_type"], event_data["item_monitored"]["item_type"],
            self.get_model_id(
                event_data["item_monitored"]["item_type"], 
                event_data["item_monitored"]["item_name"]
            ),
            self.event_ds
        )