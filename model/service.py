from model.template import DBCursor
from model.port import Port

class Service(DBCursor):

    def __init__(self, connection):

        super().__init__(connection=connection)
        self.service_type = ServiceType(self.connection)
        self.port = Port(self.connection)

    def add_service(self, service_data):
        
        self.service_type.add_service_type(service_data["service_type"])

        self.cursor.execute(
                f"""
                insert into monitoring.service(
                    name, service_desc, 
                    port_id, service_url, service_type_id,
                    created_at, updated_at
                )
                select 
                    %(service_name)s, %(service_desc)s, 
                    %(service_port)s, %(service_url)s, s.id,
                    (now() at time zone 'utc')::timestamp, 
                    (now() at time zone 'utc')::timestamp
                from monitoring.service_type s
                where s.service_type = %(service_type)s
                and not exists (
                    select 
                        id 
                    from monitoring.service
                    where name = %(service_name)s
                    and deleted_at is null 
                )
                """, {
                    "service_name": service_data["service_name"],
                    "service_desc": service_data["service_desc"],
                    "service_url": service_data["service_url"],
                    "service_type": service_data["service_type"],
                    "service_port": self.port.get_port_id(service_data["service_port"])["id"]
                }
            )
        
        self.connection.commit()

    def get_service_id(self, service_name):

        self.cursor.execute(
            f"""
            select 
                id 
            from monitoring.service
            where name = %(service_name)s
            and deleted_at is null
            """, {
                "service_name": service_name
            }
        )

        header = [x[0] for x in self.cursor.description]
        result = self.cursor.fetchone()

        return {
            header[i]: r for i, r in enumerate(result) 
        } if result else None
    
    def delete_service(self, service_name):

        self.cursor.execute(
            f"""
            update monitoring.service set deleted_at = ((now() at time zone 'utc')::timestamp)
            where service_name = %(service_name)s and deleted_at is null;
            """, {"service_name": service_name}
        )

        self.connection.commit()

class ServiceType(DBCursor):

    def __init__(self, connection):

        super().__init__(connection=connection)
    
    def add_service_type(self, service_type):

        self.cursor.execute(
            f"""
            insert into monitoring.service_type(service_type)
            select %(service_type)s
            where not exists(
                select 
                    id 
                from monitoring.service_type
                where service_type = %(service_type)s
            )
            """, {
                "service_type": service_type
            }
        )

        self.connection.commit()
    
    def get_servicetype_id(self, service_type):

        self.cursor.execute(
            f"""
            select 
                id 
            from monitoring.service_type
            where service_type = %(service_name)s
            and deleted_at is null
            """, {
                "service_name": service_type
            }
        )

        header = [x[0] for x in self.cursor.description]
        result = self.cursor.fetchone()

        return {
            header[i]: r for i, r in enumerate(result) 
        } if result else None
