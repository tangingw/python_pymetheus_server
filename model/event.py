from model.template import DBCursor


class Event(DBCursor):

    def __init__(self, connection):

        super().__init__(connection=connection)

    def add_event(self, event_type, monitoring_type, monitoring_type_id, event_data):
        self.cursor.execute(
            f"""
            insert into monitoring.monitor_event(
                event_value, event_message,
                event_status, event_type_id, monitor_type,
                monitor_type_id,
                created_at
            )
            select 
                %(event_value)s, %(event_message)s,
                %(event_status)s, %(monitoring_type)s, 
                %(monitoring_type_id)s, id,
                now()::timestamp
            from monitoring.event_type
            where type_name = %(event_type)s
            """, {
                "event_value": event_data["event_value"],
                "event_message": event_data["event_message"],
                "event_status": event_data["event_status"],
                "monitoring_type": monitoring_type, #foreign_key_table_name, 
                "monitoring_type_id": monitoring_type_id, #foreign_key_id
                "event_type": event_type
            }
        )
        
        self.connection.commit()

    def get_event(self, monitoring_type, monitoring_type_id):

        self.cursor.execute(
            f"""
            select 
                m.event_value, m.event_message, m.event_status,
                e.type_name, m.monitoring_type, 
                m.monitoring_type_id
            from 
                monitoring.monitoring_event m 
            join 
                monitoring.event_type e 
            on m.event_type_id = e.id 
            where m.event_type = %(fk_table)s
            and m.monitoring_type_id = %(fk_id)s
            and deleted_at is null
            """, {
                "fk_table": monitoring_type,
                "fk_id": monitoring_type_id
            }
        )

        header = [x[0] for x in self.cursor.description]
        result_list = self.cursor.fetchall()

        return [
            {
                header[i]: r for i, r in enumerate(result) 
            }   for result in result_list
        ] if result_list else None


class EventType(DBCursor):

    def __init__(self, connection):

        super().__init__(connection=connection)
    
    def add_event_type(self, event_type):

        self.cursor.execute(
            f"""
            insert into monitoring.event_type(type_name)
            select 
                %(event_type)s
            where not exists (
                select 
                    id 
                from monitoring.event_type where
                where type_name = %(monitor_type)s
                and deleted_at is null
            )
            """, {
                "event_type": event_type
            }
        )

        self.connection.commit()
    
    def get_monitor_type_id(self, monitor_type):

        self.cursor.execute(
            f"""
            select 
                id 
            from monitoring.event_type where
            where type_name = %(monitor_type)s
            and deleted_at is null
            """, {
                "monitor_type": monitor_type
            }
        )

        header = [x[0] for x in self.cursor.description]
        result = self.cursor.fetchone()

        return {
            header[i]: r for i, r in enumerate(result) 
        } if result else None
