

class Network:

    def __init__(self, connection):

        self.connection = connection
        self.cursor = self.connection.cursor(buffered=True)

    def add_network(self, host_name, network_data):
        self.cursor.execute(
                f"""
                insert into monitoring.network_ip(
                    ip_address, ip_version, device_id,
                    created_at, updated_at
                )
                select 
                    %(ip_address)s, %(ip_version), id,
                    now()::timestamp, now()::timestamp
                from monitoring.device
                where deleted_at is null
                and host_name = %(host_name)s
                """, {
                    "ip_address": network_data["ip_address"],
                    "ip_version": network_data["ip_version"],
                    "host_name": host_name
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