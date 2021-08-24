

class Event:

    def __init__(self, connection):

        self.connection = connection
        self.cursor = self.connection.cursor(buffered=True)

    def add_event(self, monitoring_type, foreign_key_table_name, foreign_key_id, event_data):
        self.cursor.execute(
                f"""
                insert into monitoring.monitor_event(
                    event_value, event_message,
                    event_status, fk_table, fk_id,
                    monitor_type_id,
                    created_at
                )
                select 
                    %(event_value)s, %(event_message)s,
                    %(event_status)s, %(fk_table)s, 
                    %(fk_id)s, id,
                    now()::timestamp
                from monitoring.monitor_type
                where type_name = %(monitoring_type)s
                """, {
                    "event_value": event_data["event_value"],
                    "event_message": event_data["event_message"],
                    "event_status": event_data["event_status"],
                    "fk_table": foreign_key_table_name, 
                    "fk_id": foreign_key_id,
                    "monitoring_type": monitoring_type
                }
            )
        
        self.cursor.commit()

    def get_event(self, foreign_key_table_name, foreign_key_id):

        self.cursor.execute(
            f"""
            select 
                event_value, event_message, event_status,
                monitor_type_id
            from monitoring.monitoring_event where
            where fk_table = %(fk_table)s
            and fk_id = %(fk_id)s
            and deleted_at is null
            """, {
                "fk_table": foreign_key_table_name,
                "fk_id": foreign_key_id
            }
        )

        header = [x[0] for x in self.cursor.description]
        result_list = self.cursor.fetchall()

        return [
            {
                header[i]: r for i, r in enumerate(result) 
            }   for result in result_list
        ] if result_list else None
