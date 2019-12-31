# -*- coding: utf-8 -*-
from flask import render_template, request, url_for, redirect, flash
from flask_login import login_user, login_required, logout_user, current_user

from watchlist import app, db
from watchlist.models import User, Wos_flask,wo_form


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
    form=wo_form()
    return render_template('index.html', movies=movies,pagination=pagination,form=form)


@app.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
@login_required
def edit(movie_id):
    movie = Wos_flask.query.get_or_404(movie_id)

    if request.method == 'POST':
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

        movie = Wos_flask(WoNumber=WoNumber, ApprovalNumber=ApprovalNumber, ProductClass=ProductClass, InQuantity=InQuantity, InDate=InDate,
                          InOperator=InOperator, ReceiveOperator=ReceiveOperator, CurrentNode=CurrentNode, ChipSolution=ChipSolution, Supplement=Supplement)
        db.session.add(movie)
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
