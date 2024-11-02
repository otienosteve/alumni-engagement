from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import RegistrationRequest, User

admin_bp=Blueprint('admin_bp',__name__, url_prefix='/admin')

@admin_bp.route('/')
def main_dashboard():
    
    return render_template('admin/index.html')

@admin_bp.route('/register_requests')
def register_requests():
    registration_requests = RegistrationRequest.query.all()
    return render_template('admin/admin-register-requests.html',registration_requests=registration_requests)
    
@admin_bp.route('/ajax-register-request/<string:id>')
def ajax_request(id):
    register_request = RegistrationRequest.query.filter_by(id=id).first()
    return register_request.to_dict()
    
@admin_bp.route('/users')
def users():
    all_users = User.query.all()
    return render_template('/admin/users.html', users=all_users)
