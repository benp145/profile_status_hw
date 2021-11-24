from os import stat
# from app import app, db
from . import bp as app
from app import db
from flask import render_template, url_for, redirect, request, flash
from datetime import date, datetime
from app.blueprints.auth.models import User
from app.blueprints.main.models import Post
from flask_login import login_user, logout_user, current_user

@app.route('/')
def home():

    context = {
        'first_name': 'Ben',
        'last_name': 'Peterson',
        'email': 'bp145@mail.com',
        'posts': Post.query.order_by(Post.date_created.desc()).all()
        # 'posts': [
        #     {
        #         'id': 1,
        #         'body': 'This is the first blog post',
        #         'date_created': datetime.utcnow()
        #     },
        #     {
        #         'id': 2,
        #         'body': 'This is the second blog post',
        #         'date_created': datetime.utcnow()
        #     },
        #     {
        #         'id': 3,
        #         'body': 'This is the third blog post',
        #         'date_created': datetime.utcnow()
        #     }
        # ]
    }
    return render_template('index.html', **context)

@app.route('/about')
def about():
    # data = {
    #     'first_name': 'Ben',
    #     'last_name': 'Peterson'
    # }
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    u = User.query.get(current_user.get_id())
    context = {
        'posts': Post.query.filter_by(user_id=u.get_id()).order_by(Post.date_created.desc()).all()
        # 'posts': Post.query.filter_by(user=u).all()
    }
    if request.method == 'POST':
        f_name = request.form.get('f_name')
        l_name = request.form.get('l_name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if not password and not confirm_password:
            u.first_name = f_name
            u.last_name = l_name
            u.email = email
            db.session.commit()
            flash('You have successfully updated your profile', 'info')
            return redirect(request.referrer)
        else:
            if password == confirm_password:
                u.first_name = f_name
                u.last_name = l_name
                u.email = email
                u.generate_password(password)
                db.session.commit()
                flash('You have successfully updated your profile', 'info')
                return redirect(request.referrer)
            else:
                flash('Your passwords do not match. try again', 'danger')
                return redirect(request.referrer)
            
    return render_template('profile.html', **context)

@app.route('/new_post', methods=['Post'])
def create_new_post():
    status = request.form.get('user_status')

    if status:
        p = Post(body=status, user_id=current_user.get_id())
        db.session.add(p)
        db.session.commit()
        flash('You have successfully created a new post.', 'success')
    else:
        flash('You cannot post nothing', 'danger')
    return redirect(url_for('main.home'))