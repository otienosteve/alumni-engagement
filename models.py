import uuid
from enum import Enum

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import ENUM
from sqlalchemy.sql import func
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin

db= SQLAlchemy()

roles_user = db.Table(
    'roles_user',
    db.Column('role_id', db.String(36), db.ForeignKey('role.id'), primary_key=True),
    db.Column('user_id', db.String(36), db.ForeignKey('users.id'), primary_key=True)
)

school_user = db.Table(
    'school_user',
    db.Column('school_id', db.String(36), db.ForeignKey('school.id'), primary_key=True),
    db.Column('user_id', db.String(36), db.ForeignKey('users.id'), primary_key=True)
)
class titleEnum(Enum):
    mr = 'mr'
    miss = 'miss'
    mrs = 'mrs'
    dr = 'dr'
    prof = 'prof'



class User(db.Model,UserMixin, SerializerMixin):
    __tablename__ = 'users'
    serialize_rules = ('-profile','-posts','-education','-school','-role')
    id = db.Column(db.String(36), nullable=False, unique=True, default=uuid.uuid4, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    confirmed = db.Column(db.Boolean, default=False)
    referral_code = db.Column(db.String(255))
    confirmation_code = db.Column(db.String(36))
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    school = db.relationship('School', secondary=school_user, back_populates='user')
    profile = db.relationship('Profile', back_populates='user', uselist=False)
    role = db.relationship(
        'Role',secondary=roles_user,back_populates='user')
    education = db.relationship('Education', back_populates='user')
    posts =  db.relationship('Post',back_populates='user')
    subscriptions = db.relationship('Subscription', back_populates='user')
    
    
class statusEnum(Enum):
    pending = 'pending'
    fulfilled = 'fulfilled'

class RegistrationRequest(db.Model,SerializerMixin):
    id = db.Column(db.String(36), nullable=False, unique=True, default=uuid.uuid4, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    title = db.Column(ENUM(titleEnum))
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    school = db.Column(db.String(255))
    status = db.Column(ENUM(statusEnum))
    
    
    
class Profile(db.Model):
    __tablename__ = 'profile'
    id = db.Column(db.String(36), nullable=False, unique=True, default=uuid.uuid4, primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'))
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    photo_url = db.Column(db.String(255))
    title = db.Column(ENUM(titleEnum))
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    # relationship with user
    user = db.relationship('User', back_populates='profile', uselist=False)
    


class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.String(36), nullable=False, unique=True, default=uuid.uuid4, primary_key=True)
    name = db.Column(db.String(20))
    user = db.relationship(
        'User',secondary=roles_user,back_populates='role')
    
    
class School(db.Model):
    __tablename__='school' 
    id = db.Column(db.String(36), nullable=False, unique=True, default=uuid.uuid4, primary_key=True)
    name = db.Column('name', db.String(255))
    user = db.relationship('User', secondary=school_user, back_populates='school')


class Course(db.Model):
    __tablename__='course' 
    id = db.Column(db.String(36), nullable=False, unique=True, default=uuid.uuid4, primary_key=True)
    name=  db.Column('name', db.String(255))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'))
    level =  db.Column('level', db.String(255))
    start_date = db.Column('start_date', db.Date)
    end_date = db.Column('end_date', db.Date)
    qualification =  db.Column('qualification', db.String(255))



class Education(db.Model):
    id = db.Column(db.String(36), nullable=False, unique=True, default=uuid.uuid4, primary_key=True)
    qualification  = db.Column( db.String(255))
    institution  = db.Column( db.String(255))
    name = db.Column( db.String(255))
    course = db.Column( db.String(255))
    start_date=  db.Column('start_date', db.DateTime, nullable= False)
    end_date=  db.Column('end_date', db.DateTime)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'))
    user = db.relationship('User', back_populates='education')
    
    
    
class Events(db.Model):
    __table_name__ = 'events'
    id = db.Column(db.String(36), nullable=False, unique=True, default=uuid.uuid4, primary_key=True)
    name=   db.Column( db.String(255))
    description =db.Column( db.Text)
    start_date=  db.Column('start_date', db.DateTime)
    end_date=  db.Column('end_date', db.DateTime)
    image =db.Column( db.String(255))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'))




class Experience(db.Model):
    __table_name__ = 'experience'
    id = db.Column(db.String(36), nullable=False, unique=True, default=uuid.uuid4, primary_key=True)
    organisation = db.Column(db.String(255))
    job_title =db.Column(db.String(255))
    description =db.Column(db.Text)
    start_date=  db.Column( db.DateTime)
    end_date=  db.Column( db.DateTime)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'))
    



class Membership(db.Model):
    __tablename__='membership'
    id = db.Column(db.String(36), nullable=False, unique=True, default=uuid.uuid4, primary_key=True)
    amount= db.Column( db.Float(6,3))
    date_paid= db.Column( db.Date)
    expires= db.Column( db.Date)
    user_id= db.Column( db.Integer())



class Mentee(db.Model):
    __tablename__ ='mentee'
    id = db.Column(db.String(36), nullable=False, unique=True, default=uuid.uuid4, primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'))
    mentor_id = db.Column(db.String(36), db.ForeignKey('mentor.id'))
    start_date=  db.Column( db.DateTime)
    end_date=  db.Column( db.DateTime)



class Mentor(db.Model):
    __tablename__ = 'mentor'
    id = db.Column(db.String(36), nullable=False, unique=True, default=uuid.uuid4, primary_key=True)
    user_id= db.Column(db.Integer())
    description= db.Column(db.Text)


class Post(db.Model, SerializerMixin):
    __tablename__ ='post'
    serialize_rules = ('-post_photos.post','user.email', '-user.posts')
    id = db.Column(db.String(36), nullable=False, unique=True, default=uuid.uuid4, primary_key=True)
    title = db.Column(db.String(255))
    body = db.Column(db.Text)
    date_posted = db.Column(db.DateTime)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'))
    approved = db.Column(db.Boolean, default=False)
    # approved_by = db.Column(db.String(36), db.ForeignKey('users.id'))
    post_photos = db.relationship('PostPhoto', back_populates='post')
    user =  db.relationship('User',back_populates='posts')
class PostPhoto(db.Model, SerializerMixin):
    __tablename__ ='post_photo'
    id = db.Column(db.String(36), nullable=False, unique=True, default=uuid.uuid4, primary_key=True)
    photo_url = db.Column(db.String(255))
    post_id = db.Column(db.String(36), db.ForeignKey('post.id'))
    post = db.relationship('Post', back_populates='post_photos')
    

class Email(db.Model):
    __tablename__ ='email'
    id = db.Column(db.String(36), nullable=False, unique=True, default=uuid.uuid4, primary_key=True)
    subject = db.Column(db.String(255))
    body = db.Column(db.Text)
    sender_email = db.Column(db.String(255))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'))
    
class MailingList(db.Model):
    __tablename__ = 'mailing_list'
    id = db.Column(db.String(36), nullable=False, unique=True, default=uuid.uuid4, primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'))
    email_id = db.Column(db.String(36), db.ForeignKey('email.id'))


class Skill(db.Model):
    __tablename__ = 'skills'
    id = db.Column(db.String(36), nullable=False, unique=True, default=uuid.uuid4, primary_key=True)
    name = db.Column(db.String(255))


class Plans(db.Model, SerializerMixin):
    __tablename__ = 'plan'
    serialize_rules = ('-subscriptions',)
    id = db.Column(db.String(36), nullable=False, unique=True, default=uuid.uuid4, primary_key=True)
    name = db.Column(db.String(255))
    days = db.Column(db.Integer)
    amount = db.Column(db.Float)
    subscriptions = db.relationship('Subscription', back_populates='plan')

class Subscription(db.Model):
    id = db.Column(db.String(36), nullable=False, unique=True, default=uuid.uuid4, primary_key=True)
    subscription_date = db.Column(db.DateTime, server_default=func.now())
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'))
    plan_id = db.Column(db.String(36), db.ForeignKey('plan.id'))
    user = db.relationship('User', back_populates='subscriptions')
    plan = db.relationship('Plans', back_populates='subscriptions')
    

  

    
    
    
