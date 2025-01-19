from flask import Blueprint, request, render_template, redirect, url_for, jsonify
from models.user_model import register_user, authenticate_user

user_bp = Blueprint('user', __name__, url_prefix='/api/user')

@user_bp.route('/register', methods=['GET'])
def render_register_page():
    return render_template('register.html')

@user_bp.route('/register', methods=['POST'])
def handle_register():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')

    if not username or not email or not password:
        return jsonify({"error": "All fields are required"}), 400

    result = register_user(username, email, password)
    if "error" in result:
        return jsonify(result), 400

    return redirect(url_for('user.render_login_page'))

@user_bp.route('/login', methods=['GET'])
def render_login_page():
    return render_template('login.html')

@user_bp.route('/login', methods=['POST'])
def handle_login():
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        return jsonify({"error": "All fields are required"}), 400

    user = authenticate_user(username, password)
    if not user:
        return jsonify({"error": "Invalid username or password"}), 401

    return redirect(url_for('post.render_feed'))
