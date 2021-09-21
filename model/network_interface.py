from model.network import Network
from model.interface import Interface
from template import DBCursor


class NetworkInterface(DBCursor):

    def __init__(self, connection):

        super().__init__(connection=connection)

        self.interface = Interface(self.connection)
        self.network = Network(self.connection)

    def add_network_interface(self, ip_address, mac_address):
        self.cursor.execute(
                f"""
                insert into monitoring.network_interface(
                    network_id, interface_id,
                    created_at, updated_at,
                )
                values (
                    %(network_id)s, %(interface_id)s
                    now()::timestamp, now()::timestamp
                ) on conflict (network_id, interface_id) do nothing
                """, {
                    "interface_id": self.interface.get_interface_id(mac_address)["id"],
                    "network_id": self.network.get_network_id(ip_address)["id"]
                }
            )
    
        self.cursor.commit()

    def delete_service(self, mac_address, ip_address):

        self.cursor.execute(
            f"""
            update monitoring.network_service set deleted_at = (now()::timestamp)
            where 
                interface_id = %(interface_id)s
            and network_id = %(network_id)s 
            and deleted_at is null;
            """, {
                "interface_id": self.service.get_interface_id(mac_address)["id"],
                "network_id": self.network.get_network_id(ip_address)["id"]
            }
        )

        self.cursor.commit()
    