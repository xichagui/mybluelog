# -*- coding: utf-8 -*-
# @Time    : 2019-08-20 14:06
# @Author  : Xichagui
# @Site    :
# @File    : auth.py
# @Software: PyCharm


from flask import Blueprint


auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login')
def login():
    pass


@auth_bp.route('/login')
def logout():
    pass
