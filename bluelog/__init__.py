# -*- coding: utf-8 -*-
# @Time    : 2019-08-20 13:52
# @Author  : Xichagui
# @Site    :
# @File    : __init__.py
# @Software: PyCharm
import logging
import os
from logging.handlers import RotatingFileHandler

from bluelog.blueprints.admin import admin_bp
from bluelog.blueprints.auth import auth_bp
from bluelog.blueprints.blog import blog_bp
from bluelog.commands import register_commands
from bluelog.extensions import (bootstrap, ckeditor, csrf, db, login_manager,
                                mail, moment, toolbar)
from bluelog.models import Category, Comment, User
from bluelog.settings import config
from flask import Flask, current_app, render_template
from flask_login import current_user
from flask_sqlalchemy import get_debug_queries
from flask_wtf.csrf import CSRFError


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
    register_request_handlers(app)
    return app


def register_logging(app):
    app.logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        '[%(asctime)s][%(name)s][%(levelname)s] -  %(message)s ')

    file_handler = RotatingFileHandler('logs/bluelog.log',
                                       maxBytes=10 * 1024 * 1024,
                                       backupCount=10)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    # if not app.debug:
    #     app.logger.addHandler(file_handler)
    app.logger.addHandler(file_handler)


def register_extensions(app):
    bootstrap.init_app(app)
    db.init_app(app)
    ckeditor.init_app(app)
    moment.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    toolbar.init_app(app)


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
        admin = User.query.first()
        categories = Category.query.order_by(Category.name).all()
        if current_user.is_authenticated:
            unread_comments = Comment.query.filter_by(reviewed=False).count()
        else:
            unread_comments = None
        return dict(admin=admin,
                    categories=categories,
                    unread_comments=unread_comments)


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

    @app.errorhandler(CSRFError)
    def handle_csrf_error(e):
        return render_template('errors/400.html',
                               description=e.description), 400


def register_request_handlers(app):
    @app.after_request
    def query_profiler(response):
        for q in get_debug_queries():
            if q.duration >= current_app.config['BLUELOG_SLOW_QUERY_THRESHOLD']:
                current_app.logger.warning(
                    f'Slow query: Duration :{q.duration}\nContext:{q.context}\nQuery: {q.statement}\n'
                )
        return response
