# -*- coding: utf-8 -*-
# @Time    : 2019-09-05 21:22
# @Author  : Xichagui
# @Site    :
# @File    : forms.py
# @Software: PyCharm

from bluelog.models import Category, User
from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from wtforms import (BooleanField, HiddenField, PasswordField, SelectField,
                     StringField, SubmitField, TextAreaField)
from wtforms.validators import (URL, DataRequired, Email, EqualTo, Length,
                                Optional, Regexp, ValidationError)


class LoginForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(),
                                       Length(1, 20)])
    password = PasswordField('Password',
                             validators=[DataRequired(),
                                         Length(8, 128)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Log in')


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(1, 60)])
    category = SelectField('Category', coerce=int, default=1)
    body = CKEditorField('Body', validators=[DataRequired()])
    submit = SubmitField()

    def __init__(self, *args, **kwargs):
        """
        Flask-SQLAlchemy依赖程序上下文, 所以要放到构造方法里调用, 获取分类
        """
        super(PostForm, self).__init__(
            *args, **kwargs)  # same as super().__init__(*args, **kwargs)
        self.category.choices = [
            (category.id, category.name)
            for category in Category.query.order_by(Category.name).all()
        ]


class CategoryForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(1, 30)])
    submit = SubmitField()

    def validate_name(self, field):
        if Category.query.filter_by(name=field.data).first():
            raise ValidationError('Name already is use.')


class CommentForm(FlaskForm):
    author = StringField('Author', validators=[DataRequired(), Length(1, 30)])
    email = StringField('Email',
                        validators=[DataRequired(),
                                    Email(),
                                    Length(1, 254)])
    site = StringField('Site', validators=[Optional(), URL(), Length(0, 255)])
    body = TextAreaField('Body', validators=[DataRequired()])
    submit = SubmitField()


class AdminCommentForm(CommentForm):
    author = HiddenField()
    email = HiddenField()
    site = HiddenField()


class SettingForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(1, 70)])
    blog_title = StringField('Blog Title',
                             validators=[DataRequired(),
                                         Length(1, 60)])
    blog_sub_title = StringField('Blog Sub Title',
                                 validators=[DataRequired(),
                                             Length(1, 100)])
    about = CKEditorField('About Page', validators=[DataRequired()])
    submit = SubmitField()


class RegisterForm(FlaskForm):
    username = StringField(
        'UserName',
        validators=[
            DataRequired(),
            Length(5, 18),
            Regexp(
                '^[a-zA-Z0-9]*$',
                message='Username should be contain only character or number.')
        ])
    password = PasswordField(
        'Password',
        validators=[DataRequired(),
                    Length(8, 20),
                    EqualTo('password2')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    blog_title = StringField('Blog title',
                             validators=[DataRequired(),
                                         Length(1, 60)])
    blog_sub_title = StringField('Blog sub title',
                                 validators=[DataRequired(),
                                             Length(0, 100)])
    name = StringField('Name', validators=[DataRequired(), Length(1, 30)])
    about = StringField('About', validators=[Length(0, 100)])
    email = StringField('Email',
                        validators=[DataRequired(),
                                    Length(1, 255),
                                    Email()])

    submit = SubmitField()

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('The username is already in use.')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('The email is already in use')
