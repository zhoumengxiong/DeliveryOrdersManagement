# -*- coding: utf-8 -*-
"""
    :author: Dream Zhou (周梦雄)
    :url: https://heypython.cn
    :copyright: © 2020 Dream Zhou <zhoumengxiong@outlook.com>
    :license: MIT, see LICENSE for more details.
"""
from flask import render_template, request, url_for, redirect, flash
from flask_login import login_user, login_required, logout_user, current_user

from . import app, db
from .models import User, OrderModel
from .forms import OrderForm
from sqlalchemy import or_, and_


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if not current_user.is_authenticated:
            return redirect(url_for('index'))

        order_number = request.form['order_number'].strip().upper()
        approval_number = request.form['approval_number'].strip()
        product_category = request.form['product_category']
        in_quantity = request.form['in_quantity']
        in_date = request.form['in_date']
        in_operator = request.form['in_operator'].strip()
        receive_operator = request.form['receive_operator'].strip()
        current_node = request.form['current_node']
        chip_solution = request.form['chip_solution']
        comment = request.form['comment'].strip()

        if not order_number or not product_category or not in_quantity or not in_date or not current_node or \
                not chip_solution:
            flash('Invalid input.', 'warning')
            return redirect(url_for('index'))
        if OrderModel.query.filter(
                and_(OrderModel.order_number.contains(order_number),
                     OrderModel.product_category.contains(product_category),
                     OrderModel.chip_solution.contains(chip_solution))).all():
            flash('数据库已存在该条记录，新增失败！', 'warning')
        else:
            order = OrderModel(order_number=order_number, approval_number=approval_number,
                               product_category=product_category,
                               in_quantity=in_quantity, in_date=in_date,
                               in_operator=in_operator, receive_operator=receive_operator, current_node=current_node,
                               chip_solution=chip_solution, comment=comment)
            db.session.add(order)
            db.session.commit()
            flash('Item created.', 'info')
            return redirect(url_for('index'))

    # orders = OrderModel.query.order_by(OrderModel.in_date.desc()).all()
    page = request.args.get('page', 1, type=int)
    per_page = 15
    pagination = OrderModel.query.order_by(
        OrderModel.in_date.desc()).paginate(page, per_page=per_page)
    orders = pagination.items
    form = OrderForm()
    return render_template('index.html', orders=orders, pagination=pagination, form=form)


@app.route('/order/edit/<int:order_id>', methods=['GET', 'POST'])
@login_required
def edit(order_id):
    order = OrderModel.query.get_or_404(order_id)

    if request.method == 'POST':
        order_number = request.form['order_number'].strip().upper()
        approval_number = request.form.get('approval_number').strip()
        product_category = request.form.get('product_category')
        in_quantity = request.form.get('in_quantity')
        in_date = request.form.get('in_date')
        in_operator = request.form.get('in_operator').strip()
        receive_operator = request.form.get('receive_operator').strip()
        current_node = request.form.get('current_node')
        chip_solution = request.form.get('chip_solution')
        comment = request.form.get('comment').strip()

        if not order_number or not product_category or not in_quantity or not in_date or not current_node or not \
                chip_solution:
            flash('Invalid input.', 'warning')
            return redirect(url_for('index'))
        order.order_number = order_number
        order.approval_number = approval_number
        order.product_category = product_category
        order.in_quantity = in_quantity
        order.in_date = in_date
        order.in_operator = in_operator
        order.receive_operator = receive_operator
        order.current_node = current_node
        order.chip_solution = chip_solution
        order.comment = comment
        db.session.commit()
        flash('Item updated.', 'info')
        return redirect(url_for('index'))

    return render_template('edit.html', order=order, title="修改")


@app.route('/order/delete/<int:order_id>', methods=['POST'])
@login_required
def delete(order_id):
    order = OrderModel.query.get_or_404(order_id)
    db.session.delete(order)
    db.session.commit()
    flash('Item deleted.', 'info')
    return redirect(url_for('index'))


@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        name = request.form['name']

        if not name or len(name) > 20:
            flash('Invalid input.', 'warning')
            return redirect(url_for('settings'))

        user = User.query.first()
        user.name = name
        db.session.commit()
        flash('Settings updated.', 'info')
        return redirect(url_for('index'))

    return render_template('settings.html', title="设置用户名")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Invalid input.', 'warning')
            return redirect(url_for('login'))

        user = User.query.first()

        if username == user.username and user.validate_password(password):
            login_user(user)
            flash('Login success.', 'info')
            return redirect(url_for('index'))

        flash('Invalid username or password.', 'warning')
        return redirect(url_for('login'))

    return render_template('login.html', title="登录")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Goodbye.', 'info')
    return redirect(url_for('index'))


@app.route('/search')
def search():
    page = request.args.get('page', 1, type=int)
    per_page = 20
    qu = request.args.get('q').strip()
    # pagination = OrderModel.query.whooshee_search(qu).paginate(page, per_page=per_page)
    pagination = OrderModel.query.filter(
        or_(OrderModel.order_number.contains(qu), OrderModel.approval_number.contains(qu),
            OrderModel.in_date.contains(qu))).order_by(OrderModel.in_date.desc()).paginate(page, per_page=per_page)
    orders = pagination.items
    if not orders:
        flash('未有满足该搜索条件的记录！', 'danger')
        return redirect(url_for('index'))
    return render_template('search.html', orders=orders, pagination=pagination, keyword=qu, title="查询")


@app.route('/summary_qty', methods=['GET', 'POST'])
@login_required
def summary_qty():
    qty_orders = 0
    qty_modules = 0
    if request.method == 'POST':
        start_date = str(request.form['start_date'])
        end_date = str(request.form['end_date'])
        query_by_date = OrderModel.query.filter(
            and_(OrderModel.in_date >= start_date, OrderModel.in_date <= end_date)).all()
        qty_modules = sum([x.in_quantity for x in query_by_date])
        qty_orders = len(set([y.order_number for y in query_by_date]))
    return render_template('summary_qty.html', qty_orders=qty_orders,
                           qty_modules=qty_modules, title="统计")
