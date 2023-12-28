from app import db
import enum


class Type(enum.Enum):
    news = 1
    publication = 2
    other = 3


tags = db.Table('post_tags',
                db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
                db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')))


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)

    @staticmethod
    def get_or_create(name):
        tag = Tag.query.filter_by(name=name).first()
        if tag:
            return tag
        else:
            new_tag = Tag(name=name)
            db.session.add(new_tag)
            db.session.commit()
            return new_tag


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)


class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    text = db.Column(db.String)
    image = db.Column(db.String, default='static/img')
    created = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
    type = db.Column(db.Enum(Type), default='news', nullable=False)
    enabled = db.Column(db.Boolean, default=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id', name='fk_post_category'), nullable=True)
    category = db.relationship('Category', backref='posts')
    tags = db.relationship('Tag', secondary=tags, backref='posts')
    user = db.relationship('User', backref='posts')

    def __repr__(self):
        return f"<Post {self.id}, Title: {self.title}, Type: {self.type}, Enabled: {self.enabled}>"