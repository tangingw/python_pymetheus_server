import psycopg2
from werkzeug.utils import import_string


def get_config(config):

    connector_key = dict()
    
    if isinstance(config, str):

        config = import_string(config)
    
    for key in dir(config):

        if key.isupper():

            connector_key[key] = getattr(config, key)

    return connector_key


def get_connection(config):

    connection_config = get_config(config)

    return psycopg2.connect(
        database=connection_config["DATABASE"],
        user=connection_config["USER"],
        password=connection_config["PASSWORD"],
        host=connection_config["HOST"]
    )
