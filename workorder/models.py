# -*- coding: utf-8 -*-
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


@whooshee.register_model('WoNumber', 'ApprovalNumber', 'InDate','CurrentNode')
class Wos_flask(db.Model):
    __tablename__ = 'wos_flask'
    Id = db.Column(db.Integer, primary_key=True)
    WoNumber = db.Column(db.String(15), nullable=False)
    ApprovalNumber = db.Column(db.String(12))
    ProductClass = db.Column(db.String(20), nullable=False)
    InQuantity = db.Column(db.Integer, nullable=False)
    InDate = db.Column(db.Date, nullable=False)
    InOperator = db.Column(db.String(10), nullable=False)
    ReceiveOperator = db.Column(db.String(10), nullable=False)
    CurrentNode = db.Column(db.String(10), nullable=False)
    ChipSolution = db.Column(db.String(20), nullable=False)
    Supplement = db.Column(db.String(255))
