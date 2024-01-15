from flask import url_for
from app.post.models import Post, Type, Category
from app import db
from app.post.forms import PostForm,UpdateForm


def test_create_post(authenticated_client, new_user, categories, tags):
    response = authenticated_client.get(url_for('post.create_post'))
    assert response.status_code == 200
    form = PostForm(data = {
        'title': 'Test Post4',
        'text': 'This is a test post.',
        'type': 'news',
        'category': categories[0].id,
        'tags': f'{tags[0].name}, {tags[1].name}',

    })


    response = authenticated_client.post(url_for('post.create_post'), data=form.data, follow_redirects=True)
    assert response.status_code == 200
    print(response.text)
    assert b'Test Post' in response.data

    post = Post.query.filter_by(title='Test Post4').first()
    assert post is not None
    assert post.user == new_user

def test_update_post(authenticated_client, new_user, categories, tags):
    post = Post(title='Test Post', text='This is a test post.', type=Type.news, user=new_user)
    db.session.add(post)
    db.session.commit()

    response = authenticated_client.get(url_for('post.update_post', id=post.id))
    assert response.status_code == 200

    form = UpdateForm(data = {
        'title': 'Updated Test Post',
        'text': 'This is an updated test post.',
        'type': 'publication',
        'category': categories[0].id,
        'tags': f'{tags[0].name}, {tags[1].name}'
    })

    response = authenticated_client.post(url_for('post.update_post', id=post.id), data=form.data, follow_redirects=True)
    assert response.status_code == 200

    updated_post = Post.query.filter_by(title='Updated Test Post').first()
    assert updated_post is not None
    assert updated_post.user == new_user
    assert updated_post.type == Type.publication

def test_delete_post(authenticated_client, new_user):
    post = Post(title='Test Post', text='This is a test post.', type=Type.news, user=new_user)
    db.session.add(post)
    db.session.commit()

    response = authenticated_client.post(url_for('post.delete_post', id=post.id), follow_redirects=True)
    assert response.status_code == 200
    assert Post.query.get(post.id) is None

def test_view_post(authenticated_client, new_user, categories, tags):
    post = Post(title='Test Post', text='This is a test post.', type=Type.news, user=new_user)
    db.session.add(post)
    db.session.commit()

    response = authenticated_client.get(url_for('post.view_post', id=post.id))
    assert response.status_code == 200
    assert b'Test Post' in response.data
    assert b'This is a test post.' in response.data

def test_list_categories(authenticated_client):
    response = authenticated_client.get(url_for('post.list_categories'))
    assert response.status_code == 200
    assert b'List of Categories' in response.data

def test_create_category(authenticated_client):
    response = authenticated_client.get(url_for('post.create_category'))
    assert response.status_code == 200

    category_name = 'New Category'
    form_data = {'name': category_name}
    response = authenticated_client.post(url_for('post.create_category'), data=form_data, follow_redirects=True)
    assert response.status_code == 200

    assert Category.query.filter_by(name=category_name).first() is not None

def test_delete_category(authenticated_client):
    category_name = 'CategoryToDelete'
    category = Category(name=category_name)
    db.session.add(category)
    db.session.commit()

    assert Category.query.filter_by(name=category_name).first() is not None

    form_data = {'category_name': category_name}
    response = authenticated_client.post(url_for('post.delete_category'), data=form_data, follow_redirects=True)
    assert response.status_code == 200

    assert Category.query.filter_by(name=category_name).first() is None







