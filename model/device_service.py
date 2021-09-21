from model.device import Device
from model.service import Service
from template import DBCursor


class DeviceService(DBCursor):

    def __init__(self, connection):

        super().__init__(connection=connection)

        self.service = Service(self.connection)
        self.device = Device(self.connection)

    def add_device_service(self, device_hostname, service_name):
        self.cursor.execute(
                f"""
                insert into monitoring.device_service(
                    service_id, device_id,
                    created_at, updated_at
                )
                values (
                    %(service_id)s, %(device_id)s,
                    now()::timestamp, now()::timestamp
                ) on conflict(service_id, device_id) do nothing
                """, {
                    "service_id": self.service.get_service_id(service_name)["id"],
                    "device_id": self.device.get_device_id(device_hostname)["id"]
                }
            )
    
        self.cursor.commit()

    def get_service_id(self, service_name):

        self.cursor.execute(
            f"""
            select 
                id 
            from service where
            where monitoring.device_service_name = %(service_name)s
            and deleted_at is null
            """, {
                "service_name": service_name
            }
        )

        header = [x[0] for x in self.cursor.description]
        results = self.cursor.fetchall()

        return [
            {
                header[i]: r for i, r in enumerate(result) 
            } for result in results
        ] if results else None
    
    def delete_service(self, service_name, host_name):

        self.cursor.execute(
            f"""
            update monitoring.device_service set deleted_at = (now()::timestamp)
            where 
                service_id = %(service_id)s 
            and device_id = %(device_id)s
            and deleted_at is null;
            """, {
                "service_id": self.service.get_service_id(service_name)["id"],
                "device_id": self.device.get_device_id(host_name)["id"]
            }
        )

        self.cursor.commit()
    