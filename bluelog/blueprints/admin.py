# -*- coding: utf-8 -*-
# @Time    : 2019-08-20 15:37
# @Author  : Xichagui
# @Site    :
# @File    : admin.py
# @Software: PyCharm

from bluelog.extensions import db
from bluelog.forms import SettingForm
from flask import Blueprint, flash, redirect, render_template, url_for, abort
from flask_login import current_user, login_required

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    form = SettingForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.blog_title = form.blog_title.data
        current_user.blog_sub_title = form.blog_sub_title.data
        current_user.about = form.about.data
        db.session.commit()
        flash('Setting updated.', 'success')
        return redirect(url_for('blog.index'))
    form.name.data = current_user.name
    form.blog_title.data = current_user.blog_title
    form.blog_sub_title.data = current_user.blog_sub_title
    form.about.data = current_user.about
    return render_template('admin/settings.html', form=form)


@admin_bp.route('/new_post')
def new_post():
    abort(404)


@admin_bp.route('/new_category')
def new_category():
    abort(404)


@admin_bp.route('/manager_post')
def manager_post():
    abort(404)


@admin_bp.route('/manager_category')
def manager_category():
    abort(404)


@admin_bp.route('/manager_comment')
def manager_comment():
    abort(404)

