import os
from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from werkzeug.utils import secure_filename
from models.post_model import create_post, get_all_posts

post_bp = Blueprint('post', __name__, url_prefix='/api/post')

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@post_bp.route('/create-post', methods=['GET'])
def render_create_post_page():
    return render_template('create_post.html')

@post_bp.route('/create', methods=['POST'])
def create_post_route():
    username = request.form.get('username')
    description = request.form.get('description')
    image_url = ''

    if 'image' in request.files:
        file = request.files['image']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)
            image_url = f'/{filepath}'

    if not username or not description:
        return jsonify({"error": "Username and description are required"}), 400

    create_post(username, description, image_url)
    return redirect(url_for('post.render_feed'))

@post_bp.route('/feed', methods=['GET'])
def render_feed():
    posts = get_all_posts()
    for post in posts:
        post['_id'] = str(post['_id'])
    return render_template('feed.html', posts=posts)
