# -*- coding: utf-8 -*-
"""
    :author: Dream Zhou (周梦雄)
    :url: https://heypython.cn
    :copyright: © 2020 Dream Zhou <zhoumengxiong@outlook.com>
    :license: MIT, see LICENSE for more details.
"""
import os
# import sys

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_whooshee import Whooshee
from flask_wtf import CSRFProtect

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['WHOOSHEE_MIN_STRING_LEN'] = 1
# pythonanywhere部署时需要设置该值
app.config['SQLALCHEMY_POOL_RECYLE'] = 280

db = SQLAlchemy(app)
login_manager = LoginManager(app)
bootstrap = Bootstrap(app)
whooshee = Whooshee(app)
csrf = CSRFProtect(app)


@login_manager.user_loader
def load_user(user_id):
    from .models import User
    user = User.query.get(int(user_id))
    return user


login_manager.login_view = 'login'


# login_manager.login_message = 'Your custom message'


@app.context_processor
def inject_user():
    from .models import User
    user = User.query.first()
    return dict(user=user)


# from workorder import views, errors, commands只能放在最后一行
from . import views, errors, commands
