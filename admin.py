from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import Post,RegistrationRequest, User,Subscription, db, Plans, Subscription, Events
import uuid
import os
from werkzeug.utils import secure_filename
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

@admin_bp.route('/posts')
def posts():
    posts = []
    approved = request.args.get('approved')
    if approved == 'True':
        posts = Post.query.filter_by(approved=True).all() 
    if approved == 'False':
        posts = Post.query.filter_by(approved=False).all() 
        
    return render_template('admin/post.html', posts=posts)
    
@admin_bp.route('/ajax-request-post/<string:id>')
def ajax_request_post(id):
    post = Post.query.filter_by(id=id).first()
    return post.to_dict()

@admin_bp.route('/approve_post/<string:post_id>')
def approve_post(post_id):

    post = Post.query.filter_by(id=post_id).first()
    post.approved= True 
    db.session.commit()
    
    return redirect(request.referrer)



@admin_bp.route('/plans', methods=['GET', 'POST'])
def plans():
    plans = Plans.query.all()
    if request.method=='POST':
        data = request.form
        print(data)
        new_plan = Plans(
            name= data.get('name'),
            days= data.get('days'),
            amount= data.get('amount')
        )
        db.session.add(new_plan)
        db.session.commit()
        return redirect(request.referrer)
    return render_template('admin/plans.html', plans =plans)
    
@admin_bp.route('/delete_plan/<string:plan_id>')
def delete_plan(plan_id):
    plan = Plans.query.filter_by(id=plan_id).delete()
    db.session.commit()
    flash('Plan deleted','danger')
    return redirect(request.referrer)



@admin_bp.route('/events', methods=['GET','POST'])
def events():
    all_events = Events.query.all()
    if request.method=='POST':
        file  = request.files.get('image') 
        print(file)
        data = request.form
        if file:
            ext = file.filename.split('.')[-1]
            file.filename = str(uuid.uuid4())+'.'+ext
            filename = secure_filename(file.filename)
            file.save(os.path.join('static/user/images/', filename))
            new_event = Events(name=data.get('name'),
                           description=data.get('description'),
                           start_date=data.get('start-date'),
                           end_date=data.get('end-date'),
                           image=filename)
            db.session.add(new_event)
            print(new_event)
            db.session.commit()
        else:
            new_event = Events(name=data.get('name'),
                           description=data.get('description'),
                           start_date=data.get('start-date'),
                           end_date=data.get('end-date'),
                           )
            db.session.add(new_event)
        return redirect(request.referrer)
    return render_template('admin/events.html', events=all_events)
    
@admin_bp.route('/delete_event/<string:event_id>')
def delete_event(event_id):
    event = Events.query.filter_by(id=event_id).delete()
    db.session.commit()
    flash("Event Deleted Successfully", 'danger')
    return redirect(request.referrer)

    
@admin_bp.route('/subscription')
def subscription():
    subscriptions = Subscription.query.all()
    
    return render_template('admin/subscription.html', subscriptions=subscriptions)