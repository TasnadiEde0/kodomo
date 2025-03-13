import os
import mysql.connector
import json


#"35.197.108.193"
def read_config(filename):
    """
    Reads and returns the content of a JSON configuration file.

    Parameters:
    filename -- the JSON file path
    
    Returns:
    Dictionary containing the configuration.
    """
    with open(filename, "r") as file:
        config = json.load(file)
    return config

def get_connection(config_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')):
    """
    Opens a database connection.

    Parameters:
    config_file -- the JSON file containing database connection parameters
    
    Returns:
    MySQL connection object
    """
    config = read_config(config_file)
    
    # Extract connection parameters
    host = config["host"]
    port = config["port"]
    username = config["username"]
    password = config["password"]
    dbname = config["dbname"]

    # Establish the connection
    conn = mysql.connector.connect(
        host=host,
        port=port,
        user=username,
        password=password,
        database=dbname
    )
    return conn

def close_connection(conn):
    """
    Closes the database connection.

    Parameters:
    conn -- MySQL connection object
    """
    conn.close()
