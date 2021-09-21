<<<<<<< HEAD
from model.network import Network
from model.device import Device
=======
>>>>>>> 8a15613127432a44475a4d59a00acd799f8bc1de
from template import DBCursor


class DeviceNetwork(DBCursor):

    def __init__(self, connection):

        super().__init__(connection=connection)

<<<<<<< HEAD
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
=======
    def add_device_network(self, device_id, network_id):
        self.cursor.execute(
                f"""
                insert into monitoring.device_network(
                    service_id, device_id
                )
                values (
                    %(service_id)s, %(network_id)s
                ) on conflict (service_id, device_id) do nothing
                """, {
                    "device_id": device_id,
                    "network_id": network_id
>>>>>>> 8a15613127432a44475a4d59a00acd799f8bc1de
                }
            )
    
        self.cursor.commit()

<<<<<<< HEAD
    def delete_device_network(self, ip_address, device_name):
=======
    def delete_service(self, service_name, ip_address):
>>>>>>> 8a15613127432a44475a4d59a00acd799f8bc1de

        self.cursor.execute(
            f"""
            update monitoring.network_service set deleted_at = (now()::timestamp)
            where 
<<<<<<< HEAD
                device_id = %(device_id)s
            and network_id = %(network_id)s 
            and deleted_at is null;
            """, {
                "device_id": self.device.get_device_id(device_name)["id"],
=======
                service_id = %(service_id)s
            and network_id = %(network_id)s 
            and deleted_at is null;
            """, {
                "service_id": self.service.get_service_id(service_name)["id"],
>>>>>>> 8a15613127432a44475a4d59a00acd799f8bc1de
                "network_id": self.network.get_network_id(ip_address)["id"]
            }
        )

        self.cursor.commit()
    