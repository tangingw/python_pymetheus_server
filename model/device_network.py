from model.network import Network
from model.device import Device
from template import DBCursor


class DeviceNetwork(DBCursor):

    def __init__(self, connection):

        super().__init__(connection=connection)

        self.device = Device(self.connection)
        self.network = Network(self.connection)

    def add_device_network(self, ip_address, device_name):
        self.cursor.execute(
                f"""
                insert into monitoring.device_network(
                    device_id, network_id,
                    created_at, updated_at
                )
                values (
                    %(device_id)s, %(network_id)s,
                    now()::timestamp, now()::timestamp
                ) on conflict (service_id, device_id) do nothing
                """, {
                    "device_id": self.service.get_service_id(device_name)["id"],
                    "network_id": self.network.get_network_id(ip_address)["id"]
                }
            )
    
        self.cursor.commit()

    def delete_device_network(self, ip_address, device_name):

        self.cursor.execute(
            f"""
            update monitoring.network_service set deleted_at = (now()::timestamp)
            where 
                device_id = %(device_id)s
            and network_id = %(network_id)s 
            and deleted_at is null;
            """, {
                "device_id": self.device.get_device_id(device_name)["id"],
                "network_id": self.network.get_network_id(ip_address)["id"]
            }
        )

        self.cursor.commit()
    