
from flask import Flask, render_template, request, session, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_mail import Mail
from werkzeug.utils import secure_filename
import json
import os
import math


with open("config.json", "r") as c:
    params= json.load(c)["params"]
local_server=True

app = Flask(__name__)
app.secret_key = "super-secret-key"
app.config['UPLOAD_FOLDER'] = params['upload_location']

app.config.update(MAIL_SERVER ="smtp.gmail.com", MAIL_PORT = "465", MAIL_USE_SSL = True, MAIL_USERNAME = params['user_id'], MAIL_PASSWORD = params['user_password'])
mail=Mail(app)

if(local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = params["local_uri"]
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params["prod_uri"]
    
db = SQLAlchemy(app)

class Contacts(db.Model):
    sr_no = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    phone_no = db.Column(db.String(12), nullable=False)
    message = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12), nullable=True)

class Posts(db.Model):
    post_no = db.Column(db.Integer, primary_key=True)
    post_title = db.Column(db.String(80), nullable=False)
    slug = db.Column(db.String(30), nullable=False)
    post_content = db.Column(db.String(500), nullable=False)
    post_date = db.Column(db.String(12), nullable=True)
    post_img = db.Column(db.String(12), nullable=True)
   
#HOME page
@app.route("/")
def home():
    posts= Posts.query.filter_by().all()
    last = math.ceil(len(posts)/int(params['no_of_posts']))
    #pagination logic
    page = request.args.get('page')
    if (not str(page).isnumeric()):
        page = 1
    page = int(page)
    posts = posts[(page-1)*int(params['no_of_posts']) : (page-1)*int(params['no_of_posts']) + int(params['no_of_posts'])]
    if (page==1):
        prev = "#"
        next = "/?page=" + str(page+1)
    elif (page==last):
        prev = "/?page=" + str(page-1)
        next = "#"
    else:
        prev = "/?page=" + str(page-1)
        next = "/?page=" + str(page+1)

    return render_template("index.html", params=params, posts=posts, prev=prev, next=next)

#Posts on home page
@app.route("/post/<string:post_slug>", methods=["GET"])
def post_route(post_slug):
    post = Posts.query.filter_by(slug=post_slug).first()
    return render_template("post.html", params=params, post=post)

#ABOUT page
@app.route("/about")
def about():
    return render_template("about.html", params=params)

#ADMIN LOGIN page
@app.route("/dashboard", methods=['GET','POST'])
def dashboard():
    if ('user' in session and session['user'] == params['admin_name']):
        posts = Posts.query.all()
        return render_template("dashboard.html", params=params, posts=posts)

    if request.method=='POST':
        username = request.form.get('uname')
        userpass = request.form.get('pass')
        if (username == params['admin_name'] and userpass == params['admin_password']):
            session['user'] = username 
            posts = Posts.query.all()
            return render_template("dashboard.html", params=params, posts= posts)

    return render_template("login.html", params=params)

#hidden Area
@app.route("/secretlogin", methods=['GET','POST'])
def secretcode():
    if ('secret' in session and session['secret'] == params['admin_name']):
        return render_template("secretcode.html", params=params)

    if request.method=='POST':
        username = request.form.get('usname')
        userpass = request.form.get('upass')
        if (username == params['admin_name'] and userpass == params['admin_password']):
            session['secret'] = username 
            return render_template("secretcode.html", params=params)

    return render_template("secretlogin.html", params=params)
#Exit Button
@app.route("/exit")
def exit():
    session.pop('secret')
    return redirect('/')

#ADD/EDIT Posts
@app.route("/edit/<string:post_no>", methods = ['GET', 'POST'])
def edit(post_no):
    if ('user' in session and session['user'] == params['admin_name']):
        if request.method == 'POST':
            title = request.form.get('title')
            slug = request.form.get('slug')
            content = request.form.get('content')
            img = request.form.get('img')
            date = datetime.now()

            if post_no == "0":
                post=Posts(post_title =title, slug=slug, post_content=content, post_img=img, post_date=date)
                db.session.add(post)
                db.session.commit()
            else:
                post = Posts.query.filter_by(post_no=post_no).first()
                post.post_title = title
                post.slug = slug
                post.post_content = content
                post.post_img = img
                post.post_date = date
                db.session.commit()
                return redirect('/edit/'+post_no)
        post = Posts.query.filter_by(post_no=post_no).first()
        return render_template('edit.html', params=params, post=post, post_no = post_no)

#FILE Uploader
@app.route("/uploader", methods = ['GET', 'POST'])
def uploader():
    if ('user' in session and session['user'] == params['admin_name']):
        if(request.method=='POST'):
            f = request.files['file1']
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
            return "Uploaded Successfully"
            
#LOGOUT Button
@app.route("/logout")
def logout():
    session.pop('user')
    return redirect('/dashboard')

#POST Deleter
@app.route("/delete/<string:post_no>", methods = ['GET', 'POST'])
def delete(post_no):
    if ('user' in session and session['user'] == params['admin_name']):
        post = Posts.query.filter_by( post_no = post_no).first()
        db.session.delete(post)
        db.session.commit()
        return redirect('/dashboard')
            
#CONTACT page
@app.route("/contact", methods = ['GET', 'POST'])
def contact():
    if(request.method=='POST'):
        '''adding entry to database'''
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')
    
        entry = Contacts(name=name, email=email, phone_no=phone, date=datetime.now(),  message=message)
        db.session.add(entry)
        db.session.commit()
        
        mail.send_message('New Message from your Website by '+ name, sender = email, recipients = [params["user_id"]], body = message + "\n" + phone)
        
    return render_template("contact.html", params=params)


app.run(debug=False, host='0.0.0.0')