from flask import (
	Blueprint, flash, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from app.db import get_db

bp = Blueprint('blog', __name__)

@bp.route('/blog')
def index():
	db = get_db()
	posts = db.execute(
		'SELECT p.id, p.title, p.body, p.created, COUNT(c.id) as count'
		'	FROM post p LEFT JOIN comment c ON p.id = c.post_id'
		'	GROUP BY p.id'
		'	ORDER BY p.created DESC'
	).fetchall()
	return render_template('blog/index.html', posts=posts)
	
@bp.route('/blog/create', methods=('GET', 'POST'))
def create():
	if request.method == 'POST':
		title = request.form['title']
		body = request.form['body']
		error =  None
		
		if not title:
			error = 'Title is required.'
		
		if error is not None:
			flash(error)
		else:
			db = get_db()
			db.execute(
				'INSERT INTO post (title, body)'
				'	VALUES (?, ?)',
				(title, body)
			)
			db.commit()
			return redirect(url_for('blog.index'))
		
	return render_template('blog/create.html')
	
def get_post(id):
	post = get_db().execute(
		'SELECT id, title, body, created'
		'	FROM post'
		'	WHERE id = ?',
		(id,)
	).fetchone()
	
	if post is None:
		abort(404, "Post id {0} doesn't exist.".format(id))
		
	return post
	
@bp.route('/blog/<int:id>/update', methods=('GET', 'POST'))
def update(id):
	post = get_post(id)
	
	if request.method == 'POST':
		title = request.form['title']
		body = request.form['body']
		error = None
		
		if not title:
			error = 'Title is required.'
		
		if error is not None:
			flash(error)
		else:
			db = get_db()
			db.execute(
				'UPDATE post SET title = ?, body = ?'
				'	WHERE id = ?',
				(title, body, id)
			)
			db.commit()
			return redirect(url_for('blog.index'))
	return render_template('blog/update.html', post=post)
	
@bp.route('/blog/<int:id>/delete', methods=('POST',))
def delete(id):
	get_post(id)
	db = get_db()
	db.execute('DELETE FROM post WHERE id = ?', (id,))
	db.commit()
	return redirect(url_for('blog.index'))
	
@bp.route('/blog/<int:id>', methods=('GET', 'POST'))
def view(id):
	if request.method == 'POST':
		body = request.form['body']
		
		db = get_db()
		db.execute(
			'INSERT INTO comment (post_id, body)'
			'	VALUES (?, ?)',
			(id, body)
		)
		db.commit()
	
	post = get_post(id)
	comments = get_comments(id)
	
	return render_template('blog/view.html', post=post, comments=comments)
	
def get_comments(post_id):
	db = get_db()
	comments = db.execute(
		'SELECT c.id, c.created, c.body'
		'	FROM comment c JOIN post p ON c.post_id = p.id'
		'	WHERE p.id = ?'
		'	ORDER BY c.created ASC',
		(post_id,)
	).fetchall()
	return comments