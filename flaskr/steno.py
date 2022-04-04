import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db
from flaskr.auth import login_required

bp = Blueprint('steno', __name__)

@bp.route('/')
def index():
    return render_template('steno/index.html')

@bp.route('/splash')
@login_required
def splash():
    db = get_db()
    steno = db.execute(
        'SELECT p.id, title, body, created, owner_id, username'
        ' FROM steno p JOIN user u ON p.owner_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('steno/splash.html', steno=steno)


@bp.route('/messages')
def messages():
    db = get_db()
    steno = db.execute(
        'SELECT p.id, owner_id, created, username, title, body, otp, read_time'
        ' FROM steno p JOIN user u ON p.owner_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('steno/messages.html', steno=steno)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
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
                'INSERT INTO steno (title, body, owner_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('steno.index'))

    return render_template('steno/create.html')

def get_steno(id, check_author=True):
    steno = get_db().execute(
        'SELECT p.id, title, body, created, owner_id, username'
        ' FROM steno p JOIN user u ON p.owner_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if steno is None:
        abort(404, f"Message id {id} doesn't exist.")

    if check_author and steno['owner_id'] != g.user['id']:
        abort(403)

    return steno
