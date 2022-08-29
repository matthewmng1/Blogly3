from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, PostTag, Tag

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///users_db' #must do this data base before the other db below
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'ITSASECRET'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)

# Users

@app.route('/')
def list_users():
  users = User.query.all()
  return render_template('list.html', users=users)

@app.route('/', methods=['POST'])
def create_user():
  first_name = request.form["first_name"]
  last_name = request.form["last_name"]
  image_url = request.form["image_url"]

  new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)  
  db.session.add(new_user)
  db.session.commit()
  return redirect(f"/{new_user.id}")

@app.route('/<int:user_id>')
def show_user(user_id):
  """Show details about a single user"""
  user = User.query.get_or_404(user_id)
  return render_template("details.html", user=user)

@app.route('/edit/<int:user_id>')
def edit_page(user_id):
  """Edit user details"""
  user = User.query.get_or_404(user_id)
  return render_template("edit_user.html", user=user)

@app.route('/edit/<int:user_id>', methods=['POST'])
def edit_user(user_id):
  user = User.query.get_or_404(user_id)

  user.first_name = request.form["edit-first-name"]
  user.last_name = request.form["edit-last-name"]
  user.image_url = request.form["edit-image-url"]

  db.session.add(user)
  db.session.commit()
  
  return redirect(f"/{user.id}")

@app.route('/delete/<int:user_id>')
def delete_user(user_id):
  user = User.query.get_or_404(user_id)

  User.query.filter(User.id == user_id).delete()

  db.session.commit()

  return render_template("confirm-delete.html", user=user)

# Posts

@app.route('/<int:user_id>/posts/new')
def get_post(user_id):
  user = User.query.get_or_404(user_id)
  tags = Tag.query.all()

  return render_template("get-post.html", user=user, tags=tags)

@app.route('/<int:user_id>/posts/new', methods=['POST'])
def new_post(user_id):
  user = User.query.get_or_404(user_id)
  tag_ids = [int(num) for num in request.form.getlist("tags")]
  tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()


  title = request.form["post-title"]
  content = request.form["post-content"]

  new_post = Post(title=title, content=content, user=user, tags=tags)

  db.session.add(new_post)
  db.session.commit()
  
  return redirect(f"/posts/new/{new_post.id}")

@app.route('/posts/new/<int:post_id>')
def show_post(post_id):
  """Show post """
  post = Post.query.get_or_404(post_id)
  return render_template("posts.html", post=post)

@app.route('/edit/posts/<int:post_id>')
def edit_post_page(post_id):
  """Edit  post"""
  post = Post.query.get_or_404(post_id)
  tags = Tag.query.all()
  return render_template("edit-post.html", post=post, tags=tags)

@app.route('/edit/posts/<int:post_id>', methods=['POST'])
def edit_post(post_id):
  """Edit post"""
  post = Post.query.get_or_404(post_id)
  post.title = request.form['new-title']
  post.content = request.form['new-content']

  tag_ids = [int(num) for num in request.form.getlist("tags")]
  post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

  db.session.add(post)
  db.session.commit()

  return redirect(f"/posts/new/{post.id}")

@app.route('/delete/posts/<int:post_id>')
def delete_post(post_id):
  post = Post.query.get_or_404(post_id)

  Post.query.filter(Post.id == post_id).delete()

  db.session.commit()

  return render_template("confirm-delete.html")

# tags

@app.route('/tags')
def tags_index():
    """Show a page with info on all tags"""

    tags = Tag.query.all()
    return render_template('all-tags.html', tags=tags)


@app.route('/tags/new')
def tags_new_form():
    """Show a form to create a new tag"""

    posts = Post.query.all()
    return render_template('new-tags.html', posts=posts)


@app.route("/tags/new", methods=["POST"])
def tags_new():
    """Handle form submission for creating a new tag"""

    post_ids = [int(num) for num in request.form.getlist("posts")]
    posts = Post.query.filter(Post.id.in_(post_ids)).all()
    new_tag = Tag(name=request.form['name'], posts=posts)

    db.session.add(new_tag)
    db.session.commit()
    flash(f"Tag '{new_tag.name}' added.")

    return redirect("/tags")

@app.route('/tags/<int:tag_id>')
def tags_show(tag_id):
    """Show a page with info on a specific tag"""

    tag = Tag.query.get_or_404(tag_id)
    return render_template('show-tags.html', tag=tag)


@app.route('/tags/<int:tag_id>/edit')
def tags_edit_form(tag_id):
    """Show a form to edit an existing tag"""

    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.all()
    return render_template('edit-tags.html', tag=tag, posts=posts)


@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def tags_edit(tag_id):
    """Handle form submission for updating an existing tag"""

    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['name']
    post_ids = [int(num) for num in request.form.getlist("posts")]
    tag.posts = Post.query.filter(Post.id.in_(post_ids)).all()

    db.session.add(tag)
    db.session.commit()
    flash(f"Tag '{tag.name}' edited.")

    return redirect("/tags")

@app.route('/delete/tags/<int:tag_id>')
def delete_tag(tag_id):

  tag = Post.query.get_or_404(tag_id)
  
  db.session.delete(tag)
  db.session.commit()

  return render_template("confirm-delete.html")