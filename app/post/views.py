import time
from flask import render_template, redirect, url_for, request, flash
from flask_login import current_user
from werkzeug.utils import secure_filename
from .forms import PostForm, DeleteForm, CategoryForm, UpdateForm, DeleteCategoryForm
from .models import db, Post, Category, Tag
from . import post_bp


@post_bp.route('/post/create', methods=['GET', 'POST'])
def create_post():
    form = PostForm()
    categories = Category.query.all()
    form.category.choices = [(category.id, category.name) for category in categories]
    if form.validate_on_submit():
        profile_image = form.image.data
        if profile_image:
            filename = secure_filename(profile_image.filename)
            unique_filename = f"{int(time.time())}_{filename}.jpg"
            file_path = f'postimg/{unique_filename}'
            profile_image.save(f'app/static/{file_path}')
        tags = form.tags.data.split(',')
        tags = [tag.strip() for tag in tags if tag]
        category_id = form.category.data
        category = Category.query.get(category_id)
        new_post = Post(
            title=form.title.data,
            text=form.text.data,
            type=form.type.data,
            image=file_path if profile_image else None,
            user_id=current_user.id,
            category=category,
            tags=[Tag.get_or_create(tag) for tag in tags]
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('post.list_posts'))
    return render_template('post/create_post.html', form=form, categories=categories)


# @post_bp.route('/post', methods=['GET'])
# def list_posts():
#     all_posts = Post.query.order_by(Post.created.desc()).all()
#     return render_template('post/list_posts.html', posts=all_posts)

@post_bp.route('/post', methods=['GET'])
def list_posts():
    page = request.args.get('page', 1, type=int)
    per_page = 1  # Кількість постів на сторінці
    posts = Post.query.order_by(Post.created.desc()).paginate(page=page, per_page=per_page)
    return render_template('post/list_posts.html', posts=posts)


@post_bp.route('/post/<int:id>', methods=['GET'])
def view_post(id):
    del_form = DeleteForm()
    post = Post.query.get(id)
    return render_template('post/view_post.html', post=post, del_form=del_form)


@post_bp.route('/post/<int:id>/update', methods=['POST', 'GET'])
def update_post(id):
    categories = Category.query.all()
    post = Post.query.get(id)
    form = UpdateForm()
    form.category.choices = [(category.id, category.name) for category in categories]
    if form.validate_on_submit():
        if form.title.data:
            post.title = form.title.data
        if form.text.data:
            post.text = form.text.data
        if form.type.data:
            post.type = form.type.data
        if form.tags.data:
            tags = form.tags.data.split(',')
            tags = [tag.strip() for tag in tags if tag]
            post.tags = [Tag.get_or_create(tag) for tag in tags]
        if form.category.data:
            category_id = form.category.data
            category = Category.query.get(category_id)
            post.category = category
        profile_image = form.image.data
        if profile_image:
            filename = secure_filename(profile_image.filename)
            unique_filename = f"{int(time.time())}_{filename}.jpg"
            file_path = f'img/{unique_filename}'
            profile_image.save(f'app/static/{file_path}')
            post.image = file_path
        db.session.commit()
        return redirect(url_for('post.list_posts'))
    return render_template('post/update_post.html', form=form, post=post, categories=categories)


@post_bp.route('/post/<int:id>/delete', methods=['POST'])
def delete_post(id):
    form = DeleteForm()
    if form.validate_on_submit():
        post = Post.query.get(id)
        db.session.delete(post)
        db.session.commit()
    return redirect(url_for('post.list_posts'))


@post_bp.route('/categories', methods=['GET'])
def list_categories():
    categories = Category.query.all()
    return render_template('post/list_categories.html', categories=categories)


@post_bp.route('/categories/create', methods=['GET', 'POST'])
def create_category():
    form = CategoryForm()
    if form.validate_on_submit():
        name = form.name.data
        category = Category(name=name)
        db.session.add(category)
        db.session.commit()
        return redirect(url_for('post.list_categories'))
    return render_template('post/create_category.html', form=form)

@post_bp.route('/categories/delete', methods=['GET', 'POST'])
def delete_category():
    form = DeleteCategoryForm()

    if form.validate_on_submit():
        category_name = form.category_name.data
        category = Category.query.filter_by(name=category_name).first()

        if category:
            db.session.delete(category)
            db.session.commit()
            flash(f'Category "{category_name}" has been deleted.', 'success')
            return redirect(url_for('post.list_categories'))  # Перенаправлення на сторінку зі списком категорій
        else:
            flash(f'Category "{category_name}" not found.', 'danger')

    return render_template('post/delete_category.html', form=form)