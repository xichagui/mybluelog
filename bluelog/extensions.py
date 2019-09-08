# -*- coding: utf-8 -*-
# @Time    : 2019-08-20 15:40
# @Author  : Xichagui
# @Site    :
# @File    : extensions.py
# @Software: PyCharm

from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

bootstrap = Bootstrap()
db = SQLAlchemy()
moment = Moment()
ckeditor = CKEditor()
mail = Mail()
login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    from bluelog.models import Admin
    user = Admin.query.get(int(user_id))
    return user


login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'warning'

login_manager.login_message = '请先登录'
