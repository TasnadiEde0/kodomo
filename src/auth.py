from flask import Blueprint, render_template, session, redirect, send_from_directory, jsonify, request, current_app
import bcrypt
from dataaccess.DataCon import *
from dataaccess.UserCRUD import *

auth_blueprint = Blueprint('auth', __name__)

def login_checker(f):
    """
    Checks if a user is logged in.
    
    Returns:
    true of false
    """
    def wrapper(*args, **kwargs):
        user_id = session.get('user_id')

        if user_id is None:
            return jsonify({'error': 'Unauthorized access, login required'}), 401

        return f(*args, **kwargs)

    wrapper.__name__ = f.__name__

    return wrapper

@auth_blueprint.route('/register', methods=['POST'])
def register():
    """
    Handles user registration.
    
    Returns:
    A status code and a message
    """
    conn = get_connection()

    data = request.json
    username = data.get('username')
    password = data.get('password')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    birth_date = data.get('birth_date')
    address = data.get('address')
    post_code = data.get('post_code')
    email = data.get('email')

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt).decode()

    try:
        create_user(
            conn,
            username=username,
            password_hash=hashed_password,
            first_name=first_name,
            last_name=last_name,
            birth_date=birth_date,
            address=address,
            post_code=post_code,
            email=email
        )
        users = read_user(conn)
        user = next((u for u in users if u['username'] == username), None)

        if user:
            session["user_id"] = user["userId"]
        else:
            raise Exception('User not found')

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        conn.close()

    return jsonify({"message": "User registered successfully"}), 201

@auth_blueprint.route('/login', methods=['POST'])
def login():
    """
    Handles user login.
    
    Returns:
    A status code and a message
    """
    conn = get_connection()
    data = request.json

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    try:
        users = read_user(conn)
        user = next((u for u in users if u["username"] == username), None)

        if not user:
            return jsonify({"error": "Invalid username or password"}), 401

        if not bcrypt.checkpw(password.encode(), user["password_hash"].encode()):
            return jsonify({"error": "Invalid username or password"}), 401

        session["user_id"] = user["userId"]
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    conn.close()
    return jsonify({"message": "Logged in successfully"}), 200

@auth_blueprint.route('/logout', methods=['POST', 'GET'])
@login_checker
def logout():
    """
    Logs out the user.
    
    Returns:
    A status code and a message
    """
    session.pop("user_id", None)
    return jsonify({"message": "Logged out successfully"}), 200
