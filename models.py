from time import timezone
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
  db.app = app
  db.init_app(app)

class User(db.Model):

  __tablename__ = "users"

  def __repr__(self):
    p = self
    return f"<User id = {p.id} first_name = {p.first_name} last_name = {p.last_name} image_url = {p.image_url}>"
 

  id = db.Column(db.Integer, 
                 primary_key=True, 
                 autoincrement=True)

  first_name = db.Column(db.Text, 
                         nullable=False, 
                         unique=False)

  last_name = db.Column(db.Text, 
                        nullable=False, 
                        unique=False)

  image_url = db.Column(db.Text(), 
                        nullable=True, 
                        unique=False)

  posts = db.relationship("Post", backref="user", cascade="all, delete, delete-orphan")


class Post(db.Model):

  __tablename__ = "posts"

  def _repr__(self):
    p = self
    return f"<Post id = {p.id} title = {p.title} content = {p.content} created_at = {p.created_at} post = {p.post}>"

  id = db.Column(db.Integer, 
                 primary_key=True, 
                 autoincrement=True)

  title = db.Column(db.Text, 
                    nullable=False, 
                    unique=True)

  content = db.Column(db.Text, 
                      nullable=False, 
                      unique=False)

  created_at = db.Column(db.DateTime,
                         nullable=True)

  user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

class PostTag(db.Model):

  __tablename__ = 'post_tags'

  post_id = db.Column(db.Integer, db.ForeignKey('posts.id', ondelete='CASCADE'), primary_key=True, nullable=False)

  tag_id = db.Column(db.Integer, db.ForeignKey('tags.id', ondelete='CASCADE'), primary_key=True, nullable=False)

class Tag(db.Model):

  __tablename__= 'tags'

  id = db.Column(db.Integer, 
                 primary_key=True, 
                 autoincrement=True)

  name = db.Column(db.Text, unique=True)

  posts = db.relationship('Post', secondary="post_tags", backref="tags")