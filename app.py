from flask import Flask, request, redirect, render_template, flash, session, g, abort, url_for
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Project, UserProject, Task
from forms import RegisterForm, LoginForm, UserEditForm,AddProjectForm, AddTaskForm
from werkzeug.exceptions import Unauthorized
from sqlalchemy.exc import IntegrityError
import os, requests
# from secrets import API_Key

CURR_USER_KEY = "curr_user"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL','postgresql:///codercollab')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY','izURL73j^nu24Bp')
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
        user.profile_image_url = form.profile_image_url.data
        user.bio = form.bio.data
        user.email = form.email.data
        user.location = form.location.data
            
           

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
# Projects routes:
@app.route("/projects")
def show_projects():
    """show all projects"""
    
    projects = Project.query.all()


    return render_template('projects/show.html', projects=projects)



@app.route(f"/projects/new", methods=["GET", "POST"])
def new_project():
    """Add the project form and process it."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    form = AddProjectForm()

    if form.validate_on_submit():
        name = form.name.data
        technology = form.technology.data
        about = form.about.data
        level = form.level.data
        link = form.link.data
        availability = form.availability.data

        project = Project(
            name=name,
            technology=technology,
            about=about,
            level=level,
            link=link,
            availability=availability
        )

        db.session.add(project)
        db.session.commit()


        return redirect ("/projects")

    return render_template("projects/new.html", form=form)
@app.route('/projects/<int:id>')
def detail_project(id):
    """show details of a project"""
    project = Project.query.get_or_404(id)

    return render_template('projects/detail.html', project=project)


@app.route('/projects/<int:id>/edit', methods=["GET", "POST"])
def edit_project(id):
    """Show and edit a project."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    
    project = Project.query.get_or_404(id)

    form = AddProjectForm(obj=project)

    if form.validate_on_submit():
        project.name = form.name.data
        project.technology = form.technology.data
        project.about = form.about.data
        project.level = form.level.data
        project.link = form.link.data
        project.availability=form.availability.data

        db.session.commit()

        return redirect(f"/projects/{project.id}")

    return render_template("/projects/edit.html", form=form, project=project)

@app.route('/projects/<int:id>/delete', methods=["POST"])
def delete_project(id):
    """Delete a project."""
    
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    
    project = Project.query.get_or_404(id)

    db.session.delete(project)
    db.session.commit()

    return redirect('/projects')

##############################################################################
# Task Routes:
@app.route(f"/projects/<int:id>/tasks")
def show_tasks(id):
    """show all tasks"""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    project = Project.query.get_or_404(id)
    tasks = Task.query.all()

    return render_template('tasks/show.html', project=project,tasks=tasks)

@app.route(f"/projects/<int:id>/tasks/new", methods=["GET", "POST"])
def new_task(id):
    """Add the task form and process it."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    project = Project.query.get_or_404(id)
    form = AddTaskForm()

    if form.validate_on_submit():
        title = form.title.data
        notes = form.notes.data
       
        task = Task(
            title = title,
            notes = notes
            )

        db.session.add(task)
        db.session.commit()


        return redirect (f"/projects/{project.id}/tasks")

    return render_template('tasks/new.html', project=project, form=form)


@app.route('/projects/<int:id>/tasks/<int:task_id>')
def detail_task(id,task_id):
    """show details of a task"""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    
    project = Project.query.get_or_404(id)
    task = Task.query.get_or_404(task_id)

    return render_template('tasks/detail.html', project=project, task=task)


@app.route('/projects/<int:id>/tasks/<int:task_id>/edit', methods=["GET", "POST"])
def edit_task(id,task_id):
    """Show and edit a task."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    
    project = Project.query.get_or_404(id)
    task = Task.query.get_or_404(task_id)

    form = AddTaskForm(obj=task)

    if form.validate_on_submit():
        task.title = form.title.data
        task.notes = form.notes.data
        task.status = form.status.data
       
        db.session.commit()

        return redirect(f"/projects/{project.id}/tasks/{task.task_id}")

    return render_template("tasks/edit.html", project=project,form=form, task=task)

@app.route('/projects/<int:id>/tasks/<int:task_id>/delete', methods=["POST"])
def delete_task(id,task_id):
    """Delete a task."""
    
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    project = Project.query.get_or_404(id)
    task = Task.query.get_or_404(task_id)

    db.session.delete(task)
    db.session.commit()

    return redirect(f'/projects/{project.id}/tasks')













##############################################################################
# Comments Routes:


















##############################################################################
# Tags Routes:



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

##############################################################################
# Homepage and error pages



# @app.errorhandler(404)
# def page_not_found(e):
#     """404 NOT FOUND page."""

#     return render_template('404.html'), 404


##############################################################################
# Turn off all caching in Flask

@app.after_request
def add_header(req):
    """Add non-caching headers on every request."""

    req.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    req.headers["Pragma"] = "no-cache"
    req.headers["Expires"] = "0"
    req.headers['Cache-Control'] = 'public, max-age=0'
    return req