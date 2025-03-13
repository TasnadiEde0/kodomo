from mysql.connector import Error
from .ImageCRUD import delete_allImageofUser
from .IntervalCRUD import delete_intervals_by_user
from flask import current_app

def create_user(conn, username, password_hash, usertype_id = 2, first_name = None, last_name = None, birth_date = None, address = None, post_code = None, email = None):
    """
    Inserts a new user into the database.

    Parameters:
    conn -- connection to the database
    username -- the new user's username, must be a string
    password_hash -- the new user's hashed password, must be a string
    usertype_id -- role of the user (foreign key to usertypes)
    first_name -- the user's first name
    last_name -- the user's last name
    birth_date -- the user's birth date (datetime)
    address -- the user's address
    post_code -- the user's postal code
    email -- the user's email address
    """
    cursor = conn.cursor()
    try:
        query = """
        INSERT INTO users (username, password_hash, userTypeId, first_name, last_name, birth_date, address, post_code, email) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        params = (username, password_hash, usertype_id, first_name, last_name, birth_date, address, post_code, email)
        cursor.execute(query, params)
        conn.commit()
    except Error as e:
        current_app.logger.error(f"Error: {e}")
    finally:
        cursor.close()
    conn.commit()


def read_user(conn, user_id=None, username=None):
    """
    Retrieves users from the database, either based on id or on name.

    Parameters:
    conn -- connection to the database
    user_id -- optional, if provided returns only the user with the given ID
    username -- optional, if provided returns only the user with the given username
    """
    cursor = conn.cursor(dictionary=True)
    try:
        if user_id is not None:
            query = "SELECT * FROM users WHERE userId = %s;"
            cursor.execute(query, (user_id,))
        elif username is not None:
            query = "SELECT * FROM users WHERE username = %s;"
            cursor.execute(query, (username,))
        else:
            query = "SELECT * FROM users;"
            cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        current_app.logger.error(f"Error: {e}")
    finally:
        cursor.close()


def update_user(conn, user_id, username=None, password_hash=None, usertype_id=None, first_name=None, last_name=None, birth_date=None, address=None, post_code=None, email=None):
    """
    Updates a selected user's information in the database.

    Parameters:
    conn -- connection to the database
    user_id -- the ID of the user
    Optional parameters:
        username -- new username
        password_hash -- new hashed password
        usertype_id -- new user type
        first_name -- new first name
        last_name -- new last name
        birth_date -- new birth date
        address -- new address
        post_code -- new postal code
        email -- new email
    """
    current_data = read_user(conn, user_id)
    if not current_data:
        current_app.logger.error("User not found!")
        return

    current_data = current_data[0]
    username = username if username is not None else current_data["username"]
    password_hash = password_hash if password_hash is not None else current_data["password_hash"]
    usertype_id = usertype_id if usertype_id is not None else current_data["userTypeId"]
    first_name = first_name if first_name is not None else current_data["first_name"]
    last_name = last_name if last_name is not None else current_data["last_name"]
    birth_date = birth_date if birth_date is not None else current_data["birth_date"]
    address = address if address is not None else current_data["address"]
    post_code = post_code if post_code is not None else current_data["post_code"]
    email = email if email is not None else current_data["email"]

    cursor = conn.cursor()
    try:
        query = """
        UPDATE users 
        SET username = %s, password_hash = %s, userTypeId = %s, first_name = %s, last_name = %s, 
            birth_date = %s, address = %s, post_code = %s, email = %s 
        WHERE userId = %s;
        """
        params = (username, password_hash, usertype_id, first_name, last_name, birth_date, address, post_code, email, user_id)
        cursor.execute(query, params)
        conn.commit()
    except Error as e:
        current_app.logger.error(f"Error: {e}")
    finally:
        cursor.close()
    conn.commit()


def delete_user(conn, user_id):
    """
    Deletes a selected user from the database.

    Parameters:
    conn -- connection to the database
    user_id -- the ID of the user, must be an integer
    """
    delete_intervals_by_user(conn, user_id) #getting rid of intervals attached to user
    delete_allImageofUser(conn, user_id) #marking images attached to user as deleted
    cursor = conn.cursor()
    try:
        query = "DELETE FROM users WHERE userId = %s;"
        cursor.execute(query, (user_id,))
        conn.commit()
    except Error as e:
        current_app.logger.error(f"Error: {e}")
    finally:
        cursor.close()
        
        
def read_nonadmin_users(conn):
    """
    Retrieves users from the database, either based on id or on name.

    Parameters:
    conn -- connection to the database
    user_id -- optional, if provided returns only the user with the given ID
    username -- optional, if provided returns only the user with the given username
    """
    cursor = conn.cursor(dictionary=True)
    try:
        query = "SELECT * FROM users WHERE userTypeId = 2;"
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        current_app.logger.error(f"Error: {e}")
    finally:
        cursor.close()
