from template import DBCursor


class Network:

    def __init__(self, connection):

        super().__init__(connection=connection)

    def add_network(self, network_data):
        self.cursor.execute(
                f"""
                insert into monitoring.network(
                    ip_address, ip_version
                    created_at, updated_at
                ) values(
                    %(ip_address)s, %(ip_version),
                    now()::timestamp, now()::timestamp
                )
                on conflict(ip_address) do nothing
                """, {
                    "ip_address": network_data["ip_address"],
                    "ip_version": network_data["ip_version"]
                }
            )
        
        self.cursor.commit()

    def get_network_id(self, ip_address):

        self.cursor.execute(
            f"""
            select 
                id 
            from monitoring.network_ip where
            where ip_address = %(ip_address)s
            and deleted_at is null
            """, {
                "ip_address": ip_address
            }
        )

        header = [x[0] for x in self.cursor.description]
        result = self.cursor.fetchone()

        return {
            header[i]: r for i, r in enumerate(result) 
        } if result else None
    
    def delete_network(self, ip_address):

        self.cursor.execute(
            f"""
            update monitoring.network_ip set deleted_at = (now()::timestamp)
            where ip_address = %(ip_address)s
            and deleted_at is null
            ;
            """, {"ip_address": ip_address}
        )

        self.cursor.commit()