# -*- coding: utf-8 -*-
# @Time    : 2019-08-27 15:41
# @Author  : Xichagui
# @Site    :
# @File    : fakes.py
# @Software: PyCharm
import random

from bluelog import db
from bluelog.models import Category, Comment, Post, User
from faker import Faker
from sqlalchemy.exc import IntegrityError

fake = Faker()


def fake_admin():
    admin = User(username='admin',
                 blog_title='Bluelog',
                 blog_sub_title="No, I'm the real thing.",
                 name='ZIO',
                 about="I'm the King of the world.",
                 password='12345678',
                 email='xichagui@gmail.com',
                 confirmed=True)

    # admin.set_password('12345678')
    db.session.add(admin)
    db.session.commit()


def fake_categories(count=10):

    category = Category(name='Default')
    db.session.add(category)

    for i in range(count):
        category = Category(name=fake.word())
        db.session.add(category)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


def fake_posts(count=50):
    for i in range(count):
        post = Post(title=fake.sentence(),
                    body=fake.text(2000),
                    category=Category.query.get(
                        random.randint(1, Category.query.count())),
                    timestamp=fake.date_time_this_year())

        db.session.add(post)

    salt = int(count * 0.1)

    for i in range(salt):
        post = Post(title=fake.sentence(),
                    body=fake.text(2000),
                    category=Category.query.get(
                        random.randint(1, Category.query.count())),
                    timestamp=fake.date_time_this_year(),
                    can_comment=False)

        db.session.add(post)

    db.session.commit()


def fake_comments(count=500):
    for i in range(count):
        comment = Comment(author=fake.name(),
                          email=fake.email(),
                          site=fake.url(),
                          body=fake.sentence(),
                          timestamp=fake.date_time_this_year(),
                          reviewed=True,
                          post=Post.query.get(
                              random.randint(1, Post.query.count())))
        db.session.add(comment)

    salt = int(count * 0.1)
    for i in range(salt):
        # comment without review
        comment = Comment(author=fake.name(),
                          email=fake.email(),
                          site=fake.url(),
                          body=fake.sentence(),
                          timestamp=fake.date_time_this_year(),
                          reviewed=False,
                          post=Post.query.get(
                              random.randint(1, Post.query.count())))
        db.session.add(comment)

        # comment by author
        comment = Comment(author='ZIO',
                          email='zio@zio.com',
                          site='zio.com',
                          body=fake.sentence(),
                          timestamp=fake.date_time_this_year(),
                          from_admin=True,
                          reviewed=True,
                          post=Post.query.get(
                              random.randint(1, Post.query.count())))
        db.session.add(comment)

    db.session.commit()

    # replies
    for i in range(salt):
        replied = Comment.query.get(random.randint(1, Comment.query.count()))
        comment = Comment(author=fake.name(),
                          email=fake.email(),
                          site=fake.url(),
                          body=fake.sentence(),
                          timestamp=fake.date_time_this_year(),
                          reviewed=False,
                          replied=replied,
                          post=replied.post)
        db.session.add(comment)

    db.session.commit()
