
from model.template import DBCursor


class DeviceService(DBCursor):

    def __init__(self, connection):

        super().__init__(connection=connection)

    def add_device_service(self, device_id, service_id):

        self.cursor.execute(
                f"""
                insert into monitoring.device_service(
                    service_id, device_id,
                    created_at, updated_at
                )
                select
                    %(service_id)s, %(device_id)s,
                    now()::timestamp, now()::timestamp
                where not exists (
                    select
                        id
                    from monitoring.device_service
                    where deleted_at is null
                    and device_id = %(device_id)s
                    and service_id = %(service_id)s
                )
                """, {
                    "service_id": service_id,
                    "device_id": device_id
                }
            )
    
        self.connection.commit()
    
    def get_device_service_id(self, device_id, service_id):

        self.cursor.execute(
            f"""
            select
                id
            from monitoring.device_service
            where deleted_at is null
            and device_id = %(device_id)s
            and service_id = %(service_id)s
            """, {
                "device_id": device_id,
                "service_id": service_id
            }
        )
    
        header = [x[0] for x in self.cursor.description]
        result = self.cursor.fetchone()

        return {
            header[i]: r for i, r in enumerate(result) 
        } if result else None

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

        self.connection.commit()
    