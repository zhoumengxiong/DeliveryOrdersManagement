from wtforms import DateField, IntegerField, SelectField, StringField, SubmitField, Form
from wtforms.validators import DataRequired, InputRequired


class OrderForm(Form):
    WoNumber = StringField("派工单号：", validators=[DataRequired(), InputRequired()])
    ApprovalNumber = StringField(
        "审批编号：",
        validators=[DataRequired(), InputRequired()],
        render_kw={"placeholder": "审批编号后6位"},
    )
    ProductClass = SelectField(
        "产品型态：",
        choices=[
            ("单相表", "单相表"),
            ("13版三相表", "13版三相表"),
            ("13版集中器", "13版集中器"),
            ("I型采集器", "I型采集器"),
            ("II型采集器", "II型采集器"),
            ("抄控器", "抄控器"),
            ("09版三相表", "09版三相表"),
            ("09版集中器", "09版集中器"),
        ],
        validators=[DataRequired(), InputRequired()],
    )
    InQuantity = IntegerField("产出数量：", validators=[DataRequired(), InputRequired()])
    InDate = DateField("入库日期：", validators=[DataRequired(), InputRequired()])
    InOperator = StringField("入库员工：", validators=[DataRequired(), InputRequired()])
    ReceiveOperator = StringField("接收员工：", validators=[DataRequired(), InputRequired()])
    CurrentNode = SelectField(
        "当前节点：",
        choices=[
            ("备料", "备料"),
            ("改造", "改造"),
            ("升级", "升级"),
            ("刻印", "刻印"),
            ("测试", "测试"),
            ("包装", "包装"),
            ("报检", "报检"),
            ("入库", "入库"),
            ("返工", "返工"),
        ],
        validators=[DataRequired(), InputRequired()],
    )
    ChipSolution = SelectField(
        "芯片方案：",
        choices=[("3105", "3105"), ("3911", "3911"), ("STKS_CCV1.31", "STKS_CCV1.31")],
        validators=[DataRequired(), InputRequired()],
    )
    Supplement = StringField("补充说明：", validators=[DataRequired(), InputRequired()])
    Add = SubmitField("新增")
