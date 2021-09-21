from template import DBCursor


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
            values (
                %(port_id)s, %(network_id)s
            )
            on conflict(port_id, network_id) do nothing
            """, {
                "port_id": port_id,
                "network_id": network_id
            }
        )
        
        self.cursor.commit()
    
    def delete_port(self, port_num, ip_address):

        self.cursor.execute(
            f"""
            update monitoring.network_port set deleted_at = (now()::timestamp)
            where port_id = %(port_id)s
            and network_id = %(network_id)s
            and deleted_at is null;
            """, {
                "port_id": self.port.get_port_id(port_num)["id"],
                "network_id": self.network.get_network_id(ip_address)["id"]
            }
        )

        self.cursor.commit()