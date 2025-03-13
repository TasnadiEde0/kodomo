import datetime

from flask import Blueprint, render_template, session, redirect, send_from_directory, jsonify, send_from_directory, current_app
import bcrypt
from dataaccess.DataCon import *
from dataaccess.ImageCRUD import *
from dataaccess.UserCRUD import *
from dataaccess.IntervalCRUD import *

webpage_blueprint = Blueprint('webpage', __name__)

def login_checker_webpage(f):
    """
    Checks if an user is logged in.
    
    Returns:
    true of false
    """
    def wrapper(*args, **kwargs):

        userId = session.get('user_id')

        if userId is None:
            return redirect("/login")

        return f(*args, **kwargs)

    wrapper.__name__ = f.__name__

    return wrapper

def admin_checker(conn, user_id):
    """
    Checks whether a user has admin priviliges.

    Parameters:
    conn -- database connection
    user_id -- ID of a logged in user
    
    Returns:
    True or false.
    """
    user = read_user(conn, user_id)[0]
    user_type = user["userTypeId"]
    return user_type == 1

@webpage_blueprint.route('/login', methods=['GET'])
def login_page():
    """
    Serves the login page.
    
    Returns:
    A static file.
    """
    return send_from_directory("static", "login.html")

@webpage_blueprint.route('/register', methods=['GET'])
def register_page():
    """
    Serves the register page.
    
    Returns:
    A static file.
    """
    return send_from_directory("static", "register.html")

@webpage_blueprint.route('/imgs', methods=['GET'])
@login_checker_webpage
def images_page():
    """
    Serves the image listing page of a user, or all images in case of an admin.
    
    Returns:
    The built html file.
    """
    conn = get_connection()
    userId = session.get('user_id')
    is_admin = admin_checker(conn, userId)

    imgs = read_images_of_user(conn, userId) if not is_admin else read_images(conn)
    user = read_user(conn, userId)[0]
    monogram = get_monogram(user["username"])
    conn.close()

    return render_template("imgs.html", imgs = imgs, userId = userId, username = user["username"], monogram = monogram, is_admin = is_admin, page_owner = user["username"])

@webpage_blueprint.route('/statistics', methods=['GET'])
@login_checker_webpage
def statistic_page():
    """
    Serves the statistics page of a user.
    
    Returns:
    The built html file.
    """
    conn = get_connection()
    userId = session.get('user_id')
    is_admin = admin_checker(conn, userId)

    user = read_user(conn, userId)[0]
    monogram = get_monogram(user["username"])
    conn.close()
    if is_admin:
        return {"error": "Forbidden"}, 403
    else:
        return render_template("statistics.html", username = user["username"], monogram = monogram)

@webpage_blueprint.route('/', methods=['GET'])
@webpage_blueprint.route('/index', methods=['GET'])
def index_page():
    """
    Serves the index page of a user, or the admin dashboard.
    
    Returns:
    The built html file.
    """
    conn = get_connection()
    userId = session.get('user_id')
    is_admin = admin_checker(conn, userId)

    if userId is not None:
        user = read_user(conn, userId)[0]
        monogram = get_monogram(user["username"])
        all_users = read_nonadmin_users(conn)
        conn.close()
        return render_template("index.html", username = user["username"], monogram = monogram, is_admin = is_admin, users = all_users)
    else:
        return send_from_directory("static", "home.html")

@webpage_blueprint.route('/imgs/<id>', methods=['GET'])
@login_checker_webpage
def img_page(id):
    """
    Serves the page that displays information about a specific image.
    
    Parameters:
    id -- ID of the image
    
    Returns:
    The built html file.
    """
    conn = get_connection()
    userId = session.get('user_id')
    is_admin = admin_checker(conn, userId)

    user = read_user(conn, userId)[0]
    monogram = get_monogram(user["username"])
    conn.close()


    conn = get_connection()
    result = read_image(conn, id)[0]
    result["record_time"] = datetime.datetime.strftime(result["record_time"], "%Y/%m/%d")
    conn.close()

    return render_template("img.html", username = user["username"], monogram = monogram, img = result, is_admin = is_admin)

@webpage_blueprint.route('/intervals', methods=['GET'])
@login_checker_webpage
def intervals():
    """
    Serves the intervals page of a user, or all intervals for an admin.
    
    Returns:
    The built html file.
    """
    conn = get_connection()
    userId = session.get('user_id')
    is_admin = admin_checker(conn, userId)

    user = read_user(conn, userId)[0]
    monogram = get_monogram(user["username"])
    intervals = find_intervals_by_user(conn, userId) if not is_admin else find_all_intervals(conn)
    conn.close()
    return render_template("intervals.html", username = user["username"], monogram = monogram, intervals = intervals, is_admin = is_admin, page_owner = user["username"])

@webpage_blueprint.route('/users', methods=['GET'])
@login_checker_webpage
def users():
    """
    Serves the page of users for an admin, also available on the admin dashboard.
    
    Returns:
    The built html file.
    """
    conn = get_connection()
    userId = session.get('user_id')
    is_admin = admin_checker(conn, userId)

    if is_admin:
        user = read_user(conn, userId)[0]
        users = read_nonadmin_users(conn)
        return render_template("users.html", username = user["username"], users = users)
    else:
        return {"error": "Forbidden"}, 403

@webpage_blueprint.route('/users/<id>/imgs', methods=['GET'])
@login_checker_webpage
def user_images(id):
    """
    Serves the images of a user for an admin, contains the same content that a user can see regarding their images.
    
    Returns:
    The built html file.
    """
    conn = get_connection()
    userId = session.get('user_id')
    is_admin = admin_checker(conn, userId)
    
    if is_admin:
        imgs = read_images_of_user(conn, id)
        user = read_user(conn, userId)[0]
        page_owner = read_user(conn, id)[0]
        conn.close()
        return render_template("imgs.html", imgs = imgs, userId = userId, username = user["username"], monogram = None, is_admin = True, page_owner = page_owner["username"])
    else:
        return {"error": "Forbidden"}, 403
    
@webpage_blueprint.route('/users/<id>/intervals', methods=['GET'])
@login_checker_webpage
def user_intervals(id):
    """
    Serves the intervals of a user for an admin, contains the same content that a user can see regarding their intervals.
    
    Returns:
    The built html file.
    """
    conn = get_connection()
    userId = session.get('user_id')
    is_admin = admin_checker(conn, userId)
    
    if is_admin:
        intervals = find_intervals_by_user(conn, id)
        user = read_user(conn, userId)[0]
        page_owner = read_user(conn, id)[0]
        conn.close()
        return render_template("intervals.html", username = user["username"], monogram = None, intervals = intervals, is_admin = True, page_owner = page_owner["username"])
    else:
        return {"error": "Forbidden"}, 403

def get_monogram(username):
    """
    Builds the monogram of a user based on their name
    
    Returns:
    A word with uppercase letters.
    """
    words = username.split()
    return ''.join(word[0].upper() for word in words)




