from template import DBCursor


class Port(DBCursor):

    def __init__(self, connection):

        super().__init__(connection=connection)

    def add_port(self, port_data):
        self.cursor.execute(
                f"""
                insert into monitoring.port(
                    port, port_desc,
                    created_at, updated_at
                ) values(
                    %(port)s, %(port_desc)s,
                    now()::timestamp, now()::timestamp
                )
                on conflict(port)
                """, {
                    "port": port_data["port"],
                    "port_desc": port_data["port_desc"]
                }
            )
        
        self.cursor.commit()

    def get_port_id(self, port_num):

        self.cursor.execute(
            f"""
            select 
                id 
            from monitoring.port where
            where port = %(port_num)s
            and deleted_at is null
            """, {
                "port_num": port_num
            }
        )

        header = [x[0] for x in self.cursor.description]
        result = self.cursor.fetchone()

        return {
            header[i]: r for i, r in enumerate(result) 
        } if result else None
    
    def delete_port(self, port_num):

        self.cursor.execute(
            f"""
            update monitoring.port set deleted_at = (now()::timestamp)
            where port = %(port_num)s
            and deleted_at is null;
            """, {"port_num": port_num}
        )

        self.cursor.commit()
