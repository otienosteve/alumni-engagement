from flask import Blueprint, render_template, request, redirect, url_for, flash
from auth import allow
alumni_bp = Blueprint('alumni_bp',__name__,url_prefix='/alumni')
from flask_login import login_required, current_user
from models import Education

@allow('alumni','admin', 'superadmin')
@login_required
@alumni_bp.route('/')
def index():
    
    return render_template('alumni/post.html')


@allow('alumni','admin', 'superadmin')
@login_required
@alumni_bp.route('/education')
def education():
    education = education.query.filter_by(user_id=current_user.id).all()
    
    
    
    return render_template('alumni/education.html', education = education)


