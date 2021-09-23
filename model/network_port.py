from model.template import DBCursor


class NetworkPort(DBCursor):

    def __init__(self, connection):

        super().__init__(connection=connection)

    def add_network_port(self, network_id, port_id):

        self.cursor.execute(
            f"""
            insert into monitoring.network_port(
                port_id, network_id
                created_at, updated_at
            )
            select 
                %(port_id)s, %(network_id)s,
                (now() at time zone 'utc')::timestamp,
                (now() at time zone 'utc')::timestamp
            where not exists (
                select
                    id
                from monitoring.network_port
                where deleted_at is null
                and network_id = %(network_id)s
                and interface_id = %(port_id)s
            )
            """, {
                "port_id": port_id,
                "network_id": network_id
            }
        )
        
        self.connection.commit()
        
    def get_network_port_id(self, network_id, port_id):

        self.cursor.execute(
            f"""
            select
                id
            from monitoring.network_port
            where deleted_at is null
            and network_id = %(network_id)s
            and interface_id = %(port_id)s
            """, {
                "interface_id": port_id,
                "network_id": network_id
            }
        )
    
        header = [x[0] for x in self.cursor.description]
        result = self.cursor.fetchone()

        return {
            header[i]: r for i, r in enumerate(result) 
        } if result else None

    def delete_port(self, port_num, ip_address):

        self.cursor.execute(
            f"""
            update monitoring.network_port set deleted_at = ((now() at time zone 'utc')::timestamp)
            where port_id = %(port_id)s
            and network_id = %(network_id)s
            and deleted_at is null;
            """, {
                "port_id": self.port.get_port_id(port_num)["id"],
                "network_id": self.network.get_network_id(ip_address)["id"]
            }
        )

        self.connection.commit()