# -*- coding: utf-8 -*-
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import DateField, IntegerField, SelectField, StringField, SubmitField, Form
from wtforms.validators import DataRequired, InputRequired
from watchlist import db
from watchlist import whooshee


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)


@whooshee.register_model('WoNumber', 'ApprovalNumber', 'InDate')
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


class wo_form(Form):
    WoNumber = StringField('派工单号：', validators=[DataRequired, InputRequired])
    ApprovalNumber = StringField('审批编号：', validators=[
                                 DataRequired, InputRequired], render_kw={'placeholder': '审批编号后6位'})
    ProductClass = SelectField('产品型态：', choices=[('单相表', '单相表'), ('13版三相表', '13版三相表'), ('13版集中器', '13版集中器'), (
        'I型采集器', 'I型采集器'), ('II型采集器', 'II型采集器'), ('抄控器', '抄控器'), ('09版三相表', '09版三相表'), ('09版集中器', '09版集中器')], validators=[
        DataRequired, InputRequired])
    InQuantity = IntegerField(
        '产出数量：', validators=[DataRequired, InputRequired])
    InDate = DateField('入库日期：', validators=[DataRequired, InputRequired])
    InOperator = StringField('入库员工：', validators=[DataRequired, InputRequired])
    ReceiveOperator = StringField(
        '接收员工：', validators=[DataRequired, InputRequired])
    CurrentNode = SelectField('当前节点：', choices=[('备料', '备料'), ('改造', '改造'), ('升级', '升级'), (
        '刻印', '刻印'), ('测试', '测试'), ('包装', '包装'), ('报检', '报检'), ('入库', '入库'), ('返工', '返工')], validators=[DataRequired, InputRequired])
    ChipSolution = SelectField('芯片方案：', choices=[('3105', '3105'), ('3911', '3911'), (
        'STKS_CCV1.31', 'STKS_CCV1.31')], validators=[DataRequired, InputRequired])
    Supplement = StringField('补充说明：', validators=[DataRequired, InputRequired])
    Add = SubmitField('新增')
