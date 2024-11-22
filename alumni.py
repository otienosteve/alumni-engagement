from flask import Blueprint, current_app, render_template, request, redirect, url_for, flash
from auth import allow
from werkzeug.utils import secure_filename
import datetime
alumni_bp = Blueprint("alumni_bp", __name__, url_prefix="/alumni")
from flask_login import login_required, current_user
from models import Education, Experience, Post,db, PostPhoto, Profile, Plans, Subscription
import uuid, os


@allow("alumni", "admin", "superadmin")
@login_required
@alumni_bp.route("/")
def index():
    posts = Post.query.filter_by(approved=True).order_by(Post.date_posted.desc()).all()

    return render_template("alumni/post.html", posts=posts)


@allow("alumni", "admin", "superadmin")
@login_required
@alumni_bp.route("/", methods=['GET','POST'])
def add_post():
    
    if request.method=='POST':
        data = request.form
        
        new_post = Post(
            body=data.get('body'),
            title=data.get('title'),
            date_posted=datetime.datetime.now(),
            user_id=current_user.id            
        )
        db.session.add(new_post)
        files = files = request.files.getlist('files') 
        for file in files:
            ext = file.filename.split('.')[-1]
            file.filename = str(uuid.uuid4())+'.'+ext
            filename = secure_filename(file.filename)
            file.save(os.path.join('static/user/images/', filename))
            new_post_photo = PostPhoto(photo_url=filename)
            new_post.post_photos.append(new_post_photo)
        db.session.commit()
            
        flash("Post Successful", "success")
        return redirect(request.referrer)



@allow("alumni", "admin", "superadmin")
@login_required
@alumni_bp.route("/education", methods=["POST", "GET"])
def education():
    user_education = Education.query.filter_by(user_id=current_user.id).all()
    if request.method == "POST":
        data = request.form
        new_education = Education(
            start_date=data.get("start-date"),
            end_date=data.get("end-date"),
            user_id=current_user.id,
            name=data.get("name"),
            institution=data.get("institution"),
            course=data.get("course"),
            qualification=data.get("qualification"),
        )
        db.session.add(new_education)
        db.session.commit()
        flash("Education Added", "success")
        return redirect(request.referrer)

    return render_template("alumni/education.html", user_education=user_education)


@allow("alumni", "admin", "superadmin")
@login_required
@alumni_bp.route("/delete_education/<string:education_id>", methods=["POST", "GET"])
def delete_education(education_id):
    education = Education.query.filter_by(id=education_id).delete()
    db.session.commit()
    flash("Education deleted", "danger")
    return redirect(request.referrer)


@allow("alumni", "admin", "superadmin")
@login_required
@alumni_bp.route("/experience", methods=["POST", "GET"])
def experience():
    user_experience = Experience.query.filter_by(user_id=current_user.id).all()
    if request.method == "POST":
        data = request.form
        experience = Experience(
            start_date=data.get("start-date"),
            end_date=data.get("end-date"),
            user_id=current_user.id,
            organisation=data.get("organisation"),
            description=data.get("description"),
            job_title=data.get("job-title"),
        )
        db.session.add(experience)
        db.session.commit()
        flash("Experience Added ", "success")
        return redirect(request.referrer)
    return render_template("alumni/experience.html", user_experience=user_experience)


@allow("alumni", "admin", "superadmin")
@login_required
@alumni_bp.route("/delete_experience/<string:experience_id>", methods=["POST", "GET"])
def delete_experience(experience_id):
    education = Experience.query.filter_by(id=experience_id).delete()
    db.session.commit()
    flash("Experience deleted", "danger")
    return redirect(request.referrer)

@allow("alumni", "admin", "superadmin")
@alumni_bp.route('/profile')
def profile():
    profile= Profile.query.filter_by(user_id=current_user.id).first()
    return render_template('alumni/profile.html', profile=profile)



@allow("alumni", "admin", "superadmin")
@alumni_bp.route('/subscription')
def subscription():
    user_subscriptions = Subscription.query.filter_by(user_id=current_user.id).all()
    print(user_subscriptions)
    return render_template('alumni/subscription.html', user=current_user, user_subscriptions=user_subscriptions)


@alumni_bp.route('/plans')
def plan():
    plans = Plans.query.all()
    plans = [plan.to_dict() for plan in plans ]
    return plans

@alumni_bp.route('/subscribe/<string:user_id>/<string:plan_id>')
def subscribe(user_id, plan_id):
    print(user_id, plan_id)
    new_subscription = Subscription(user_id = user_id, plan_id = plan_id)
    db.session.add(new_subscription)
    db.session.commit()
    return redirect(request.referrer)
    
    