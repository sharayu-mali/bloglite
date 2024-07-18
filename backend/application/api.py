from flask_restful import Resource
from flask_restful import reqparse
from flask_restful import fields, marshal_with
from .models import Blog,User,followers,Likes
from application.validation import BusinessValidationError
from application.database import db
from datetime import datetime
from main import app as app
from flask_security import auth_required
from sqlalchemy.sql import text
from werkzeug.security import generate_password_hash
import os

response_fields = {
    "message": fields.String
}

  
'''
Request Parsers and Output Resource Fields for LikesAPI 
'''

likes_parser = reqparse.RequestParser()

likes_parser.add_argument("user_id")
likes_parser.add_argument("blog_id")
like_fields={
    "user_id":fields.Integer,
}
class LikesAPI(Resource):
    
    @marshal_with(like_fields)
    @auth_required("token")
    def get(self,blog_id=None,user_id=None):
        # Default to 200 OK
        if user_id!=None:
            data=Likes.query.with_entities(Likes.user_id).filter_by(user_id=user_id,blog_id=blog_id).all()
            #print(data)
            return data,200
        if blog_id!=None:
            blog = Blog.query.filter_by(blog_id=blog_id).first()   
            if blog is None:
                raise BusinessValidationError(status_code=404, error_code="ERROR_B01", error_message="Blog not found")   
            else:
                data=Likes.query.with_entities(Likes.user_id).filter_by(blog_id=blog_id).all()
                #print(data)
                return data,200
        
    @auth_required("token")
    @marshal_with(response_fields)
    def post(self):
        args = likes_parser.parse_args() 
        user_id=args.get("user_id", None)
        blog_id=args.get("blog_id", None)
        #print(user_id,blog_id)
        user = db.session.query(User).filter_by(id=user_id).first()   
        if user is None:
            raise BusinessValidationError(status_code=404, error_code="ERROR_U00", error_message="User not found")
        blog = db.session.query(Blog).filter_by(blog_id=blog_id).first()   
        if blog is None:
            raise BusinessValidationError(status_code=404, error_code="ERROR_U00", error_message="Blog not found")
        blog = db.session.query(Blog).filter_by(blog_id=blog_id,user_id=user_id).first()   
        if blog is not None:
            raise BusinessValidationError(status_code=404, error_code="ERROR_U00", error_message="You cannot like your own blog")
        
        exists=db.session.query(Likes).filter_by(user_id=user_id,blog_id=blog_id).first() is not None
        if exists:
            raise BusinessValidationError(status_code=400, error_code="ERROR_U03", error_message="You have already liked the post following user")
        
        add_like = Likes(user_id=user_id,blog_id=blog_id)
        db.session.add(add_like)
        db.session.commit()

        Msg={"message":"Blog Liked"}
        return Msg,200 

    @auth_required("token")
    @marshal_with(response_fields)
    def delete(self,blog_id,user_id):

        exists=db.session.query(Likes).filter_by(user_id=user_id,blog_id=blog_id).first() 
        if exists is  None:
            raise BusinessValidationError(status_code=400, error_code="ERROR_U03", error_message="You have not liked the post")
        
        db.session.delete(exists)
       
        db.session.commit()
        Msg={"message":"Blog Unliked"}
        return Msg,200 
    
'''
Request Parsers and Output Resource Fields for BlogAPI 
'''

blog_parser = reqparse.RequestParser()

blog_parser.add_argument("blog_id" )
blog_parser.add_argument("user_id")
blog_parser.add_argument("blog_name")
blog_parser.add_argument("description")
blog_parser.add_argument("image_loc")
blog_parser.add_argument("uploaded_on")
blog_parser.add_argument("last_updated_on")


blog_fields = {
    "blog_id": fields.String,
    "blog_name": fields.String,
    "description": fields.String,
    "uploaded_on": fields.DateTime(dt_format='iso8601'),
    "image_loc":  fields.String,
    "last_updated_on":fields.DateTime(dt_format='iso8601'),
    "likes": fields.List(fields.Nested(like_fields))
}

