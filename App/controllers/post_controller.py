# app/controllers/post_controller.py
from flask import jsonify, request
from ..models import Post, db

def create_post():
    data = request.json
    new_post = Post(title=data['title'], content=data['content'], image_url=data.get('image_url'), user_id=data['user_id'])
    db.session.add(new_post)
    db.session.commit()
    return jsonify({"message": "Post created", "post": new_post}), 201

def get_posts():
    posts = Post.query.all()
    return jsonify([{"id": post.id, "title": post.title, "content": post.content, "image_url": post.image_url, "user_id": post.user_id} for post in posts]), 200

def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return jsonify({"message": "Post deleted"}), 200
