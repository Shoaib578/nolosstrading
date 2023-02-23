from application import db,login_manager,ma

from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))



class User(db.Model,UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(100),nullable=True)
    
    password = db.Column(db.String(200),nullable=False)
    is_admin = db.Column(db.Integer())


class Blog(db.Model):
    blog_id = db.Column(db.Integer(), primary_key=True)
    blog_title = db.Column(db.String(300),nullable=True)
    blog_category = db.Column(db.String(300),nullable=True)
    blog_description = db.Column(db.String(2000),nullable=True)
    blog_image = db.Column(db.String(200),nullable=True)
    added_date = db.Column(db.Date())
    
class BlogSchema(ma.Schema):
    class Meta:
        fields = ('blog_id','blog_description','blog_title','blog_image','added_date')
