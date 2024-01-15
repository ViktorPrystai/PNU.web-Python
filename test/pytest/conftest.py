import pytest
from app import create_app, db
from app.post.models import Category, Post, Tag
from app.auth.models import User
from flask import url_for
from app.auth.forms import LoginForm

@pytest.fixture(scope='module')
def app():
    app = create_app('test')
    app.config['SERVER_NAME'] = '127.0.0.1:5000'

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope='module')
def client(app):
    with app.test_client() as client:
        yield client

@pytest.fixture(scope='module')
def new_user(app):
    with app.app_context():
        user = User(username='Test User', email='test.user@gmail.com', password='password')
        yield user

@pytest.fixture(scope='module')
def categories(app):
    with app.app_context():
        categories = [
            Category(name='Sport'),
            Category(name='Art')
        ]
        yield categories

@pytest.fixture(scope='module')
def tags(app):
    with app.app_context():
        tags = [
            Tag(name='cats'),
            Tag(name='music')
        ]
        yield tags

@pytest.fixture(scope='module')
def posts(app, new_user, categories, tags):
    with app.app_context():
        posts = [
            Post(title='Test Post 1', text='This is a test post', user=new_user, category=categories[0],
                 tags=[tags[0], tags[1]]),
            Post(title='Test Post 2', text='Another test post', user=new_user, category=categories[1], tags=[tags[1]]),
            Post(title='Test Post 3', text='Yet another test post', user=new_user, category=categories[0],
                 tags=[tags[1], tags[0]])
        ]
        yield posts

@pytest.fixture(scope='module')
def init_database(app, new_user, posts, categories, tags):
    with app.app_context():
        db.create_all()

        default_user = User(username='Cool User', email='cool@gmail.com', password='password')
        db.session.add_all(
            [new_user, default_user, *categories, *tags, *posts])
        db.session.commit()

        yield

@pytest.fixture(scope='function')
def authenticated_client(app, init_database, new_user, client):
    form = LoginForm(data={'email': new_user.email, 'password': 'password'})
    response = client.post(
        url_for('auth.login'),
        data=form.data,
        follow_redirects=True
    )
    print(response.text)
    assert response.status_code == 200

    yield client

    # Вийдіть з системи після кожного тесту
    response = client.post(url_for('auth.logout'), follow_redirects=True)
    assert response.status_code == 200










