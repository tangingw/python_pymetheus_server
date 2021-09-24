from model.template import DBCursor


class Port(DBCursor):

    def __init__(self, connection):

        super().__init__(connection=connection)

    def add_port(self, port_data):
        self.cursor.execute(
                f"""
                insert into monitoring.port(
                    port, port_desc,
                    created_at, updated_at
                ) select
                    %(port)s, %(port_desc)s,
                    (now() at time zone 'utc')::timestamp, 
                    (now() at time zone 'utc')::timestamp
                where not exists(
                    select 
                        id 
                    from monitoring.port
                    where port = %(port)s
                    and deleted_at is null
                )
                """, {
                    "port": port_data["port"],
                    "port_desc": port_data["port_desc"]
                }
            )
        
        self.connection.commit()

    def get_port_id(self, port_num):

        self.cursor.execute(
            f"""
            select 
                id 
            from monitoring.port
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
            update monitoring.port set deleted_at = ((now() at time zone 'utc')::timestamp)
            where port = %(port_num)s
            and deleted_at is null;
            """, {"port_num": port_num}
        )

        self.connection.commit()
