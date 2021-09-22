from model.template import DBCursor


class Interface(DBCursor):

    def __init__(self, connection):

        super().__init__(connection=connection)
    
    def add_interface(self, interface_dict):

        self.cursor.execute(
                f"""
                insert into monitoring.interface(
                    interface_name, mac_address,
                    created_at, updated_at
                ) select
                    %(interface_name)s, %(mac_address)s,
                    now()::timestamp, now()::timestamp
                where not exists (
                    select 
                        id 
                    from monitoring.interface
                    where mac_address = %(mac_address)s
                    and deleted_at is null
                )
                """, {
                    "interface_name": interface_dict["interface_name"],
                    "mac_address": interface_dict["mac_address"],
                }
            )
        
        self.connection.commit()
    
    def get_interface_id(self, mac_address):

        self.cursor.execute(
            f"""
            select 
                id 
            from monitoring.interface
            where mac_address = %(mac_address)s
            and deleted_at is null
            """, {
                "mac_address": mac_address
            }
        )

        header = [x[0] for x in self.cursor.description]
        result = self.cursor.fetchone()

        return {
            header[i]: r for i, r in enumerate(result) 
        } if result else None
    
    def delete_interface(self, interface_name):

        self.cursor.execute(
            f"""
            update monitoring.interface set deleted_at = (now()::timestamp)
            where interface_name = %(interface_name)s
            and deleted_at is null;
            """, {"interface_name": interface_name}
        )

        self.connection.commit()