

class Harddisk:

    def __init__(self, connection):

        self.connection = connection
        self.cursor = self.connection.cursor(buffered=True)

    def add_hardisk(self, host_name, harddisk_data):
        self.cursor.execute(
                f"""
                insert into monitoring.harddisk(
                    name, mount_point,
                    fs_type, size, 
                    device_id,
                    created_at, updated_at
                )
                select 
                    %(name)s, %(mount_point), %(fs_tye), 
                    %(size), id,
                    now()::timestamp, now()::timestamp
                from monitoring.device
                where deleted_at is null
                and host_name = %(host_name)s
                """, {
                    "name": harddisk_data["name"],
                    "mount_point": harddisk_data["mount_point"],
                    "fs_type": harddisk_data["fs_type"],
                    "size": harddisk_data["size"],
                    "host_name": host_name
                }
            )
        
        self.cursor.commit()

    def get_harddisk_id(self, harddisk_name):

        self.cursor.execute(
            f"""
            select 
                id 
            from monitoring.harddisk where
            where name = %(name)s
            and deleted_at is null
            """, {
                "name": harddisk_name
            }
        )

        header = [x[0] for x in self.cursor.description]
        result = self.cursor.fetchone()

        return {
            header[i]: r for i, r in enumerate(result) 
        } if result else None
    
    def delete_harddisk(self, harddisk_name):

        self.cursor.execute(
            f"""
            update monitoring.harddisk set deleted_at = (now()::timestamp)
            where name = %(name)s and deleted_at is null;
            """, {"name": harddisk_name}
        )

        self.cursor.commit()