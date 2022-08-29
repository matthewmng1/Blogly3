from models import User, Post, PostTag, Tag, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# Users

deb = User(first_name="Debra", last_name="Lovings", image_url="None")
jon = User(first_name="Jon", last_name="Snow", image_url="None")
ray = User(first_name="Raymond", last_name="Chandler", image_url="None")
bubbles = User(first_name="Bubbles", last_name="The Cat", image_url="None")
peter = User(first_name="Peter", last_name="Parker", image_url="None")

db.session.add_all([deb, jon, ray, bubbles, peter])
db.session.commit()
