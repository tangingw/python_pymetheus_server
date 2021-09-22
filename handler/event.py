from werkzeug.utils import import_string
from model.event import Event
from model.event import EventType


class EventHandler:

    def __init__(self, db_conn):

        self.event_ds = {
            "event_value": None,
            "event_message": None,
            "event_status": None,
        }

        self.db_conn = db_conn
        self.event = Event(self.db_conn)
        self.event_type = EventType(self.db_conn)

    def get_model_id(self, table_name, item_name) -> int:

        return getattr(
            import_string(
                f"model.{table_name}." + table_name[0].uppercase() + table_name[1:]
            ), f"get_{table_name}_id"
        )(item_name)

    def add_current_event(self, event_type, monitoring_type, monitoring_name, event_data):

        for key in event_data.keys():

            self.event_ds[key] = event_data.get(key)

        self.event_type.add_event_type(event_type)
        self.event.add_event(
            event_type, monitoring_type,
            self.get_model_id(monitoring_type, monitoring_name),
            self.event_ds
        )