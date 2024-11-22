from flask import Flask,redirect,url_for,render_template,request
from models import db
from flask_migrate import Migrate
from posts import post_bp


from auth import auth_bp, bcrypt, login_manager
from admin import admin_bp
from alumni import alumni_bp
app=Flask(__name__,static_url_path='/static', static_folder='./static')


app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://avnadmin:AVNS_UjlOv7n5pEX0_IFKkdg@mysql-a0c09ce-steveotieno701-7c25.d.aivencloud.com:11033/defaultdb'
app.config['SECRET_KEY']='a6ccbe3bc4bfa0e93fcc0dd814a9b758fc278fa96b7eb0fc4e9d273789c5'
app.config['UPLOAD_FOLDER']='static/user/images'
app.register_blueprint(post_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(alumni_bp)




migrate = Migrate(app=app, db=db)
db.init_app(app)
bcrypt.init_app(app)
login_manager.init_app(app)


# app.register_blueprint(admin_bp)
app.register_blueprint(auth_bp)
