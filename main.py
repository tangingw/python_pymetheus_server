import psycopg2


conn = psycopg2.connect(
    database="postgres",
    user="postgres",
    password="tallgeese3",
    host="192.168.0.179"
)

with conn.cursor() as cursor:

    cursor.execute(
        """
        select now()::timestamp
        """
    )

    result = cursor.fetchone()
    print(result)