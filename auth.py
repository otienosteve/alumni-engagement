import datetime
import uuid
import os
from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from functools import wraps
from forms import RegisterForm,RequestRegisterForm, LoginForm,PasswordResetForm, UpdateProfileForm
from models import User, db, Role, School, Profile, RegistrationRequest
from utils import generate_confirmation_code,generate_token
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


bcrypt = Bcrypt()
login_manager = LoginManager()

auth_bp = Blueprint('auth', __name__,url_prefix='/auth', template_folder='templates')
login_manager = LoginManager()
login_manager.login_view = "auth.login"

def allow(*roles):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            user_roles = [role.name for role in current_user.role]
            for role in roles:
                if role in user_roles:
                    return fn(*args, **kwargs)
            else:
                return redirect(url_for('auth.forbidden'))
        return decorator
    return wrapper

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            code = generate_confirmation_code()
            password = generate_confirmation_code()
            hashed_password = bcrypt.generate_password_hash(password)
            new_user = User(email=form.data.get('email'),password=hashed_password, confirmation_code=code)
            school = School(name=form.data.get('school'))
            new_user.school.append(school)   
            profile = Profile(last_name= form.data.get('last_name'),first_name= form.data.get('first_name'),title=form.data.get('title'))  
            role = Role.query.filter_by(name='alumni').first()
            new_user.profile=profile
            new_user.role.append(role)
            db.session.add(new_user)
            db.session.commit()
            # msg = Message(subject='Welcome to Parish MIS', sender='administration@niclex.com', recipients=[form.data['email']])
            # msg.body = "Welcome to Niclex, Your confirmation Code is "+code
            # mail.send(msg)
            return redirect(url_for('auth.login'))
    else:
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f'Error in field "{getattr(form, field).label.text}": {error}', 'error')

    return render_template('auth/register.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            payload = form.data
            user = User.query.filter_by(email=payload.get('email')).first()
            if not user: 
                flash(f'User with email {payload["email"]} does not exist!', 'error')
                return render_template('auth/login.html', form=form)
            if bcrypt.check_password_hash(user.password, payload.get('password')):
                login_user(user)
                flash('Welome to Firm Roots', category='success')
                return redirect(url_for('admin_bp.dashboard'))
            else:
                flash('Incorrect Password Entered', 'error')
                return render_template('auth/login.html', form=form)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f'Error in field "{getattr(form, field).label.text}": {error}', 'error')
            return render_template('auth/login.html', form=form)
    return render_template('auth/login.html', form=form)

@auth_bp.route('/confirm_email', methods=['POST','GET'])
@login_required
def confirm_email():
    code = request.args.get('code')
    if request.method =='POST':
        code = request.form.get('confirmation_code')
        user = User.query.filter_by(id=current_user.id).first()
        if code == user.confirmation_code:
            user.confirmed = True
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('user_bp.branch'))
        else:
            flash('Wrong Confirmation code or Confirmation Code expired','warning')
            return render_template('auth/confirm_email.html', code = code)

    return render_template('auth/confirm_email.html', code = code)

@auth_bp.route('/resend_confirmation_code')
@login_required
def resend_confirmation_code():
    user = User.query.filter_by(id=current_user.id).first()
    code = generate_confirmation_code()
    user.confirmation_code = code 
    db.session.add(user)
    db.session.commit()
    msg = Message(subject='Confirmation', sender='administration@niclex.com', recipients=[current_user.email])
    msg.body = "Your New confirmation Code is "+code
    mail.send(msg)
    flash('Another confirmation code has been sent','resent')
    return redirect(url_for('auth.confirm_email'))

@auth_bp.route('/password_reset', methods=['GET', 'POST'])
def reset_password():
     if request.method=='POST':
        user = User.query.filter_by(email=request.form.get('email')).first()
        if not user:
            flash(f'User With Email: {request.form.get("email")} Not Found','failure')
            return render_template("auth/request_reset_password.html")
        flash('sending link', 'dispatched')
        token = generate_token()
        password_reset =  PasswordReset(reset_code=token,request_status=False,expires=datetime.datetime.now() + datetime.timedelta(minutes=4))
        user.password_reset.append(password_reset)
        db.session.add(password_reset)
        db.session.commit()
        msg = Message(subject='Niclex[Password Reset]', sender='administration@niclex.com', recipients=[request.form.get('email')])
        msg.body = f"Follow the Link Below to Reset your Password \n{request.url_root}/reset_password/{token} \nLink Expires in 4 mins"
        mail.send(msg)
        flash(f'Password Reset Link  Has Been Sent to Email: {request.form.get("email")}','success')
     
     return render_template("auth/request_reset_password.html")

@auth_bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password_form(token):
    form = PasswordResetForm()
    password_reset= PasswordReset.query.filter_by(reset_code=token).first()
    if not password_reset:
        flash('Invalid Request Link Request Another')
    if password_reset.expires <  datetime.datetime.now():
         flash('Reset Link Has Expired')
    if request.method == 'POST':
        if form.validate_on_submit():
            password = form.data.get('password')
            hashed_password = generate_password_hash(
                password, method='pbkdf2')
            user = User.query.filter_by(id=password_reset.user_id).first()
            user.password=hashed_password
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('auth.login'))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f'Error in field "{getattr(form, field).label.text}": {error}', 'error')
        
       
    return render_template('auth/reset_password.html', token=token, form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("user_bp.branch"))

@auth_bp.route('/profile')
def profile():
    profile = Profile.query.filter_by(user_id=current_user.id).first()

    return render_template('auth/profile.html', profile=profile)

@auth_bp.route('/update_profile',methods=['GET','POST'])
def update_profile():
    profile = Profile.query.filter_by(user_id=current_user.id).first()
    if not profile:
        profile = Profile(user_id=current_user.id)
    form = UpdateProfileForm()
    if request.method =='POST':
        if form.validate_on_submit():
            file = form.data.get('photo_url')
            if file:
                ext = file.filename.split('.')[-1]
                file.filename = str(uuid.uuid4())+'.'+ext
                filename = secure_filename(file.filename)
                file.save(os.path.join(os.environ.get('UPLOAD_FOLDER'), filename))
                profile.photo_url = filename
            for key, value in form.data.items():
                if value is not None and key != 'photo_url':
                    setattr(profile, key, value)
            db.session.add(profile)
            db.session.commit()
            return redirect(url_for('auth.profile'))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f'Error in field "{getattr(form, field).label.text}": {error}', 'error')  

    return render_template('auth/update_profile.html', profile=profile, form=form)

@auth_bp.route('/access_denied')
def forbidden():

    return render_template('auth/503.html')


@auth_bp.route('/request_register', methods=['GET','POST'])
def request_registration():
    form = RequestRegisterForm()
    if request.method=='POST':
        if form.validate_on_submit():
            registration_request = RegistrationRequest(email= form.data.get('email'),
                                                       title=form.data.get('title'),
                                                       first_name=form.data.get('first_name'),
                                                       last_name=form.data.get('last_name'),
                                                       school=form.data.get('school'))
            db.session.add(registration_request)
            db.session.commit() 
            flash('Registration Request Successful, We Typically reply with an email in 2-3 days with login details, Looking forward to engaging with you')
    
    return render_template('auth/request-register.html', form=form)

