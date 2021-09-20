from template import DBCursor


class Service(DBCursor):

    def __init__(self, connection):

        super().__init__(connection=connection)

    def add_service(self, port_num, service_data):
        self.cursor.execute(
                f"""
                insert into monitoring.service(
                    name, service_desc, 
                    port_id, service_url, service_type_id,
                    created_at, updated_at
                )
                select 
                    %(service_name)s, %(service_desc)s, 
                    p.id, %(service_url)s, s.id,
                    now()::timestamp, now()::timestamp
                from monitoring.port p join service_type s
                on p.service_type_id = s.id
                where p.deleted_at is null
                and p.port = %(port_num)s
                and s.service_type = %(service_type)s
                on conflict(service_url, name) do nothing
                """, {
                    "service_name": service_data["service_name"],
                    "service_desc": service_data["service_desc"],
                    "service_url": service_data["service_url"],
                    "service_type": service_data["service_type"],
                    "port_num": port_num
                }
            )
        
        self.cursor.commit()

    def get_service_id(self, service_name):

        self.cursor.execute(
            f"""
            select 
                id 
            from monitoring.service where
            where service_name = %(service_name)s
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
            update monitoring.service set deleted_at = (now()::timestamp)
            where service_name = %(service_name)s and deleted_at is null;
            """, {"service_name": service_name}
        )

        self.cursor.commit()


class ServiceType(DBCursor):

    def __init__(self, connection):

        super().__init__(connection=connection)
    
    def add_service(self, service_type):

        self.cursor.execute(
            f"""
            insert into service_type(service_type)
            values (%(service_type)s)
            """, {
                "service_type": service_type
            }
        )

        self.cursor.commit()
    
    def get_servicetype_id(self, service_type):

        self.cursor.execute(
            f"""
            select 
                id 
            from monitoring.service_type where
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
