from flask import Blueprint, render_template, request, flash, redirect, url_for, abort
from flask_login import login_required, current_user
from .models import Post
from . import db

views = Blueprint("views", __name__)

@views.route("/")
@views.route("/home")
@login_required
def home():
    posts = Post.query.all()
    return render_template("home.html", name=current_user.username, posts=posts)

@views.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!', category='error')
        else:
            post = Post(title = title, content = content, author = current_user.id)
            db.session.add(post)
            db.session.commit()
            flash('Post Created', category='success')
            return redirect(url_for('views.home'))
    
    return render_template('create.html')

@views.route('/terms', methods=('GET', 'POST'))
def terms():
      return render_template('terms.html')

@views.route('/<int:post_id>', methods=('GET', 'POST'))
def post(post_id):
    post = Post.query.filter_by(id=post_id).first()
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!', category='error')
        else:
            post.title = title
            post.content = content
            db.session.commit()
            flash('Post updated', category='success')
            return redirect(url_for('views.post', post_id=post.id))

    return render_template('post.html', post=post)

@views.route('/post/<int:post_id>/edit', methods=('GET', 'POST'))
@login_required
def edit(post_id):
    post = Post.query.get(post_id)
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!', category='error')
        else:
            post.title = title
            post.content = content
            db.session.commit()
            flash('Post updated', category='success')
            return redirect(url_for('views.home'))

    return render_template('edit.html', post=post)

@views.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)

    if not current_user.is_authenticated or post.author != current_user.id:
        abort(403)

    db.session.delete(post)
    db.session.commit()

    flash('Your post has been deleted!', 'success')
    return redirect(url_for('views.home'))
