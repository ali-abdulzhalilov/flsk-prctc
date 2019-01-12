from flask import (
	Blueprint, render_template
)

from app.db import get_db

bp = Blueprint('blog', __name__)

@bp.route('/blog')
def index():
	db = get_db()
	posts = db.execute(
		'SELECT id, title, body, created'
		'	FROM post'
		'	ORDER BY created DESC'
	).fetchall()
	return render_template('blog/index.html')