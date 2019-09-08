# -*- coding: utf-8 -*-
# @Time    : 2019-08-20 14:06
# @Author  : Xichagui
# @Site    :
# @File    : auth.py
# @Software: PyCharm

from bluelog.forms import LoginForm
from bluelog.models import Admin
from bluelog.utils import redirect_back
from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required, login_user, logout_user

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('blog.index'))

    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember.data
        admin = Admin.query.first()  # 单管理员
        if admin:
            if username == admin.username and admin.validate_password(
                    password):
                login_user(admin, remember)
                flash('Welcome back.', 'info')
                return redirect_back()
            flash('Invalid username or password.', 'warning')
        else:
            flash('No account.', 'warning')
    return render_template('auth/login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout success.', 'info')
    return redirect_back()
