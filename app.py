from flask import Flask, request, redirect, render_template, flash, session, g, abort, url_for
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, UserApod, APOD
from forms import RegisterForm, LoginForm, UserEditForm
from werkzeug.exceptions import Unauthorized
from sqlalchemy.exc import IntegrityError
import os, requests
from secrets import APOD_API
from helper import get_apod, load_new_apod

CURR_USER_KEY = "curr_user"

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL','postgresql:///codingcollabs')
# app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY','izURL73j^nu24Bp')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///nasa'
app.config['SECRET_KEY'] = 'SECRET'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['DEBUG_TB_INTERCEPT_REDIRECTS']= False
 
debug = DebugToolbarExtension(app)
 
connect_db(app)

##############################################################################
# User signup/login/logout
    
@app.before_request
def add_user_to_g():
    """Register a user: produce form and handle form submission"""
    
    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None

def do_login(user):
    session[CURR_USER_KEY] = user.username

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
            return render_template('users/register.html', form=form)

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
        flash("Invalid credentials.", 'danger')

    return render_template('users/login.html',form=form)

@app.route('/logout')
def logout():
    """Handle logout of user."""
    user = g.user
    do_logout(user)

    flash("You have successfully logged out.", 'success')
    return redirect("/login")

##############################################################################
# General user routes:

@app.route('/')
def landing_page():
    """show landing page for register or sign in"""
    
    return render_template('users/index.html')

@app.route("/users/<username>")
def show_user(username):
    """show profile of an user."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    user = User.query.get(username)

    return render_template("users/detail.html", user=user)

@app.route("/users/<username>/edit", methods=["GET", "POST"])
def edit_user(username):
    """Show update user form and process it."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    user = g.user

    form = UserEditForm(obj=user)

    if form.validate_on_submit():
        # if User.authenticate(user.username, form.password.data):
        # user.username= form.username.data
        user.password = form.password.data
        user.email = form.email.data
        db.session.commit()

        return redirect(f"/users/{username}")
        
        # flash("Wrong password, please try again.", 'danger')

    return render_template("users/edit.html", form=form, user=user)

@app.route("/users/<username>/delete", methods=["POST"])
def remove_user(username):
    """Remove user and redirect to login."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    do_logout(username)

    db.session.delete(g.user)
    db.session.commit()

    return redirect("/register")

##############################################################################
# APOD Routes:


@app.route("/apod")
def show_apod():
    """show apod image"""
    search_date = request.args['search']
    get_apod(search_date)
    load_new_apod()

    apod = APOD.query.all()

    return render_template("apod/show.html",apod=apod)





















##############################################################################
# Homepage and error pages



# @app.errorhandler(404)
# def page_not_found(e):
#     """404 NOT FOUND page."""

#     return render_template('404.html'), 404


##############################################################################
# Turn off all caching in Flask

# @app.after_request
# def add_header(req):
#     """Add non-caching headers on every request."""

#     req.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
#     req.headers["Pragma"] = "no-cache"
#     req.headers["Expires"] = "0"
#     req.headers['Cache-Control'] = 'public, max-age=0'
#     return req