# -*- coding: utf-8 -*-
# @Time    : 2019-08-20 13:52
# @Author  : Xichagui
# @Site    :
# @File    : __init__.py
# @Software: PyCharm

import os

from bluelog.blueprints.admin import admin_bp
from bluelog.blueprints.auth import auth_bp
from bluelog.blueprints.blog import blog_bp
from bluelog.commands import register_commands
from bluelog.extensions import (bootstrap, ckeditor, db, login_manager, mail,
                                moment)
from bluelog.models import Admin, Category
from bluelog.settings import config
from flask import Flask, render_template


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('bluelog')
    app.config.from_object(config[config_name])
    register_extensions(app)
    register_blueprint(app)
    register_commands(app)
    register_errors(app)
    register_logging(app)
    register_shell_context(app)
    register_template_context(app)
    return app


def register_logging(app):
    pass


def register_extensions(app):
    bootstrap.init_app(app)
    db.init_app(app)
    ckeditor.init_app(app)
    moment.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)


def register_blueprint(app):
    app.register_blueprint(blog_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')


def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db)


def register_template_context(app):
    @app.context_processor
    def make_template_context():
        admin = Admin.query.first()
        categories = Category.query.order_by(Category.name).all()
        return dict(admin=admin, categories=categories)


def register_errors(app):
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('errors/400.html'), 400

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500
