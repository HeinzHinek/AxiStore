# -*- coding: utf-8 -*-

from flask import redirect, url_for, flash, request, render_template, g
from app import app
from forms import LoginForm
from models import User
from flask_login import login_user, logout_user
from flask.ext.babel import gettext


@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        #session['remember_me'] = form.remember_me.data
        nickname = form.nickname.data
        password = form.password.data
        user = User.query.filter_by(nickname=nickname, password=password).first()
        if user is None:
            flash(gettext('Username or Password is invalid'), 'error')
            return redirect(url_for('login'))
        login_user(user)
        flash(gettext("Logged in successfully."))
        return redirect(request.args.get("next") or url_for("index"))
    return render_template('login/login.html',
                           title=gettext('Sign In'),
                           form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))