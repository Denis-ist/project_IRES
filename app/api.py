from flask import Blueprint, jsonify
from app.models import Post


api = Blueprint('api_module', __name__)


@api.route('/posts')
def posts_api():
    posts = Post.query.all()
    return jsonify([post.to_dict() for post in posts])