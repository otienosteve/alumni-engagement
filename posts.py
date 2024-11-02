from flask import Blueprint,render_template


post_bp = Blueprint('post_bp', __name__,url_prefix='/post')

@post_bp.route('')
def post():
    return render_template('post/post.html')