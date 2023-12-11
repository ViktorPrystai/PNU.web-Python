import json
import os
from datetime import datetime, timedelta

from flask import render_template, redirect, url_for, session, make_response, flash, request
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.utils import secure_filename

from app import app, db
from app.data import posts
from app.forms import FeedbackForm, LoginForm, TodoForm, RegistrationForm, UpdateAccountForm ,ChangePasswordForm
from app.models import Feedback, Todo, User
from PIL import Image

app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
app.config['SESSION_REFRESH_EACH_REQUEST'] = True


def _get_credentials_filepath(filename="mydata/users.json",):
    parent_dir = os.path.abspath(os.path.dirname(__file__))
    filepath = os.path.join(parent_dir, filename)
    return filepath
with open(_get_credentials_filepath(), 'r') as f:
    users = json.load(f)


# @app.route('/login', methods=["GET", "POST"])
# def login():
#     form = LoginForm()
#
#     if form.validate_on_submit():
#         name = form.name.data
#         password = form.password.data
#         remember = bool(request.form.get("remember"))
#
#         if name in users and users[name] == password:
#             session["username"] = name
#             if remember:
#
#                 session.permanent = True
#                 app.permanent_session_lifetime = timedelta(days=730)
#             else:
#
#                 app.permanent_session_lifetime = timedelta(minutes=30)
#             flash('Login successful', 'success')
#             return redirect(url_for("info"))
#         else:
#             flash('Invalid username or password', 'danger')
#             return redirect(url_for("login"))
#
#     return render_template("login.html", form=form)

