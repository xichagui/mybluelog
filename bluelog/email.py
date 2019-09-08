# -*- coding: utf-8 -*-
# @Time    : 2019-09-06 16:51
# @Author  : Xichagui
# @Site    :
# @File    : email.py
# @Software: PyCharm

from threading import Thread

from bluelog.extensions import mail
from flask import current_app, url_for
from flask_mail import Message


def _send_async_mail(app, message):
    with app.app_context():
        mail.send(message)


def send_mail(subject, to, html):
    allow_to_send_email = current_app.config['ALLOW_TO_SEND_EMAIL']
    if allow_to_send_email:
        app = current_app._get_current_object()
        message = Message(subject, recipients=[to], html=html)
        thr = Thread(target=_send_async_mail, args=[app, message])
        thr.start()
        return thr


def send_new_comment_email(post):
    post_url = url_for('blog.show_post', post_id=post.id,
                       _external=True) + '#comments'

    send_mail(
        subject='New comment',
        to=current_app.config['BLUELOG_ADMIN_EMAIL'],
        html=
        f'<p>New comment in post <i>{post.title}</i>, click the link below to check:</p>'
        f'<p><a href="{post_url}">{post_url}</a></p>'
        f'<p><small style="color: #868e96">Do not reply this email.</small></p>'
    )


def send_new_reply_email(comment):
    post_url = url_for('blog.show_post',
                       post_id=comment.post_id,
                       _external=True) + '#comments'

    # todo change the email to comment writer's email
    send_mail(
        subject='New reply',
        to=current_app.config['BLUELOG_ADMIN_EMAIL'],
        html=
        f'<p>New reply for comment you left in post <i>{comment.post.title}</i>, click the link below to check:</p>'
        f'<p><a href="{post_url}">{post_url}</a></p>'
        f'<p><small style="color: #868e96">Do not reply this email.</small></p>'
    )
