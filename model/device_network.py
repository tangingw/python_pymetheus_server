from template import DBCursor


class DeviceNetwork(DBCursor):

    def __init__(self, connection):

        super().__init__(connection=connection)

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
                }
            )
    
        self.cursor.commit()

    def delete_service(self, service_name, ip_address):

        self.cursor.execute(
            f"""
            update monitoring.network_service set deleted_at = (now()::timestamp)
            where 
                service_id = %(service_id)s
            and network_id = %(network_id)s 
            and deleted_at is null;
            """, {
                "service_id": self.service.get_service_id(service_name)["id"],
                "network_id": self.network.get_network_id(ip_address)["id"]
            }
        )

        self.cursor.commit()
    