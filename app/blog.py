import functools

from flask import (
	Blueprint, flash, g, redirect, render_template, request, url_for
)

from app.db import get_db

bp = Blueprint('blog', __name__, url_prefix='/blog')

@bp.route('/')
def index():
	db = get_db()
	posts = db.execute(
		'SELECT id, title, body, created'
		'	FROM post'
		'	ORDER BY created DESC'
	).fetchall()
	return render_template('blog/index.html', posts=posts)