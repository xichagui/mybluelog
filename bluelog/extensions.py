# -*- coding: utf-8 -*-
# @Time    : 2019-08-20 15:40
# @Author  : Xichagui
# @Site    :
# @File    : extensions.py
# @Software: PyCharm

from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

bootstrap = Bootstrap()
db = SQLAlchemy()
moment = Moment()
ckeditor = CKEditor()
mail = Mail()
