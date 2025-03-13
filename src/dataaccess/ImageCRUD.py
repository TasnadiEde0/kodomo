from mysql.connector import Error
from flask import current_app

def create_image(conn, user_id, image_path, probability=0.0, record_time=None, is_deleted=0):
    """
    Inserts a new image into the database.

    Parameters:
    conn -- connection to the database
    user_id -- the user's ID who uploads the image
    image_path -- the uploaded image path
    probability -- optional, default is 0
    record_time -- optional, the record time of the image
    is_deleted -- optional, default is 0 (not deleted)
    """
    cursor = conn.cursor()
    try:
        query = """
        INSERT INTO images (userId, imagePath, probability, record_time, isDeleted) 
        VALUES (%s, %s, %s, %s, %s);
        """
        params = (user_id, image_path, probability, record_time, is_deleted)
        cursor.execute(query, params)
        conn.commit()
        current_app.logger.info("Image created successfully.")
    except Error as e:
        current_app.logger.error(f"Error: {e}")
    finally:
        cursor.close()
    conn.commit()

def read_image(conn, image_id=None):
    """
    Retrieves images from the database.

    Parameters:
    conn -- connection to the database
    image_id -- optional, if provided returns only the image with the given ID
    """
    cursor = conn.cursor(dictionary=True)
    try:
        if image_id is None:
            query = "SELECT * FROM images WHERE isDeleted = 0;"
            cursor.execute(query)
        else:
            query = "SELECT * FROM images WHERE imageId = %s AND isDeleted = 0;"
            cursor.execute(query, (image_id,))
        result = cursor.fetchall()
        return result
    except Error as e:
        current_app.logger.error(f"Error: {e}")
    finally:
        cursor.close()

def read_images_of_user(conn, user_id):
    """
    Retrieves images of a specific user from the database.

    Parameters:
    conn -- connection to the database
    user_id -- the ID of the user
    """
    cursor = conn.cursor(dictionary=True)
    try:
        query = "SELECT * FROM images WHERE userId = %s AND isDeleted = 0;"
        cursor.execute(query, (user_id,))
        result = cursor.fetchall()
        return result
    except Error as e:
        current_app.logger.error(f"Error: {e}")
    finally:
        cursor.close()

def update_image(conn, image_id, probability=None, record_time=None, is_deleted=None):
    """
    Updates a selected image's information in the database.

    Parameters:
    conn -- connection to the database
    image_id -- the ID of the image
    probability -- optional, new probability value
    record_time -- optional, new record time
    is_deleted -- optional, update deleted status
    """
    current_data = read_image(conn, image_id)
    if not current_data:
        current_app.logger.error("Image not found!")
        return

    # Extract current values
    current_probability = current_data[0]["probability"]
    current_record_time = current_data[0]["record_time"]
    current_is_deleted = current_data[0]["isDeleted"]

    # Use current values if new values are not provided
    probability = probability if probability is not None else current_probability
    record_time = record_time if record_time is not None else current_record_time
    is_deleted = is_deleted if is_deleted is not None else current_is_deleted

    cursor = conn.cursor()
    try:
        query = """
        UPDATE images 
        SET probability = %s, record_time = %s, isDeleted = %s
        WHERE imageId = %s;
        """
        cursor.execute(query, (probability, record_time, is_deleted, image_id))
        conn.commit()
        current_app.logger.info("Image updated successfully.")
    except Error as e:
        current_app.logger.error(f"Error: {e}")
    finally:
        cursor.close()
    conn.commit()

def delete_image(conn, image_id):
    """
    Marks an image as deleted by setting its isDeleted field to 1.

    Parameters:
    conn -- connection to the database
    image_id -- the ID of the image
    """
    cursor = conn.cursor()
    try:
        query = "UPDATE images SET isDeleted = 1 WHERE imageId = %s;"
        cursor.execute(query, (image_id,))
        conn.commit()
        current_app.logger.info("Image marked as deleted successfully.")
    except Error as e:
        current_app.logger.error(f"Error: {e}")
    finally:
        cursor.close()
    conn.commit()

def delete_allImageofUser(conn, user_id):
    """
    Marks all images of a specific user as deleted by setting their isDeleted field to 1.

    Parameters:
    conn -- connection to the database
    user_id -- the ID of the user
    """
    cursor = conn.cursor()
    try:
        query = "UPDATE images SET isDeleted = 1 WHERE userId = %s;"
        cursor.execute(query, (user_id,))
        conn.commit()
        current_app.logger.info("All images for the user marked as deleted successfully.")
    except Error as e:
        current_app.logger.error(f"Error: {e}")
    finally:
        cursor.close()
    conn.commit()
    
def read_images(conn):
    """
    Retrieves every image from the database.

    Parameters:
    conn -- connection to the database
    """
    cursor = conn.cursor(dictionary=True)
    try:
        query = "SELECT * FROM images;"
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        current_app.logger.error(f"Error: {e}")
    finally:
        cursor.close()
    
    