from flask import Blueprint, render_template, request, redirect, url_for, flash
from kardash_plus_inventory.forms import UserLoginForm
from kardash_plus_inventory.models import User, db
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, login_required 


auth = Blueprint('auth', __name__, template_folder = 'auth_templates')

@auth.route('/signup', methods = ['GET', 'POST']) #always going to be a list and you know what they say, "always be methods"
def signup(): 
    form = UserLoginForm()
    try:
        if request.method == "POST" and form.validate_on_submit(): #method coming from our forms.html
            email = form.email.data 
            first_name = form.first_name.data
            last_name = form.last_name.data
            password = form.password.data
            #These pieces are what takes information and plugs it into our databases
            #instantiate a user and plug in information 
            user = User(email, first_name, last_name, password = password)

            db.session.add(user)
            db.session.commit()

            flash(f'You have successfully created a user account {email}', 'user-created')
            
            return redirect(url_for("auth.signin"))
    except: 
        raise Exception('Invalid Form Data: Please Check Your Form')

    return render_template('signup.html', form = form) # form = form --> passing our instantiated form into our template

@auth.route('/signin', methods = ['GET', 'POST'])
def signin():
    form = UserLoginForm()

    try:
        if request.method == "POST" and form.validate_on_submit():
            email = form.email.data 
            password = form.password.data
            print(email, password)

            logged_user = User.query.filter(User.email == email).first() #if this exists and 
            if logged_user and check_password_hash(logged_user.password, password): #check a password against this and if it matches and then we'll do an import (wut)
                login_user(logged_user)
                flash('You were successfully logged in via email/password', 'auth-success') 
                return redirect(url_for('site.profile')) #we'll use that information if that passes
            else: 
                flash('Your email or password is invalid.', 'auth-failed')
                return redirect(url_for('auth.signin'))  #if it fails we'll go back to where we started from
    except:
        raise Exception('Invalid Form Data: Please Try Again, doggy doggerson!')


    return render_template('signin.html', form = form)

@auth.route('/logout')
@login_required #protecting information we don't want unauthenticated users to see (ie facebook users can see more than nonusers)
def logout():
    logout_user()
    return redirect(url_for('site.home'))