# -*- coding: utf-8 -*-
# @Time    : 2019-09-18 20:08
# @Author  : Xichagui
# @Site    :
# @File    : decorators.py
# @Software: PyCharm

from functools import wraps

from markupsafe import Markup

from flask import flash, redirect, url_for
from flask_login import current_user


def confirm_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not current_user.confirmed:
            message = Markup(
                '请先到邮箱确认账户激活.'
                '没有收到确认邮件?'
                f'<a class="alert-link" href="{url_for("auth.resend_confirm_email")}">重新发送</a>'
            )
            flash(message, 'warning')
            return redirect(url_for('blog.index'))
        return func(*args, **kwargs)

    return decorated_function
