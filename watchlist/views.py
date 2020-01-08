# -*- coding: utf-8 -*-
from flask import render_template, request, url_for, redirect, flash
from flask_login import login_user, login_required, logout_user, current_user

from watchlist import app, db
from watchlist.models import User, Wos_flask, wo_form
from sqlalchemy import or_, and_


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if not current_user.is_authenticated:
            return redirect(url_for('index'))

        WoNumber = request.form['WoNumber']
        ApprovalNumber = request.form['ApprovalNumber']
        ProductClass = request.form['ProductClass']
        InQuantity = request.form['InQuantity']
        InDate = request.form['InDate']
        InOperator = request.form['InOperator']
        ReceiveOperator = request.form['ReceiveOperator']
        CurrentNode = request.form['CurrentNode']
        ChipSolution = request.form['ChipSolution']
        Supplement = request.form['Supplement']

        if not WoNumber or not ProductClass or not InQuantity or not InDate or not CurrentNode or not ChipSolution:
            flash('Invalid input.')
            return redirect(url_for('index'))
        if Wos_flask.query.filter(
                and_(Wos_flask.WoNumber.contains(WoNumber), Wos_flask.ProductClass.contains(ProductClass), Wos_flask.ChipSolution.contains(ChipSolution))).all():
            flash('数据库已存在该条记录，新增失败！')
        else:
            movie = Wos_flask(WoNumber=WoNumber, ApprovalNumber=ApprovalNumber, ProductClass=ProductClass, InQuantity=InQuantity, InDate=InDate,
                              InOperator=InOperator, ReceiveOperator=ReceiveOperator, CurrentNode=CurrentNode, ChipSolution=ChipSolution, Supplement=Supplement)
            db.session.add(movie)
            db.session.commit()
            flash('Item created.')
            return redirect(url_for('index'))

    # movies = Wos_flask.query.order_by(Wos_flask.InDate.desc()).all()
    page = request.args.get('page', 1, type=int)
    per_page = 20
    pagination = Wos_flask.query.order_by(
        Wos_flask.InDate.desc()).paginate(page, per_page=per_page)
    movies = pagination.items
    form = wo_form()
    return render_template('index.html', movies=movies, pagination=pagination, form=form)


@app.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
@login_required
def edit(movie_id):
    movie = Wos_flask.query.get_or_404(movie_id)

    if request.method == 'POST':
        """WoNumber = request.form['WoNumber']
        ApprovalNumber = request.form['ApprovalNumber']
        ProductClass = request.form['ProductClass']
        InQuantity = request.form['InQuantity']
        InDate = request.form['InDate']
        InOperator = request.form['InOperator']
        ReceiveOperator = request.form['ReceiveOperator']
        CurrentNode = request.form['CurrentNode']
        ChipSolution = request.form['ChipSolution']
        Supplement = request.form['Supplement']"""
        WoNumber = request.form['WoNumber']
        ApprovalNumber = request.form.get('ApprovalNumber')
        ProductClass = request.form.get('ProductClass')
        InQuantity = request.form.get('InQuantity')
        InDate = request.form.get('InDate')
        InOperator = request.form.get('InOperator')
        ReceiveOperator = request.form.get('ReceiveOperator')
        CurrentNode = request.form.get('CurrentNode')
        ChipSolution = request.form.get('ChipSolution')
        Supplement = request.form.get('Supplement')

        if not WoNumber or not ProductClass or not InQuantity or not InDate or not CurrentNode or not ChipSolution:
            flash('Invalid input.')
            return redirect(url_for('index'))
        movie.WoNumber = WoNumber
        movie.ApprovalNumber = ApprovalNumber
        movie.ProductClass = ProductClass
        movie.InQuantity = InQuantity
        movie.InDate = InDate
        movie.InOperator = InOperator
        movie.ReceiveOperator = ReceiveOperator
        movie.CurrentNode = CurrentNode
        movie.ChipSolution = ChipSolution
        movie.Supplement = Supplement
        db.session.commit()
        flash('Item updated.')
        return redirect(url_for('index'))

    return render_template('edit.html', movie=movie)


@app.route('/movie/delete/<int:movie_id>', methods=['POST'])
@login_required
def delete(movie_id):
    movie = Wos_flask.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash('Item deleted.')
    return redirect(url_for('index'))


@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        name = request.form['name']

        if not name or len(name) > 20:
            flash('Invalid input.')
            return redirect(url_for('settings'))

        user = User.query.first()
        user.name = name
        db.session.commit()
        flash('Settings updated.')
        return redirect(url_for('index'))

    return render_template('settings.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Invalid input.')
            return redirect(url_for('login'))

        user = User.query.first()

        if username == user.username and user.validate_password(password):
            login_user(user)
            flash('Login success.')
            return redirect(url_for('index'))

        flash('Invalid username or password.')
        return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Goodbye.')
    return redirect(url_for('index'))


@app.route('/search')
def search():
    page = request.args.get('page', 1, type=int)
    per_page = 20
    qu = request.args.get('q').strip()
    """pagination = Wos_flask.query.whooshee_search(qu).paginate(page, per_page=per_page)"""
    pagination = Wos_flask.query.filter(
        or_(Wos_flask.WoNumber.contains(qu), Wos_flask.ApprovalNumber.contains(qu), Wos_flask.InDate.contains(qu))).order_by(Wos_flask.InDate.desc()).paginate(page, per_page=per_page)
    movies = pagination.items
    return render_template('search.html', movies=movies, pagination=pagination, keyword=qu)


@app.route('/summary_qty', methods=['GET', 'POST'])
@login_required
def summary_qty():
    qty_orders = 0
    qty_modules = 0
    if request.method == 'POST':
        start_date = str(request.form['start_date'])
        end_date = str(request.form['end_date'])
        query_by_date = Wos_flask.query.filter(
            and_(Wos_flask.InDate >= start_date, Wos_flask.InDate <= end_date)).all()
        qty_modules = sum([x.InQuantity for x in query_by_date])
        qty_orders = len(set([y.WoNumber for y in query_by_date]))
    return render_template('summary_qty.html', qty_orders=qty_orders,
                           qty_modules=qty_modules)
