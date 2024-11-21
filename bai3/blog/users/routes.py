from flask import Blueprint
from flask import render_template,url_for,flash,redirect,request,Blueprint
from flask_login import login_user,current_user,logout_user,login_required
from blog import db,bcrypt
from blog.models import User, Post
from blog.users.forms import (RegistrationForm,LoginForm,UpdateAccountForm, RequestResetForm,ResetPasswordForm)
from blog.users.utils import save_picture,send_reset_email
users = Blueprint('users',__name__)

@users.route("/register",methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username = form.userName.data,email=form.email.data,password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Tài khoản {form.userName.data} đã tạo thành công! vui lòng đăng nhập','success')
        return redirect(url_for('users.login'))
    return render_template('register.html',title="Đăng ký",form=form)

@users.route("/login",methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user,remember=form.rememberMe.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        else:
            flash('Đăng nhập không thành công, kiểm tra lại tài khoản và mật khẩu','danger')
    return render_template('login.html',title="Đăng nhập",form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@users.route("/account",methods=['GET','POST'])
@login_required
def account():
    
    if not current_user.is_authenticated: 
        return redirect(url_for('login')) 
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.userName = form.userName.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Tài khoản của bạn đã được cập nhật','success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.userName.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static',filename='myAva/' + current_user.image_file)
    return render_template('account.html',title="Tài khoản",image_file=image_file, form=form)

@users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template("user_posts.html",posts=posts,user=user)


@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('Email đã được gửi qua Google vui lòng thực hiện theo để đổi mật khẩu.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)

@users.route("/reset_password/<token>",methods=['GET','POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('Token này đã hết hạn', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Mật khẩu của bạn đã được cập nhât, hãy đăng nhập ngay!', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)
