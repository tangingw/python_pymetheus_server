from model.network import Network
from model.interface import Interface
from model.template import DBCursor


class NetworkInterface(DBCursor):

    def __init__(self, connection):

        super().__init__(connection=connection)

    def add_network_interface(self, network_id, interface_id):

        self.cursor.execute(
            f"""
            insert into monitoring.network_interface(
                network_id, interface_id,
                created_at, updated_at
            )
            select
                %(network_id)s, %(interface_id)s,
                now()::timestamp, now()::timestamp
            where not exists(
                select
                    id
                from monitoring.network_interface
                where deleted_at is null
                and network_id = %(network_id)s
                and interface_id = %(interface_id)s
            )
            """, {
                "interface_id": interface_id,
                "network_id": network_id                
            }
        )
        
        self.connection.commit()

    def get_network_interface_id(self, network_id, interface_id):

        self.cursor.execute(
            f"""
            select
                id
            from monitoring.network_interface
            where deleted_at is null
            and network_id = %(network_id)s
            and interface_id = %(interface_id)s
            """, {
                "interface_id": interface_id,
                "network_id": network_id
            }
        )
    
        header = [x[0] for x in self.cursor.description]
        result = self.cursor.fetchone()

        return {
            header[i]: r for i, r in enumerate(result) 
        } if result else None

    def delete_interface(self, network_id, interface_id):

        self.cursor.execute(
            f"""
            update monitoring.network_interface set deleted_at = (now()::timestamp)
            where 
                interface_id = %(interface_id)s
            and network_id = %(network_id)s 
            and deleted_at is null;
            """, {
                "interface_id": interface_id,
                "network_id": network_id
            }
        )

        self.connection.commit()
    