# -*- coding: utf-8 -*-
"""
    :author: Dream Zhou (周梦雄)
    :url: https://heypython.cn
    :copyright: © 2020 Dream Zhou <zhoumengxiong@outlook.com>
    :license: MIT, see LICENSE for more details.
"""
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from . import whooshee


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)


@whooshee.register_model('order_number', 'approval_number', 'in_date', 'current_node')
class OrderModel(db.Model):
    __tablename__ = 'wos_flask'
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(15), nullable=False)
    approval_number = db.Column(db.String(12))
    product_category = db.Column(db.String(20), nullable=False)
    in_quantity = db.Column(db.Integer, nullable=False)
    in_date = db.Column(db.Date, nullable=False)
    in_operator = db.Column(db.String(10), nullable=False)
    receive_operator = db.Column(db.String(10), nullable=False)
    current_node = db.Column(db.String(10), nullable=False)
    chip_solution = db.Column(db.String(20), nullable=False)
    comment = db.Column(db.String(255))
