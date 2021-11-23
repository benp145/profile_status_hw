from os import stat
# from app import app, db
from . import bp as app
from app import db
from flask import render_template, url_for, redirect, request, flash
from datetime import date, datetime
from app.blueprints.auth.models import User
from app.blueprints.main.models import Post
from flask_login import login_user, logout_user, current_user

@app.route('/<id>')
def post(id):
    current_post = None
    try:
        if id.isdigit():
            current_post = Post.query.get(id)

            if current_post == None:
                raise ValueError(f'Post {id} not found')
        else:
            raise ValueError(f'ID: {id} is not valid')
    except ValueError as e:
        flash(str(e), 'danger')
    context = {
        'post': current_post
    }
    return render_template('post.html', **context)
    # return "You're looking for post " + id