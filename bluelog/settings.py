# -*- coding: utf-8 -*-
# @Time    : 2019-08-20 13:52
# @Author  : Xichagui
# @Site    :
# @File    : settings.py
# @Software: PyCharm

import os


# 嵌套返回上层路径
# /Users/Cha/Developer/mybluelog
# /Users/Cha/Developer/mybluelog/bluelog
# /Users/Cha/Developer/mybluelog/bluelog/settings.py
basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


class BaseConfig(object):
    SECRET_KEY = os.getenv('SECRET_KEY', 'cha key')

    # Flask-SQLAlchemy 将会追踪对象的修改并且发送信号, 耗费内存, 可以关闭
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = ('Bluelog Admin', MAIL_USERNAME)

    BLUELOG_MAIL = os.getenv('BLUELOG_MAIL')
    BLUELOG_POST_PER_PAGE = 10
    BLUELOG_MANAGE_POST_PER_PAGE = 15
    BLUELOG_COMMENT_PER_PAGE = 15


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
        os.path.join(basedir, 'data-dev.db')


class TestingConfig(BaseConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory'  # in-memory database


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'sqlite:///' +
        os.path.join(
            basedir,
            'data.db'))


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
