import random
import datetime
from uuid import uuid4

from models import db, User, Tag, Post

user = User(username='Tachikoma', password='199Roses')
db.session.add(user)
db.session.commit()

user = db.session.query(User).first()
tag_one = Tag(name='Python')
tag_two = Tag(name='Flask')
tag_three = Tag(name='SQLAlchemy')
tag_four = Tag(name='JMilkFan')
tag_list = [tag_one, tag_two, tag_three, tag_four]

EXAMPLE_TEXT = 'EXAMPLE TEXT'

for i in range(100):
    new_post = Post(title='Post' + str(i))
    new_post.user = user
    new_post.publish_date = datetime.datetime.now()
    new_post.text = 5
    new_post.tags = random.sample(tag_list, random.randint(1, 3))
    db.session.add(new_post)

db.session.commit()
