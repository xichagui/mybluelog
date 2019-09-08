# -*- coding: utf-8 -*-
# @Time    : 2019-08-27 16:00
# @Author  : Xichagui
# @Site    :
# @File    : commands.py
# @Software: PyCharm

import click

from bluelog.extensions import db


def register_commands(app):
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop')
    def initdb(drop):
        if drop:
            click.confirm(
                'This operation will delete the database, do you want to continue?',
                abort=True)
            db.drop_all()
            click.echo('Drop tables.')
        db.create_all()
        click.echo('Initialized database.')

    @app.cli.command()
    @click.option('--category',
                  default=10,
                  help='Quantity of categories, default is 10.')
    @click.option('--post',
                  default=50,
                  help='Quantity of posts, default is 50.')
    @click.option('--comment',
                  default=500,
                  help='Quantity of comments, default is 500.')
    def forge(category, post, comment):
        """Generates the fake categories, posts, and comments"""
        from bluelog.fakes import fake_admin, fake_categories, fake_posts, fake_comments

        db.drop_all()
        db.create_all()

        click.echo('Generating the administrator...')
        fake_admin()

        click.echo(f'Generating {category} categories...')
        fake_categories(category)

        click.echo(f'Generating {post} posts...')
        fake_posts(post)

        click.echo(f'Generating {comment} comments...')
        fake_comments(comment)

        click.echo('Done.')