blog_resource_fields = {

    "username": fields.String,
    "id": fields.Integer,
    "blogs": fields.List(fields.Nested(blog_fields))
}
class BlogAPI(Resource):

    
    @marshal_with(blog_resource_fields)
    def get(self,user_id=None,blog_id=None):
        # Default to 200 OK
        if blog_id!=None:
            blog = Blog.query.filter_by(blog_id=blog_id).first()   
            if blog is None:
                raise BusinessValidationError(status_code=404, error_code="ERROR_B01", error_message="Blog not found")
            else:
                resp={"blogs":blog,"id":user_id}
                return resp,200
        if user_id!=None:
            data = User.query.filter_by(id=user_id).first()   
            if data is None:
                raise BusinessValidationError(status_code=404, error_code="ERROR_U00", error_message="User not found")
                  
            else:
                return data,200
            
            
    

    @auth_required("token")
    @marshal_with(blog_fields)
    def put(self):
        # Default to 200 OK
        args = blog_parser.parse_args() 
        blog_id=args.get("blog_id",None)
        name=args.get("blog_name", None)
        descr=args.get("description", None)
        #print(blog_id,name,descr,sep="\t")
        if name is None:
            raise BusinessValidationError(status_code=400, error_code="ERROR_B02", error_message="Blog Name is required")
        
        blog = Blog.query.filter_by(blog_id=blog_id).first()   
        if blog is None:
            raise BusinessValidationError(status_code=404, error_code="ERROR_B01", error_message="Blog not found")
                   
        else:
            try:
                blog.blog_name=name
                blog.description=descr
                blog.last_updated_on=datetime.now()
                db.session.commit()
            except Exception as e:
                raise BusinessValidationError(status_code=400, error_code="ERROR_B03", error_message="Blog already exists")
            
        return blog,200
        
    
    @auth_required("token")
    @marshal_with(blog_fields)
    def post(self):
        # Default to 200 OK
        #print("in posts")
        args = blog_parser.parse_args() 
        user_id=args.get("user_id",None)
        name=args.get("blog_name", None)
        descr=args.get("description", None)
        image_loc=args.get("image_loc", None)
        #print(user_id,name,descr,image_loc)
        if name is None:
            raise BusinessValidationError(status_code=400, error_code="ERROR_B02", error_message="Blog Name is required")
        
        data = User.query.filter_by(id=user_id).first()   
        if data is None:
                raise BusinessValidationError(status_code=404, error_code="ERROR_B01", error_message="User not found")       
        else:
            new_blog = Blog(blog_name=name,description=descr,user_id=user_id,image_loc=image_loc)
            blog = Blog.query.filter_by(user_id=user_id ,blog_name=name).first() 
           
            if blog!=None:
                raise BusinessValidationError(status_code=400, error_code="ERROR_B04", error_message="Blog Name already exists.. Please choose another name")
            else:
                db.session.add(new_blog)
                data.no_blogs+=1                
                db.session.commit()
        
        return new_blog,200


    @auth_required("token")
    @marshal_with(response_fields)
    def delete(self,user_id=None,blog_id=None):
        # Default to 200 OK
        if blog_id!=None:
            blog = Blog.query.filter_by(blog_id=blog_id).first()   
          
            if blog is None:
                raise BusinessValidationError(status_code=404, error_code="ERROR_B01", error_message="Blog not found")
            else:
                data = User.query.filter_by(id=user_id).first()   
                if data is None:
                        raise BusinessValidationError(status_code=404, error_code="ERROR_B01", error_message="Blog not found")       
                else:
                    '''likes=Likes.query.filter_by(blog_id=blog_id).all()
                    for like in likes:
                        print(like)
                        db.session.delete(like)
                        db.session.commit()   '''
                    try:
                        os.remove(app.config["UPLOAD_FOLDER"]+'/'+blog.image_loc)
                    except:
                        pass
                    db.session.delete(blog)
                    data.no_blogs-=1
                    db.session.commit()           
        
        Msg={"message":"Successfully Deleted"}
        return Msg,200 
            
'''
Request Parsers and Output Resource Fields for UserAPI 
'''

user_parser = reqparse.RequestParser()

user_parser.add_argument("id", location='form')
user_parser.add_argument("username", location='form')
user_parser.add_argument("password", location='form')
user_parser.add_argument("email", location='form')

user_resource_fields = {
    "id": fields.Integer,
    "username": fields.String,
    "email": fields.String,
    "profile_pic": fields.String,
    "no_blogs": fields.Integer,
    "no_followers": fields.Integer,
    "no_following": fields.Integer,
    "blogs": fields.List(fields.Nested(blog_fields))
    
}

