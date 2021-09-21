
from template import DBCursor


class DeviceService(DBCursor):

    def __init__(self, connection):

        super().__init__(connection=connection)

    def add_device_service(self, device_id, service_id):
        self.cursor.execute(
                f"""
                insert into monitoring.device_service(
                    service_id, device_id
                )
                values (
                    %(service_id)s, %(device_id)s
                ) on conflict(service_id, device_id) do nothing
                """, {
                    "service_id": service_id,
                    "device_id": device_id
                }
            )
    
        self.cursor.commit()
    
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
    