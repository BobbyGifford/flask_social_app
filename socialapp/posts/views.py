from flask import render_template, url_for, flash, request, Blueprint, redirect, abort
from flask_login import current_user, login_required
from socialapp import db
from socialapp.models import Post
from socialapp.posts.forms import PostForm

posts = Blueprint('posts', __name__)


# Create
@posts.route('/create', methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()

    if form.validate_on_submit():
        new_post = PostForm(title=form.title.data,
                            text=form.text.data,
                            user_id=current_user.id)
        db.session.add(new_post)
        db.session.commit()
        flash('Post created')
        return redirect(url_for('core.index'))

    return render_template('create_post.html', form=form)


# Read
@posts.route('/<int:post_id>')
def post(post_id):
    single_post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=single_post.title, date=single_post.date, post=single_post)


# Update
@posts.route('/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update(post_id):
    single_post = Post.query.get_or_404(post_id)
    if single_post.author != current_user:
        abort(403)

    form = PostForm()

    if form.validate_on_submit():
        single_post.title = form.title.data
        single_post.text = form.text.data
        db.session.commit()
        flash('Post updated')
        return redirect(url_for('posts.post', post_id=single_post.id))

    elif request.method == 'GET':
        form.title.data = single_post.title
        form.text.data = single_post.text
    return render_template('create_post.html', title='Updating', form=form)


# Delete
@posts.route('/<int:post_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    single_post = Post.query.get_or_404(post_id)

    if single_post.author != current_user:
        abort(403)

    db.session.delete(single_post)
    db.session.commit()
    flash("Post Deleted")
    return redirect(url_for('core.index'))
