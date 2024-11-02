from flask import Blueprint, render_template, request, redirect, url_for, flash

alumni_bp = Blueprint('alumni_bp',__name__,url_prefix='/alumni')


@alumni_bp.route('/')
def index():
    
    return render_template('alumni/post.html')