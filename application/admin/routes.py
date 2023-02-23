from flask import Blueprint,jsonify,request,render_template,flash,redirect,url_for
from application import db,app
from werkzeug.security import generate_password_hash,check_password_hash
from application.models import User,Blog
import os
from sqlalchemy import text
from datetime import datetime
from werkzeug.utils import secure_filename
from flask_login import login_user, current_user, logout_user, login_required
import requests
import random
from datetime import datetime
import tweepy
import facebook


# Twitter Keys
twitter_api_key = "..."
twitter_api_secrets = "..."
twitter_access_token = "..."
twitter_access_secret = "..."
 
# Authenticate to Twitter
twitter_auth = tweepy.OAuthHandler(twitter_api_key,twitter_api_secrets)
twitter_auth.set_access_token(twitter_access_token,twitter_access_secret)
twitter = tweepy.API(twitter_auth)



#Facebook Keys
facebook_page_id = 109998795333855
facebook_access_token = 'EAAP3lBUoDhkBAA8SiPSRbHLEMK38yEjWkAryoRYtM9ZBdd8NffNea2r9AZCZBUG65m9cEfWRCXvhyIe6qcICxjJGJyPylWm3iTKhBC0k16np1ZCGlx2fV7YsgtZAi8ZCD68ZBz7ze9FwhZB9Vf6uRmt5ZB1NV2ZBLCmUpWusZAAELrayvn2jAhPoyYas7yPtxsumJogKiOPSzZBD7VtUpO5RNG8jYOro25TSwwcZD'

admin = Blueprint('admin', __name__,static_folder='../static')






def remove_file(file, type):
    file_name = file
    folder = os.path.join(app.root_path, "static/" + type + "/"+file_name)
    os.remove(folder)
    return 'File Has Been Removed'


def save_file(file, type):
    file_name = secure_filename(file.filename)
    file_ext = file_name.split(".")[1]
    folder = os.path.join(app.root_path, "static/" + type + "/")
    file_path = os.path.join(folder, file_name)
    try:
        file.save(file_path)
        return True, file_name
    except:
        return False, file_name


def PostTwitter(blog_description,blog_image):
    imagePath = url_for('static',filename="uploads/"+blog_image)
    status = blog_description
    api.update_with_media(imagePath, status)
    return "Posted on twitter"



def PostFacebook(blog_description,blog_image):
   
    post_url = 'https://graph.facebook.com/{}/feed'.format(facebook_page_id)
    payload = {
    'title': "hello there",
    'access_token': facebook_access_token
    }
    r = requests.post(post_url, data=payload)
    print(r.text)

    return "Posted on facebook"


def PostTelegram(blog_description,blog_image):
    apiToken = '6017200918:AAGHn1kukC-Qqr0kfV7_n9VmEGnySkf9RnI'
    chatID = '5677641767'
    apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'

    try:
        response = requests.post(apiURL, json={'chat_id': chatID, 'text': message,'photo':url_for('static',filename='uploads/'+blog_image)})
        print(response.text)
    except Exception as e:
        print(e)
    return "Uploaded on telegram"

@admin.route('/admin/login',methods=['GET', 'POST'])
def Login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        admin = User.query.filter_by(email=email).first()
        if admin and check_password_hash(admin.password, password):
            login_user(admin)
            return redirect(url_for('admin.Index'))
            
    return render_template("admin/login.html")


@admin.route("/admin",methods=["GET", "POST"])
@login_required
def Index():
    if request.method == "POST":
        blog_title = request.form.get('blog_title')
        blog_description = request.form.get('blog_description')
        blog_image = request.files.get('blog_image')
        blog_category = request.form.get('blog_category')
        save_file(blog_image,"uploads")
        blog = Blog(blog_title=blog_title,blog_description=blog_description,blog_image=blog_image.filename,blog_category=blog_category,added_date=datetime.today())
        db.session.add(blog)
        db.session.commit()
      

        flash("Added Successfully")
        return redirect(url_for('admin.Index'))

    blogs = Blog.query.filter_by(blog_category="us stock market").all()

    return render_template("admin/index.html",blogs=blogs)


@admin.route("/admin/india_stock",methods=["GET", "POST"])
@login_required
def IndiaStockMarket():
    if request.method == "POST":
        blog_title = request.form.get('blog_title')
        blog_description = request.form.get('blog_description')
        blog_image = request.files.get('blog_image')
        blog_category = request.form.get('blog_category')
        save_file(blog_image,"uploads")
        blog = Blog(blog_title=blog_title,blog_description=blog_description,blog_image=blog_image.filename,blog_category=blog_category,added_date=datetime.today())
        db.session.add(blog)
        db.session.commit()
        flash("Added Successfully")
        return redirect(url_for('admin.IndiaStockMarket'))

    blogs = Blog.query.filter_by(blog_category="indian stock market").all()
    print(blogs)
    return render_template("admin/india_stock.html",blogs=blogs)


@admin.route('/admin/delete_indian_stock_blog/<int:id>')
@login_required
def DeleteIndianStockBlog(id):
    blog = Blog.query.get_or_404(id)
    remove_file(blog.blog_image,"uploads")

    db.session.delete(blog)
    db.session.commit()
    flash("Deleted Successfully")
    return redirect(url_for('admin.IndiaStockMarket'))



@admin.route('/admin/delete_us_stock_blog/<int:id>')
@login_required
def DeleteUsStockBlog(id):
    blog = Blog.query.get_or_404(id)
    remove_file(blog.blog_image,"uploads")
    db.session.delete(blog)
    db.session.commit()
    flash("Deleted Successfully")
    return redirect(url_for('admin.Index'))

@admin.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("admin.Login"))