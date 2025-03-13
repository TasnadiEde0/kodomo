from flask import Blueprint, render_template, session, redirect, send_from_directory, jsonify, request, current_app
import uuid
import os
import numpy as np
from PIL import Image
from datetime import date

from classifier import predict_image
from util import green_prop, blur_detection
from flask import Flask, request, session
import random
import uuid
import dataaccess.ImageCRUD as ImageDao
import dataaccess.DataCon as DataCon
import webpage
import datetime
import dataaccess.IntervalCRUD as IntervalDao
import dataaccess.UserCRUD as UserDao
from flask import current_app

api_blueprint = Blueprint('api', __name__)



@api_blueprint.route('/images', methods=['POST'])
@webpage.login_checker_webpage
def upload():
    """
    Handles picture uploads.
    The picture is retrieved from the request body along with the date
    
    Returns:
    A status code and a message
    """
    if "img" not in request.files:
        return {"error": "Invalid request, 'img' key is missing"}, 400
    img = request.files["img"]
    filename2 = img.filename
    try:
        conn = DataCon.get_connection()
        filename = f"/static/images/{uuid.uuid4()}.jpg"
        # img.save(filename)
        img.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), "." + filename))
        pil_image = Image.open(img).convert("RGB")
        image_array = np.array(pil_image)
        print(green_prop(image_array))
        if green_prop(image_array) < 0.4:
            return {"message": "Image not green enough"}, 400
        user_id = session.get('user_id')

        probability = predict_image(filename[1:], filename2) # random.random()

        ImageDao.create_image(conn, user_id, filename, probability, datetime.datetime.strptime(request.form["date"], "%Y-%m-%d").isoformat())
        conn.close()
        return {"message": "Image uploaded successfully"}, 200
    except Exception as e:
        return {"error": f"Failed to upload image: {str(e)}"}, 500

@api_blueprint.route('/images/<img_id>', methods=['DELETE'])
@webpage.login_checker_webpage
def delete_img(img_id):
    """
    Handles image deletion.

    Parameters:
    img_id -- ID of the image
    
    Returns:
    A status code and a message
    """
    conn = DataCon.get_connection()
    img_props = ImageDao.read_image(conn, img_id)
    if img_props[0]["imagePath"] is not None:
        filename = img_props[0]["imagePath"][1:]
        os.remove(f"./{filename}")
        ImageDao.delete_image(conn, img_id)
        conn.close()
        return {"message": "Image deleted successfully"}, 200
    return {"message": "Image does not exist"}, 400

@api_blueprint.route('/periods', methods=['GET'])
@webpage.login_checker_webpage
def get_periods():
    """
    Constructs the periods of a user.
    
    Returns:
    The list of periods
    """
    conn = DataCon.get_connection()
    cursor = conn.cursor()
    userId = session.get('user_id')
    cursor.execute("SELECT i.startDate, i.endDate FROM intervals i  WHERE i.userId = %s", (userId, ))
    result = cursor.fetchall()

    current_app.logger.debug(result)

    result = [{"start": i[0].strftime("%Y-%m-%d"), "end": i[1].strftime("%Y-%m-%d")} for i in result]

    current_app.logger.debug(result)

    cursor.close()
    conn.commit()
    conn.close()
    return result

@api_blueprint.route('/periods', methods=['POST'])
@webpage.login_checker_webpage
def post_periods():
    """
    Handles upload of a period.
    
    Returns:
    A status code and a message
    """
    startDate = datetime.datetime.strptime(request.form['startDate'], "%Y-%m-%d").date()
    endDate = datetime.datetime.strptime(request.form['endDate'], "%Y-%m-%d").date()

    current_app.logger.info(startDate)
    current_app.logger.info(endDate)

    conn = DataCon.get_connection()
    cursor = conn.cursor()
    userId = session.get('user_id')
    cursor.execute("INSERT INTO intervals(startDate, endDate, userId) VALUES (%s, %s, %s)", (startDate, endDate, userId))
    cursor.close()
    conn.commit()
    conn.close()

    return {"message": "Interval registered"}, 200

@api_blueprint.route('/images', methods=['GET'])
@webpage.login_checker_webpage
def get_images():
    """
    Retrieves the images of a user.
    
    Returns:
    The list of images
    """
    conn = DataCon.get_connection()

    userId = session.get('user_id')
    result = ImageDao.read_images_of_user(conn, userId)

    result = [{"date": i["record_time"].strftime("%Y-%m-%d"),
               "prob": i["probability"],
               "imagePath": i["imagePath"],
               "link": f"imgs/" + str(i["imageId"]) } for i in result ]

    conn.close()
    return result

@api_blueprint.route('/user', methods=['DELETE'])
@webpage.login_checker_webpage
def delete_user():
    """
    Deletes the logged-in user and all their related data (images and intervals).
    """
    conn = DataCon.get_connection()
    user_id = session.get('user_id')

    try:
        UserDao.delete_user(conn, user_id)
        session.pop('user_id', None)# we log the user out
    except Exception as e:
        current_app.logger.error(f"Error deleting user: {e}")
        return jsonify({"error": "An error occurred while deleting the user."}), 500
    finally:
        conn.close()

    return jsonify({"message": "User and all related data deleted successfully"}), 200

@api_blueprint.route('/intervals/<id>', methods=['DELETE'])
def delete_interval(id):
    """
    Handles deletion of an interval.

    Parameters:
    id -- ID of the interval
    
    Returns:
    A status code and a message
    """
    conn = DataCon.get_connection()
    user_id = session.get('user_id')

    if not user_id:
        return jsonify({"error": "User not logged in"}), 401
    try:
        IntervalDao.delete_interval(conn, id)
    except Exception as e:
        return jsonify({"error": "An error occurred while deleting the user."}), 500
    finally:
        conn.close()
        
    return jsonify({"message": "Interval deleted successfully"}), 200