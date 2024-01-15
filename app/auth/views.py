import os
from datetime import datetime

from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.utils import secure_filename

from app import db
from .forms import LoginForm, RegistrationForm, UpdateAccountForm ,ChangePasswordForm
from .models import  User
from PIL import Image
from . import auth_blueprint

@auth_blueprint.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('.users'))
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
    return render_template('auth/register.html', form=form)

@auth_blueprint.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('.users'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.verify_password(form.password.data):
            login_user(user, remember=form.remember.data)
            flash('Login successful!', 'success')
            return redirect(url_for('.users'))
        else:
            flash('Login unsuccessful. Please check email and password.', 'danger')
    return render_template('auth/login.html', form=form)

@auth_blueprint.route('/users')
@login_required
def users():
    users_list = User.query.all()
    total_users = len(users_list)
    update_form = UpdateAccountForm()
    change_password_form = ChangePasswordForm()
    return render_template('auth/users.html', users_list=users_list, total_users=total_users, update_form=update_form, change_password_form=change_password_form)



@auth_blueprint.route('/update_users', methods=['GET', 'POST'])
@login_required
def update_users():
    update_form = UpdateAccountForm()
    change_password_form = ChangePasswordForm()


    if update_form.validate_on_submit():
        if update_form.profile_photo.data:
            profile_photo = update_form.profile_photo.data
            if profile_photo.filename != '':
                 profile_photo_path = 'static/profile_photos/'
                 new_filename = secure_filename(profile_photo.filename)
                 # profile_photo.save(os.path.join(app.root_path ,profile_photo_path, new_filename))
                 output_size = (200, 200)
                 i = Image.open(profile_photo)
                 i.thumbnail(output_size)
                 i.save(os.path.join(auth_blueprint.root_path ,profile_photo_path, new_filename))
                 current_user.image_file = new_filename
        current_user.username = update_form.username.data
        current_user.email = update_form.email.data
        current_user.about_me = update_form.about_me.data
        db.session.commit()

        flash('Your account information has been updated successfully!', 'success')
        return redirect(url_for('.users'))

    elif request.method == 'GET':
        update_form.username.data = current_user.username
        update_form.email.data = current_user.email
        update_form.about_me.data = current_user.about_me

    return render_template('auth/users.html', update_form=update_form, change_password_form=change_password_form)

@auth_blueprint.route('/change_password', methods=['POST'])
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

        return redirect(url_for('.users'))

    return render_template('auth/users.html', change_password_form=form, update_form=UpdateAccountForm())

@auth_blueprint.after_request
def after_request(response):
    if current_user:
        current_user.last_seen = datetime.now()
        try:
             db.session.commit()
        except:
             flash('Error while update user last seen!', 'danger')
        return response

@auth_blueprint.route("/logout", methods=['GET','POST'])
def logout():
    logout_user()
    flash('You have been logged out', 'success')
    return redirect(url_for('.login'))