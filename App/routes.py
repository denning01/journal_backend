# app/routes.py
from flask import Blueprint
from App.controllers import create_post, get_posts, delete_post

posts_bp = Blueprint('posts', __name__)

@posts_bp.route('/posts', methods=['POST'])
def create_post_route():
    return create_post()

@posts_bp.route('/posts', methods=['GET'])
def get_posts_route():
    return get_posts()

@posts_bp.route('/posts/<int:post_id>', methods=['DELETE'])
def delete_post_route(post_id):
    return delete_post(post_id)
