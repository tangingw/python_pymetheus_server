from model.network import Network
from model.service import Service
from template import DBCursor


class NetworkService(DBCursor):

    def __init__(self, connection):

        super().__init__(connection=connection)

        self.service = Service(self.connection)
        self.network = Network(self.connection)

    def add_network_service(self, ip_address, service_name):
        self.cursor.execute(
                f"""
                insert into monitoring.device_service(
                    service_id, device_id
                )
                values (
                    %(service_id)s, %(network_id)s
                ) on conflict (service_id, device_id) do nothing
                """, {
                    "service_id": self.service.get_service_id(service_name)["id"],
                    "network_id": self.network.get_network_id(ip_address)["id"]
                }
            )
    
        self.cursor.commit()

    def get_service_id(self, service_name):

        self.cursor.execute(
            f"""
            select 
                id 
            from monitoring.network_service where
            where service_id = %(service_id)s
            and deleted_at is null
            """, {
                "service_id": self.service.get_service_id(service_name)["id"]
            }
        )

        header = [x[0] for x in self.cursor.description]
        results = self.cursor.fetchall()

        return [
            {
                header[i]: r for i, r in enumerate(result) 
            } for result in results
        ]   if results else None
    
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
    