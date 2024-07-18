from .database import db
from datetime import datetime
from flask_security import UserMixin,RoleMixin
from werkzeug.security import generate_password_hash, check_password_hash

roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))    


followers = db.Table('followers',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('follow_id', db.Integer(), db.ForeignKey('user.id')))  

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id=db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    username = db.Column(db.String, unique=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String(255))
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    last_updated_on = db.Column(db.DateTime, default=datetime.utcnow)
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False) 
    active = db.Column(db.Boolean())
    
    no_followers = db.Column(db.Integer,default=0)
    no_following = db.Column(db.Integer,default=0)
    no_blogs = db.Column(db.Integer,default=0)
    roles = db.relationship('Role', secondary=roles_users,backref=db.backref('user', lazy='dynamic'))
    blogs = db.relationship('Blog', backref=db.backref('user'))
    followers = db.relationship(
                    'User',secondary=followers,
                    primaryjoin=followers.c.user_id==id,
                    secondaryjoin=followers.c.follow_id==id,
                    backref="followees")
    
    db.relationship('User', secondary=followers,backref=db.backref('user', lazy='dynamic'))
    
    def verify_password(self, pwd):
        
        return check_password_hash(self.password, pwd)

class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class Blog(db.Model):
    __tablename__ = 'blog'
    blog_id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer,   db.ForeignKey("user.id"), nullable=False)
    blog_name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    image_loc = db.Column(db.String, nullable=False)
    uploaded_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    last_updated_on = db.Column(db.DateTime, default=datetime.utcnow)
    likes = db.relationship('Likes', backref=db.backref('blog'),cascade="all,delete", passive_deletes=True)


class Likes(db.Model):
    __tablename__ = 'likes'    
    user_id = db.Column(db.Integer,   db.ForeignKey("user.id"), primary_key=True, nullable=False)
    blog_id = db.Column(db.Integer,   db.ForeignKey("blog.blog_id", ondelete="CASCADE"), primary_key=True,nullable=False)