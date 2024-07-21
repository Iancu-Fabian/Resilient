from flask import Blueprint,redirect, url_for
from flask import render_template, request, flash
from .models import User
from passlib.hash import bcrypt
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint("auth", __name__ )

@auth.route('/login', methods= ['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if bcrypt.verify(password, user.password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                print("merge")
                return render_template("home.html", user=current_user)
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')
            
    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign_up', methods= ['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists', category='error')
            return render_template("sign_up.html", user=current_user)

        if len(email) < 4:
            flash('Email must be greater than 4 characters.', category='error')
        elif len (name) <2:
            flash('First name must be greater than 2 characters.', category='error')
        elif password1 != password2:
            flash('Passwords must match.', category='error')
        elif len(password1) < 7:
            flash('Password must be greater than 7 characters.', category='error')
        else:
            new_user = User(email=email, first_name=name, password=bcrypt.hash(password1))
            db.session.add(new_user)
            db.session.commit()
            flash('Account created!', category='success')
            login_user(new_user, remember=True)
            return redirect(url_for('routes.home'))
    return render_template("sign_up.html", user=current_user)