class UserAPI(Resource):

    @auth_required("token")
    @marshal_with(user_resource_fields)
    def get(self,user_id=None):
        # Default to 200 OK
        if user_id!=None:
            data = User.query.filter_by(id=user_id).first()   
            if data is None:
                raise BusinessValidationError(status_code=404, error_code="ERROR_U00", error_message="User not found")
                  
            else:
                return data,200
    
    @auth_required("token")
    @marshal_with(response_fields)
    def put(self):
        args = user_parser.parse_args() 
        username=args.get("username", None)
        email=args.get("email", None)
        password=args.get("password", None)
        user_id=args.get("id",None)
        #print(user_id,username,email,password)
        data = User.query.filter_by(id=user_id).first()   
        if data is None:
                raise BusinessValidationError(status_code=400, error_code="ERROR_U01", error_message="Email address already taken")
        else:
            data.username=username
            data.email=email
            data.password=password
            db.session.commit()

        Msg={"message":"User updated successfully"}
        return Msg,200 
    
    @marshal_with(response_fields)
    def post(self):
        args = user_parser.parse_args() 
        username=args.get("username", None)
        email=args.get("email", None)
        password=args.get("password", None)

        if app.security.datastore.find_user(email=email):
            raise BusinessValidationError(status_code=400, error_code="ERROR_U01", error_message="Email address already taken")
        elif app.security.datastore.find_user(username=username):
            raise BusinessValidationError(status_code=400, error_code="ERROR_U02", error_message="Username already taken")
        else:
            app.security.datastore.create_user(username=username,email=email,password=password,fs_uniquifier=generate_password_hash(password))
            db.session.commit()
        Msg={"message":"User created successfully"}
        return Msg,200 


    @auth_required("token")
    @marshal_with(response_fields)
    def delete(self,user_id=None):
        # Default to 200 OK
        if user_id!=None:
            data = User.query.filter_by(id=user_id).first()   
            if data is None:
                raise BusinessValidationError(status_code=404, error_code="ERROR_U00", error_message="User not found")    
            else:
                db.session.delete(data)
                db.session.commit()      
        Msg={"message":"User deleted successfully"}
        return Msg,200 

            
'''
Request Parsers and Output Resource Fields for FollowerAPI 
'''

follower_parser = reqparse.RequestParser()

follower_parser.add_argument("user_id")
follower_parser.add_argument("follow_id")

follower_resource_fields = {
    "follow_id": fields.Integer
}

class FollowerAPI(Resource):
    
    @marshal_with(follower_resource_fields)
    @auth_required("token")
    def get(self,user_id=None):
        # Default to 200 OK
        if user_id!=None:
            data = User.query.filter_by(id=user_id).first()   
            if data is None:
                raise BusinessValidationError(status_code=404, error_code="ERROR_U00", error_message="User not found")
                  
            else:
                data=db.session.query(followers).filter_by(user_id=user_id).all()
                #print(data)
                return data,200
        
    @auth_required("token")
    @marshal_with(response_fields)
    def post(self):
        args = follower_parser.parse_args() 
        user_id=args.get("user_id", None)
        follow_id=args.get("follow_id", None)
        #print(user_id,follow_id)
        user = db.session.query(User).filter_by(id=user_id).first()   
        if user is None:
            raise BusinessValidationError(status_code=404, error_code="ERROR_U00", error_message="User not found")
        follow = db.session.query(User).filter_by(id=follow_id).first()   
        if follow is None:
            raise BusinessValidationError(status_code=404, error_code="ERROR_U00", error_message="User not found")
        exists=db.session.query(followers).filter_by(user_id=user_id,follow_id=follow_id).first() is not None
        if exists is None:
            raise BusinessValidationError(status_code=400, error_code="ERROR_U03", error_message="You are already following user")
        
        user.followers.append(follow)
        #add_follower = Followers(user_id=user_id,follower_id=follow_id)
        #db.session.add(add_follower)
        user.no_following+=1  
        follow.no_followers+=1
        db.session.commit()

        Msg={"message":"Follower addeed successfully"}
        return Msg,200 

    @auth_required("token")
    @marshal_with(response_fields)
    def delete(self,user_id,follow_id):

        user = db.session.query(User).filter_by(id=user_id).first()   
        if user is None:
            raise BusinessValidationError(status_code=404, error_code="ERROR_U00", error_message="User not found")
        follow = db.session.query(User).filter_by(id=follow_id).first()   
        if follow is None:
            raise BusinessValidationError(status_code=404, error_code="ERROR_U00", error_message="User not found")
        exists=db.session.query(followers).filter_by(user_id=user_id,follow_id=follow_id).first() 
        if exists is  None:
            raise BusinessValidationError(status_code=400, error_code="ERROR_U03", error_message="You are not following user")
        
        query = text("delete from followers where followers.user_id="+str(user_id)+" and followers.follow_id="+str(follow_id))
    
        db.session.execute(query)
       
        user.no_following-=1  
        follow.no_followers-=1
        db.session.commit()      
        Msg={"message":"User Unfollowed"}
        return Msg,200 
    