#         hashed_password = generate_password_hash(form.password.data, method='sha256')
#         new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
#         db.session.add(new_user)
#         db.session.commit()
#         flash('Your account has been created!', 'success')
#         return redirect(url_for('login'))
#     return render_template('register.html', title='Register', form=form)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            user = User(username=form.username.data, email=form.email.data, password=form.password.data)
            db.session.add(user)
            db.session.commit()
            flash(f'Account successfully created for {form.username.data}!', 'success')
            return redirect(url_for('home'))
        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'danger')
            db.session.rollback()
    return render_template('register.html', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('register'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.verify_password(form.password.data):
            login_user(user, remember=form.remember.data)
            flash('Login successful!', 'success')
            return redirect(url_for('users'))
        else:
            flash('Login unsuccessful. Please check email and password.', 'danger')
    return render_template('login.html', form=form)

@app.route("/logout")
def logout():
    logout_user()
    flash('You have been logged out', 'success')
    return redirect(url_for('home'))

@app.route('/info', methods=["GET", "POST"])
def info():
    user = session.get('username')

    user_cookies = request.cookies
    if user:
        if request.method == "POST":

            return render_template("info.html", username=user, user_cookies=user_cookies)
        return render_template("info.html", username=user, user_cookies=user_cookies)
    else:
        return redirect(url_for("login"))

# @app.route('/logout', methods=["GET", "POST"])
# def logout():
#     session.pop('username', None)
#     return redirect(url_for("login"))


@app.route('/add_cookie', methods=["POST"])
def add_cookie():
    user = session.get('username')

    if user:
        key = request.form.get('key')
        value = request.form.get('value')
        expiration = request.form.get('expiration')

        if key and value and expiration:
            expiration = int(expiration)
            expiration_time = datetime.now() + timedelta(seconds=expiration)


            response = make_response(redirect(url_for("info")))


            response.set_cookie(key, value, expires=expiration_time)

            return response
        else:
            return "Error: Invalid input for adding a cookie"
    else:
        return redirect(url_for("login"))
    pass


@app.route('/delete_cookie', methods=["POST"])
def delete_cookie():
    user = session.get('username')

    if user:
        key_to_delete = request.form.get('delete_key')

        if key_to_delete:

            response = make_response(redirect(url_for("info")))
            response.delete_cookie(key_to_delete)

            return response
        else:
            return "Error: Invalid input for deleting a cookie"
    else:
        return redirect(url_for("login"))



@app.route('/delete_all_cookies', methods=["POST"])
def delete_all_cookies():
    user = session.get('username')

    if user:

        response = make_response(redirect(url_for("info")))


        for key in request.cookies.keys():
            response.delete_cookie(key)

        return response
    else:
        return redirect(url_for("login"))
    pass


# @app.route('/change_password', methods=['POST'])
# def change_password():
#     user = session.get('username')
#
#     if user:
#         new_password = request.form.get('new_password')
#
#         if new_password:
#
#             users[user] = new_password
#             return redirect(url_for("info"))
#
#     return redirect(url_for("login"))


@app.context_processor
def inject_data():
    os_name = os.name
    user_agent = request.headers.get('User-Agent')
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return dict(os_name=os_name, user_agent=user_agent, current_time=current_time)

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    form = FeedbackForm()
    if form.validate_on_submit():
        name = form.name.data
        message = form.message.data

        feedback = Feedback(name=name, message=message)
        db.session.add(feedback)
        db.session.commit()
        flash('Ваш відгук був збережений', 'success')
        return redirect(url_for('feedback'))

    feedbacks = Feedback.query.all()
    return render_template('feedback.html', form=form, feedbacks=feedbacks)

@app.route('/delete_feedback/<int:feedback_id>', methods=['POST'])
def delete_feedback(feedback_id):
    feedback = Feedback.query.get(feedback_id)
    if feedback:
        db.session.delete(feedback)
        db.session.commit()
        flash('Відгук був видалений', 'success')
    else:
        flash('Відгук не знайдено', 'danger')
    return redirect(url_for('feedback'))


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/skill/')
@app.route('/skill/<int:idx>')
def skill(idx=None):
    if idx is not None:
        return render_template("skill.html", posts=posts, idx=idx)
    else:
        return render_template("skills.html", posts=posts)

@app.route('/todo', methods=['POST','GET'])
def todo():
    todo_list = Todo.query.all()
    form = TodoForm()
    return render_template("todo.html", todo_list=todo_list, form=form)


@app.route("/add", methods=["POST"])
def todo_add():
    form = TodoForm()
    if form.validate_on_submit():
        title = form.title.data
        new_todo = Todo(title=title, complete=False)
        db.session.add(new_todo)
        db.session.commit()
    return redirect(url_for("todo"))


@app.route("/update/<int:todo_id>")
def todo_update(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("todo"))


@app.route("/delete/<int:todo_id>")
def todo_delete(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("todo"))

@app.route('/users')
@login_required
def users():
    users_list = User.query.all()
    total_users = len(users_list)
    update_form = UpdateAccountForm()
    change_password_form = ChangePasswordForm()
    return render_template('users.html', users_list=users_list, total_users=total_users, update_form=update_form, change_password_form=change_password_form)



@app.route('/update_users', methods=['GET', 'POST'])
@login_required
def update_users():
    update_form = UpdateAccountForm()
    change_password_form = ChangePasswordForm()


    if update_form.validate_on_submit():
        if 'profile_photo' in request.files:
            profile_photo = request.files['profile_photo']
            if profile_photo.filename != '':
                 profile_photo_path = 'static/profile_photos/'
                 new_filename = secure_filename(profile_photo.filename)
                 # profile_photo.save(os.path.join(app.root_path ,profile_photo_path, new_filename))
                 output_size = (200, 200)
                 i = Image.open(profile_photo)
                 i.thumbnail(output_size)
                 i.save(os.path.join(app.root_path ,profile_photo_path, new_filename))
                 current_user.image_file = new_filename
        current_user.username = update_form.username.data
        current_user.email = update_form.email.data
        current_user.about_me = update_form.about_me.data
        db.session.commit()

        flash('Your account information has been updated successfully!', 'success')
        return redirect(url_for('users'))

    elif request.method == 'GET':
        update_form.username.data = current_user.username
        update_form.email.data = current_user.email
        update_form.about_me.data = current_user.about_me

    return render_template('users.html', update_form=update_form, change_password_form=change_password_form)

@app.route('/change_password', methods=['POST'])
def change_password():
    form = ChangePasswordForm()

    if form.validate_on_submit():
        new_password = form.new_password.data
        try:
            current_user.set_password(new_password)
            db.session.commit()
            flash('Password updated successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash("Failed to update!", category="danger")

        return redirect(url_for('users'))

    return render_template('users.html', change_password_form=form, update_form=UpdateAccountForm())


@app.after_request
def after_request(response):
    if current_user:
        current_user.last_seen = datetime.now()
        try:
         db.session.commit()
        except:
         flash('Error while update user last seen!', 'danger')
        return response