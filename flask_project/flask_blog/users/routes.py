from flask import render_template,url_for,flash,redirect,request,Blueprint
from flask_login import login_user, current_user, logout_user,login_required
from flask_blog import db
from flask_blog.models import User,Post
from flask_blog.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                    RequestResetForm, ResetPasswordForm)
from flask_blog.users.utils import save_picture, send_reset_email
from flask_bcrypt import Bcrypt

users = Blueprint('users',__name__)
bcrypt = Bcrypt()
@users.route("/register", methods =['GET', 'POST'])
def register():
    # In case user has registered no need of register page,
    # so when user clicks register it redirects to home page
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form= RegistrationForm()
    if form.validate_on_submit():
        hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user=User(username=form.username.data,email=form.email.data,password=hashed_password)
        db.session.add(user)
        db.session.commit()
        #Easy method to send a one-time alert,second argument=category
        flash(f'Your Account has been created! You are now able to log in ', 'success')
        return redirect(url_for('main.home'))
    return render_template('register.html',title="Register",form=form)

@users.route("/login", methods =['GET', 'POST'])
def login():
    # In case user has logged in no need of login page,
    # so when user clicks login it redirects to home page
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        # Checks the credentials entered are correct or not
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('main.home'))

        else:
            flash('Login Unsuccessful. Please check username and password','danger')
    return render_template('login.html',title="Login",form=form)

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@users.route("/account", methods =['GET', 'POST'])
@login_required
def account():
    form=UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            # Updates the currrent profile picture with picture_file
            current_user.image_file = picture_file

        current_user.username=form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated','success')
        return redirect(url_for('users.account'))
    # This populates the form with old i.e. before updated data
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file=url_for('static',filename="profile_pics/"+current_user.image_file)
    return render_template('account.html',title='Account',
                           image_file=image_file,form=form)

# Route that shows all the posts of a particular user
@users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page',1,type=int)
    user = User.query.filter_by(username = username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page,per_page=2)
    return render_template('user_posts.html', posts=posts, user=user)

@users.route("/reset_password",methods=['GET','POST'])
def reset_request():
    # Check if user is logged out before resetting the password
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset the password','info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password',form=form)

@users.route("/reset_password/<token>",methods=['GET','POST'])
def reset_token(token):
    # Check if user is logged out before resetting the password
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    # print("hello")
    user = User.verify_reset_token(token)
    # print(user)
    if user is None:
        flash('That is an invalid or expired token','warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        #Easy method to send a one-time alert,second argument=category
        flash(f'Your password has been updated! You are now able to log in ', 'success')
        return redirect(url_for('users.login'))

    return render_template('reset_token.html', title='Reset Password',form=form)

