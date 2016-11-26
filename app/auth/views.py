from flask import render_template, redirect, url_for, current_app, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from .. import db
from ..models import User
from ..email import send_email
from ..decorators import confirmed_required


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(login_name=request.form['login_name']).first()
        if user is not None and user.verify_password(request.form['password']):
            login_user(user)
            if user.login_name == 'meiling':
                return redirect(url_for('meiling.index'))
            return redirect(request.args.get('next') or url_for('main.index'))
        flash("无效的用户名或密码!")
    return render_template('auth/login.html')


@auth.route('/logout')
@login_required
@confirmed_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':

        if not request.form['email'].strip():
            flash("邮箱不能为空!")
            return render_template('auth/register.html', form=request.form)

        user = User.query.filter_by(email=request.form['email']).first()
        if user is not None:
            flash("此邮箱已被注册!")
            return render_template('auth/register.html', form=request.form)

        if not request.form['login_name'].strip():
            flash("登录名不能为空!")
            return render_template('auth/register.html', form=request.form)

        user = User.query.filter_by(login_name=request.form['login_name']).first()
        if user is not None:
            flash("此登录已被使用!")
            return render_template('auth/register.html', form=request.form)

        if not request.form['user_name'].strip():
            flash("昵称不能为空!")
            return render_template('auth/register.html', form=request.form)

        if not request.form['password'].strip():
            flash("密码不能为空!")
            return render_template('auth/register.html', form=request.form)

        new_user = User(email=request.form['email'],
                        login_name=request.form['login_name'],
                        user_name=request.form['user_name'],
                        password=request.form['password'])

        db.session.add(new_user)
        db.session.commit()
        token = new_user.generate_confirmation_token()
        send_email([request.form['email']], token=token)
        return redirect(url_for('auth.email_sent'))

    return render_template('auth/register.html', form=request.form)


@auth.route('/email_sent')
def email_sent():
    return render_template('auth/email_sent.html')


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        return render_template('auth/confirmed_success.html')
    return render_template('403.html')