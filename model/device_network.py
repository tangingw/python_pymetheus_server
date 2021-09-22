
from model.template import DBCursor


class DeviceNetwork(DBCursor):

    def __init__(self, connection):

        super().__init__(connection=connection)

    def add_device_network(self, device_id, network_id):

        ds = self.get_device_network_id(device_id, network_id)

        if not ds:
            self.cursor.execute(
                    f"""
                    insert into monitoring.device_network(
                        device_id, network_id,
                        created_at, updated_at
                    )
                    values (
                        %(device_id)s, %(network_id)s,
                        now()::timestamp, now()::timestamp
                    )
                    """, {
                        "device_id": device_id,
                        "network_id": network_id
                    }
                )
        
            self.connection.commit()

    def get_device_network_id(self, device_id, network_id):

        self.cursor.execute(
            f"""
            select
                id
            from monitoring.device_network
            where deleted_at is null
            and network_id = %(network_id)s
            and device_id = %(device_id)s
            """, {
                "device_id": device_id,
                "network_id": network_id
            }
        )

        header = [x[0] for x in self.cursor.description]
        result = self.cursor.fetchone()

        return {
            header[i]: r for i, r in enumerate(result) 
        } if result else None

    
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

        self.connection.commit()
    