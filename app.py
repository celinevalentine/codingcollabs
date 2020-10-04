from flask import Flask, request, redirect, render_template, flash, session, g, abort, url_for
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post
from forms import RegisterForm, LoginForm, PostForm
from werkzeug.exceptions import Unauthorized
from sqlalchemy.exc import IntegrityError
import requests
from secrets import API_Key

CURR_USER_KEY = "curr_user"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///mealplans'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "SECRET!"
 
app.config['DEBUG_TB_INTERCEPT_REDIRECTS']= False
 
debug = DebugToolbarExtension(app)
 
connect_db(app)
db.create_all()

API_BASE_URL = "https://api.nasa.gov"
# https://images-api.nasa.gov

def pic_of_day(date):
    """get a picture of the day from NASA"""

   
    response = requests.get(f"{API_BASE_URL}/planetary/apod?api_key={API_Key}&date={date}")
    data = response.json()
    title = data['title']
    expl = data['explanation']
    url = data['url']
    info = {"date":date,"title":title, "expl":expl, "url":url }

    return info

    
@app.before_request
def add_user_to_g():
    """Register a user: produce form and handle form submission"""
    
    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None

def do_login(user):
    session[CURR_USER_KEY] = user.id

def do_logout(user):
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.route('/register',methods=['GET','POST'])
def register():
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]
    form = RegisterForm()

    if form.validate_on_submit():
        try:
            user = User.register(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
                first_name=form.first_name.data,
                last_name=form.last_name.data            )
            db.session.commit()

        except IntegrityError as e:
            flash("Username already taken", 'danger')
            return render_template('users/signup.html', form=form)

        do_login(user)

        return redirect("/")

    else:
        return render_template('users/register.html', form=form)
   
@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate():
        user = User.authenticate(form.username.data,form.password.data)

        if user: 
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect('/')
    return render_template('users/login.html',form=form)

@app.route('/logout')
def logout():
    """Handle logout of user."""

    do_logout()

    flash("You have successfully logged out.", 'success')
    return redirect("/login")

@app.route('/')
def homepage():
    """show homepage about project information"""

    return render_template('users/index.html')

@app.route('/users/<username>')
def user_detail(username):

    if "username" not in session or username != session['username']:
        raise Unauthorized()

    user = User.query.get(username)
    form = DeleteForm()

    return render_template("users/show.html", user=user, form=form)

@app.route("/users/<username>/delete", methods=["POST"])
def remove_user(username):
    """Remove user and redirect to login."""

    if "username" not in session or username != session['username']:
        raise Unauthorized()

    user = User.query.get(username)
    db.session.delete(user)
    db.session.commit()
    session.pop("username")

    return redirect("/login")


@app.route("/users/<username>/post/new", methods=["GET", "POST"])
def new_post(username):
    """Show add-feedback form and process it."""

    if "username" not in session or username != session['username']:
        raise Unauthorized()

    form = PostForm()

    if form.validate_on_submit():
        topic = form.topic.data
        summary = form.summary.data
        image_url = form.image_url.data

        post = Post(
            topic=topic,
            summary=summary,
            image_url=image_url
        )

        db.session.add(post)
        db.session.commit()

        return redirect(f"/users/{post.username}")

    else:
        return render_template("posts/new.html", form=form)


@app.route("/posts/<int:post_id>/update", methods=["GET", "POST"])
def edit_post(post_id):
    """Show update-post form and process it."""

    post = Post.query.get(post_id)

    if "username" not in session or post.username != session['username']:
        raise Unauthorized()

    form = PostForm(obj=post)

    if form.validate_on_submit():
        post.topic = form.topic.data
        post.summary = form.summary.data
        post.image_url = form.image_url.data

        db.session.commit()

        return redirect("url_for('edit_post', post_id=post.id)")

    return render_template("posts/edit.html", form=form, post=post)


@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    """Delete a post."""
    post = Post.query.get(post_id)

    if "username" not in session or post.username != session['username']:
        raise Unauthorized()


    form = DeleteForm()

    if form.validate_on_submit():
        db.session.delete(post)
        db.session.commit()

    return redirect(f"/users/{post.username}")
