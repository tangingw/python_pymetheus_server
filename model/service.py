

class Service:

    def __init__(self, connection):

        self.connection = connection
        self.cursor = self.connection.cursor(buffered=True)

    def add_service(self, port_num, service_data):
        self.cursor.execute(
                f"""
                insert into service(
                    name, service_desc, 
                    device_id, network_ip_id,
                    port_id, service_url, service_type,
                    created_at, updated_at
                )
                select 
                    %(service_name)s, %(service_desc)s, 
                    device_id, network_ip_id, id,
                    %(service_url)s, %(service_type)s
                    now()::timestamp, now()::timestamp
                from port
                where deleted_at is null
                and port = %(port_num)s
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
            from service where
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
    
    def delete_network(self, service_name):

        self.cursor.execute(
            f"""
            update service set deleted_at = (now()::timestamp)
            where service_name = %(service_name)s;
            """, {"service_name": service_name}
        )

        self.cursor.commit()
