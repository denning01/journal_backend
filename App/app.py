import json
from flask import Flask, request
from App.models import db
from App.config import Config
from App.controllers  import post_controller
import psycopg2

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

conn = psycopg2.connect("dbname=test user=postgres password=secret")

app.add_url_rule('/posts', view_func=post_controller.create_post, methods=['POST'])
app.add_url_rule('/posts', view_func=post_controller.get_posts, methods=['GET'])
app.add_url_rule('/posts/<int:post_id>', view_func=post_controller.get_post, methods=['GET'])
app.add_url_rule('/posts/<int:post_id>', view_func=post_controller.delete_post, methods=['DELETE'])

def is_valid_image_url(url):
    valid_extensions = ['jpg', 'jpeg', 'png', 'gif']
    return any(url.lower().endswith(ext) for ext in valid_extensions)

@app.route('/posts', methods=['POST'])
def create_post():
    data = request.get_json()

    if 'image_url' in data and not is_valid_image_url(data['image_url']):
        return json.dumps({"error": "Invalid image URL format"}), 400

    cur = conn.cursor()
    cur.execute("""
        INSERT INTO posts (title, content, image_url, user_id)
        VALUES (%s, %s, %s, %s) RETURNING id;
    """, (data['title'], data['content'], data.get('image_url'), data['user_id']))

    post_id = cur.fetchone()[0]
    conn.commit()
    cur.close()

    return json.dumps({"message": "Post created successfully", "post_id": post_id}), 201

@app.route('/posts', methods=['GET'])
def get_posts():
    user_id = request.args.get('user_id')
    location = request.args.get('location')

    cur = conn.cursor()
    query = "SELECT * FROM posts WHERE TRUE"
    params = []

    if user_id:
        query += " AND user_id = %s"
        params.append(user_id)

    if location:
        query += " AND content ILIKE %s"
        params.append(f'%{location}%')

    cur.execute(query, params)
    posts = cur.fetchall()
    cur.close()

    posts_list = [
        {"id": row[0], "title": row[1], "content": row[2], "image_url": row[3], "user_id": row[4]}
        for row in posts
    ]

    return json.dumps(posts_list), 200

@app.route('/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    cur = conn.cursor()

    cur.execute("DELETE FROM posts WHERE id = %s RETURNING id", (post_id,))
    deleted_post_id = cur.fetchone()
    
    if not deleted_post_id:
        return json.dumps({"error": "Post not found"}), 404

    conn.commit()
    cur.close()

    return json.dumps({"message": "Post deleted successfully"}), 200


if __name__ == "__main__":
    app.run(debug=True)
