import os.path
from db.connector import get_config, get_connection


def test_config_file():

    assert os.path.exists("config.py")


def test_import_config():

    my_config = get_config('config')
    for keyword in ["DATABASE", "USER", "PASSWORD", "HOST"]:

        assert keyword in my_config.keys()


def test_connection():

    result = None
    my_connection = get_connection("config")

    with my_connection.cursor() as cursor:

        cursor.execute(
            """
            select 1 + 1
            """
        )

        result = cursor.fetchone()
    
    assert isinstance(result, tuple)
    assert result[0] == 2