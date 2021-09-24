from template import DBCursor


class HeartBeat(DBCursor):

    def __init__(self, connection):
        super().__init__(connection)
    
    def add_heart_beat(self, device_name):

        self.cursor.execute(
            f"""
            insert into monitoring.device_heartbeat(
                device_id, 
                created_at,
                updated_at
            )
            select
                id, (now() at time zone 'utc')::timestamp,
                (now() at time zone 'utc')::timestamp
            from monitoring.device
            where deleted_at is null
            and host_name = %(device_name)s
            and not exists (
                select
                    device_id
                from monitoring.device_heartbeat
                where device_id = (
                    select id from monitoring.device
                    where host_name = %(device_name)s
                    and deleted_at is null
                )
            )
            """, {
                "device_name": device_name
            }
        )
        self.connection.commit()

    def get_latest_heartbeat(self, device_name):

        self.cursor.execute(
            f"""
            select 
                max(updated_at) as last_updated
            from monitoring.device_heartbeat
            where device_id = (
                select
                    id
                from monitoring.device
                where
                    host_name = %(host_name)s
                and deleted_at is null
            )
            """, {
                "host_name": device_name
            }
        )

        header = [x[0] for x in self.cursor.description]
        result = self.cursor.fetchone()

        return {
            header[i]: r for i, r in enumerate(result) 
        } if result else None

    def update_heartbeat(self, device_name):

        self.cursor.execute(
            f"""
            update monitoring.device_heartbeat
            set 
                updated_at = (now() at time zone 'utc')::timestamp
            where device_id = (
                select
                    id
                from monitoring.device
                where deleted_at is null
                and host_name = %(host_name)s
            )
            """, {
                "host_name": device_name
            }
        )

        self.connection.commit()