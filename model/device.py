

class Device:

    def __init__(self, connection):

        self.connection = connection
        self.cursor = self.connection.cursor(buffered=True)
    
    def insert_device(self, device_data):

        self.cursor.execute(
            f"""
            insert into monitoring.device(
                host_name, cpu, memory,
                os_install, created_at,
                updated_at
            ) values (
                %(host_name)s, %(cpu)s, %(memory)s,
                %(os_install), now()::timestamp,
                now()::timestamp
            )
            """, {
                "host_name": device_data["host_name"],
                "cpu": device_data["cpu"], "memory": device_data["memory"],
                "os_install": device_data["os_install"]
            }
        )
    
        self.cursor.commit()

    def get_device_id(self, host_name):

        self.cursor.execute(
            f"""
            select 
                id 
            from monitoring.device where
            where host_name = %(host_name)s
            and deleted_at is null
            """, {
                "host_name": host_name
            }
        )

        header = [x[0] for x in self.cursor.description]
        result = self.cursor.fetchone()

        return {
            header[i]: r for i, r in enumerate(result) 
        } if result else None

    def delete_device(self, host_name):

        self.cursor.execute(
            f"""
            update monitoring.device set deleted_at = (now()::timestamp)
            where host_name = %(host_name)s;
            """, {"host_name": host_name}
        )

        self.cursor.commit()
