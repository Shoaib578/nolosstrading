from flask import Blueprint,jsonify,request,render_template
from application import db,app
from werkzeug.security import generate_password_hash,check_password_hash
from application.models import User,Blog,BlogSchema

import os
from sqlalchemy import text
from datetime import datetime
from werkzeug.utils import secure_filename
from flask_login import login_user, current_user, logout_user, login_required
import requests


main = Blueprint('main', __name__,static_folder='../static')



@main.route("/")
def LandingPage():
    
    return render_template('main/landing_page.html')


@main.route("/about")
def About():
    return render_template('main/about.html')

@main.route("/blogs")
def Blogs():
    blogs = Blog.query.all()
    return render_template('main/blogs.html',blogs=blogs)


@main.route('/search_by_category/<string:category>')
def SearchByCategory(category):
    blogs = Blog.query.filter_by(blog_category=category).all()
    return render_template('main/blogs.html',blogs=blogs)

    
@main.route('/search_blog')
def SearchByKeywords():
    keywords = request.args.get('keywords')
    query = text("SELECT * FROM Blog WHERE blog_title LIKE '%"+str(keywords)+"%' OR blog_description LIKE '%"+str(keywords)+"%'")
    engine = db.engine.execute(query)
    schema = BlogSchema(many=True)
    blogs = schema.dump(engine)
    return render_template("main/blogs.html",blogs=blogs)


@main.route("/view_blog/<int:id>")
def ViewBlog(id):
    blog = Blog.query.get(id)
    return render_template('main/view_blog.html',blog=blog)


@main.route("/slides")
def Slides():
    return render_template('main/slides.html')