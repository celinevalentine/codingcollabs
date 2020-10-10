from flask import Flask, request, redirect, render_template, flash, session, g, abort, url_for
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Project
from forms import RegisterForm, LoginForm, AddProjectForm
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
    form = DeleteForm()

    return render_template("users/detail.html", user=user, form=form)

 @app.route("/users/<username>/edit", methods=["GET", "POST"])
def edit_user(username):
    """Show update user form and process it."""

    user = User.query.get(username)

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    form = UserForm(obj=post)

    if form.validate_on_submit():
        user.username = form.username.data
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.email = form.email.data

        db.session.commit()

        return redirect("url_for('edit_user', username=username)")

    return render_template("users/edit.html", form=form, post=post)

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


@app.route(f"/projects/{project.id}/new", methods=["GET", "POST"])
def new_project(username):
    """Add the project form and process it."""

    if "username" not in session or username != session['username']:
        raise Unauthorized()

    form = AddProjectForm()

    if form.validate_on_submit():
        name = form.name.data
        technology = form.technology.data
        about = form.about.data
        level = form.level.data
        link = form.link.data

        project = Project(
            name=name,
            technology=technology,
            about=about,
            level=level,
            link=link,
            username=username
        )

        db.session.add(project)
        db.session.commit()


        return redirect (f"/user/{project.username}")

    else:
        return render_template("projects/new.html", form=form)


# @app.route("/posts/<int:post_id>/update", methods=["GET", "POST"])
# def edit_post(post_id):
#     """Show update-post form and process it."""

#     post = Post.query.get(post_id)

#     if "username" not in session or post.username != session['username']:
#         raise Unauthorized()

#     form = PostForm(obj=post)

#     if form.validate_on_submit():
#         post.topic = form.topic.data
#         post.summary = form.summary.data
#         post.image_url = form.image_url.data

#         db.session.commit()

#         return redirect("url_for('edit_post', post_id=post.id)")

#     return render_template("posts/edit.html", form=form, post=post)


# @app.route("/posts/<int:post_id>/delete", methods=["POST"])
# def delete_post(post_id):
#     """Delete a post."""
#     post = Post.query.get(post_id)

#     if "username" not in session or post.username != session['username']:
#         raise Unauthorized()


#     form = DeleteForm()

#     if form.validate_on_submit():
#         db.session.delete(post)
#         db.session.commit()

#     return redirect(f"/users/{post.username}")
