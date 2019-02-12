from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4
from .extensions import bcrypt


db = SQLAlchemy()


posts_tags = db.Table('posts_tags',
                      db.Column('post_id', db.String(45),
                                db.ForeignKey('posts.id')),
                      db.Column('tag_id', db.String(45),
                                db.ForeignKey('tags.id'))
                      )


class User(db.Model):
    """Represents Proected users."""

    __tablename__ = 'users'
    id = db.Column(db.String(45), primary_key=True)
    username = db.Column(db.String(191))
    password = db.Column(db.String(191))
    # one to many: User ==> Post
    # Establish contact with Post's ForeignKey: user_id
    posts = db.relationship(
        'Post',
        backref='users',
        lazy='dynamic')

    def __init__(self, username, password):
        self.id = str(uuid4())
        self.username = username
        self.password = self.set_password(password)

    def __repr__(self):
        return f'<Model User: {self.username}>'

    def set_password(self, password):
        """Convert the password to cryptograph via flask-bcrypt"""
        return bcrypt.generate_password_hash(password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)


class Role(db.Model):
    """Represents Proected roles."""

    __tablename__ = 'roles'
    id = db.Column(db.String(45), primary_key=True)
    name = db.Column(db.String(191), unique=True)
    description = db.Column(db.String(191))

    def __init__(self):
        self.id = str(uuid4())

    def __repr__(self):
        return f'<Model Role: {self.name}>'


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.String(45), primary_key=True)
    title = db.Column(db.String(191))
    text = db.Column(db.Text())
    publish_date = db.Column(db.DateTime)
    # Set the foreign key for Post
    user_id = db.Column(db.String(45), db.ForeignKey('users.id'))
    comments = db.relationship(
        'Comment',
        backref='posts',
        lazy='dynamic'
    )
    # many to many: posts <==> tags
    tags = db.relationship(
        'Tag',
        secondary=posts_tags,
        backref=db.backref('posts', lazy='dynamic')
    )

    def __init__(self, title):
        self.id = str(uuid4())
        self.title = title

    def __repr__(self):
        return f'<Model Post: {self.title}>'


class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.String(45), primary_key=True)
    name = db.Column(db.String(191))

    def __init__(self, name):
        self.id = str(uuid4())
        self.name = name

    def __repr__(self):
        return f'<Model Tag: {self.name}>'


class BrowseVolume(db.Model):
    """Represents Proected browse_volumes."""

    __tablename__ = 'browse_volumes'
    id = db.Column(db.String(45), primary_key=True)
    home_view_total = db.Column(db.Integer)

    def __init__(self):
        self.id = str(uuid())
        self.home_view_total = 0

    def __repr__(self):
        return f'<Model BrowseVolume: {self.home_view_total}>'

    def add_one(self):
        self.home_view_total += 1


class Reminder(db.Model):
    """Represents Proected reminders."""

    __tablename__ = 'reminders'
    id = db.Column(db.String(45), primary_key=True)
    date = db.Column(db.DateTime())
    email = db.Column(db.String(191))
    text = db.Column(db.Text())

    def __init__(self):
        self.id = str(uuid4())

    def __repr__(self):
        return f'<Model Reminder: {self.text[:20]}>'


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.String(45), primary_key=True)
    name = db.Column(db.String(191))
    text = db.Column(db.Text())
    date = db.Column(db.DateTime())
    post_id = db.Column(db.String(45), db.ForeignKey('posts.id'))

    def __init__(self, name):
        self.id = str(uuid4())
        self.name = name

    def __repr__(self):
        return f'<Model Comment: {self.name}>'
