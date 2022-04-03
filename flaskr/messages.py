import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db
from flaskr.auth import login_required

bp = Blueprint('messages', __name__)

@bp.route('/messages')
def messages():
#    return 'testing'
    db = get_db()
    messages = db.execute(
        'SELECT p.id, owner_id, created, username, title, body, otp, read_time'
        ' FROM messages p JOIN user u ON p.owner_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('messages/messages.html', messages=messages)

@bp.route('/create', methods=('GET', 'MESSAGES'))
@login_required
def create():
    if request.method == 'MESSAGES':
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
                'INSERT INTO messages (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')

def get_messages(id, check_author=True):
    messages = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM messages p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if messages is None:
        abort(404, f"Message id {id} doesn't exist.")

    if check_author and messages['author_id'] != g.user['id']:
        abort(403)

    return messages
