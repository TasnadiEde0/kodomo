from mysql.connector import Error
from flask import current_app

def find_all_intervals(conn):
    """
    Retrieves all intervals from the database.

    Parameters:
    conn -- connection to the database
    """
    cursor = conn.cursor(dictionary=True)
    try:
        query = "SELECT * FROM intervals;"
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        current_app.logger.error(f"Error: {e}")
    finally:
        cursor.close()


def find_intervals_by_user(conn, user_id):
    """
    Retrieves intervals associated with a specific user from the database.

    Parameters:
    conn -- connection to the database
    user_id -- the ID of the user
    """
    cursor = conn.cursor(dictionary=True)
    try:
        query = "SELECT * FROM intervals WHERE userId = %s;"
        cursor.execute(query, (user_id,))
        result = cursor.fetchall()
        return result
    except Error as e:
        current_app.logger.error(f"Error: {e}")
    finally:
        cursor.close()


def insert_interval(conn, user_id, start_date=None, end_date=None):
    """
    Inserts a new interval into the database.

    Parameters:
    conn -- connection to the database
    start_date -- the start date of the interval
    end_date -- the end date of the interval
    user_id -- the ID of the user associated with this interval
    """
    cursor = conn.cursor()
    try:
        query = """
        INSERT INTO intervals (startDate, endDate, userId) 
        VALUES (%s, %s, %s);
        """
        params = (start_date, end_date, user_id)
        cursor.execute(query, params)
        conn.commit()
        current_app.logger.info("Interval inserted successfully.")
    except Error as e:
        current_app.logger.error(f"Error: {e}")
    finally:
        cursor.close()
    conn.commit()

def delete_intervals_by_user(conn, user_id):
    """
    Deletes all intervals associated with a specific user from the database.

    Parameters:
    conn -- connection to the database
    user_id -- the ID of the user whose intervals should be deleted
    """
    cursor = conn.cursor()
    try:
        query = "DELETE FROM intervals WHERE userId = %s;"
        cursor.execute(query, (user_id,))
        conn.commit()
        current_app.logger.info(f"All intervals for userId {user_id} deleted successfully.")
    except Error as e:
        current_app.logger.error(f"Error: {e}")
    finally:
        cursor.close()
        
def delete_interval(conn, interval_id):
    cursor = conn.cursor()
    try:
        query = "DELETE FROM intervals WHERE intervalId = %s;"
        cursor.execute(query, (interval_id,))
        conn.commit()
    except Error as e:
        current_app.logger.error(f"Error: {e}")
    finally:
        cursor.close()

