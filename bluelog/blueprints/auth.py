# -*- coding: utf-8 -*-
# @Time    : 2019-08-20 14:06
# @Author  : Xichagui
# @Site    :
# @File    : auth.py
# @Software: PyCharm
from bluelog.email import send_confirm_account_email
from bluelog.extensions import db
from bluelog.forms import LoginForm, RegisterForm
from bluelog.models import User
from bluelog.utils import (Operations, generate_token, redirect_back,
                           validate_token)
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
        user = User.query.filter_by(username=username).first()
        if user:
            if user.validate_password(password):
                login_user(user, remember)
                flash('Welcome back.', 'info')
                return redirect_back()
            flash('Invalid username or password.', 'warning')
        else:
            flash('Invalid username or password.', 'warning')
    return render_template('auth/login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout success.', 'info')
    return redirect_back()


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('blog.index'))

    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    password=form.password.data,
                    blog_title=form.blog_title.data,
                    blog_sub_title=form.blog_sub_title.data,
                    email=form.email.data,
                    name=form.name.data,
                    about=form.about.data)
        db.session.add(user)
        db.session.commit()
        token = generate_token(user=user, operation=Operations.CONFIRM)
        send_confirm_account_email(user=user, token=token)
        flash('注册成功, 请到邮箱确认', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form=form)


@auth_bp.route('/confirm/<token>')
def confirm(token):
    validate_token(token, operation=Operations.CONFIRM)
    return render_template('auth/confirm.html', token=token)


@auth_bp.route('/resend-confirm-email')
@login_required
def resend_confirm_email():
    if not current_user.confirmed:
        token = generate_token(user=current_user, operation=Operations.CONFIRM)
        send_confirm_account_email(user=current_user, token=token)
        flash('已重新发送, 请到邮箱确认', 'info')
    return redirect(url_for('blog.index'))
