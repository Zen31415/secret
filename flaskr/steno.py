from crypt import methods
import functools, random, string

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, abort
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db
from flaskr.auth import login, login_required

bp = Blueprint('steno', __name__)

@bp.route('/')
def index():
    """Index page for users who are not logged in.
    Checks if user is logged in, and if yes redirects to splash.
    """
    if not session.get('user_id') is None:
        return render_template('steno/splash.html')
    else:
        return render_template('steno/index.html')

@bp.route('/splash')
@login_required
def splash():
    db = get_db()
    posts = db.execute(
        'SELECT p.title, body, created, author_id, username, otp'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('steno/splash.html', posts=posts)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    """Create a new post for the current user."""
    otp = None
    if request.method == 'POST':
        otp = generate_otp(otp)
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
                'INSERT INTO post (title, body, author_id, otp)'
                ' VALUES (?, ?, ?, ?)',
                (title, body, g.user['id'], otp)
            )
            db.commit()
            return redirect(url_for('steno.splash'))

    return render_template('steno/create.html')

def generate_otp(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(size))

def get_post(otp, check_author=True):
    """Get a post and its author by otp.
    Checks that the otp exists and optionally that the current user is
    the author.
    :param otp: otp of post to get
    :param check_author: require the current user to be the author
    :return: the post with author information
    :raise 404: if a post with the given id doesn't exist
    :raise 403: if the current user isn't the author
    """
    post = (
        get_db()
        .execute(
            "SELECT p.title, body, created, author_id, username, otp"
            " FROM post p JOIN user u ON p.author_id = u.id"
            " WHERE otp = ?",
            (otp,),
        )
        .fetchone()
    )

    if post is None:
        abort(404, f"Post id {otp} doesn't exist.")

    if check_author and post["author_id"] != g.user["id"]:
        abort(403)

    return post

@bp.route("/<string:otp>/view")
@login_required
def view(otp):
    """View a single post."""
    post = get_post(otp)
    return render_template('steno/view.html', post=post)

@bp.route("/<string:otp>/update", methods=("GET", "POST"))
@login_required
def update(otp):
    """Update a post if the current user is the author."""
    post = get_post(otp)

    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        error = None

        if not title:
            error = "Title is required."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "UPDATE post SET title = ?, body = ? WHERE id = ?", (title, body, id)
            )
            db.commit()
            return redirect(url_for("steno.index"))

    return render_template("steno/update.html", post=post)

@bp.route("/<string:otp>/delete", methods=("POST",))
@login_required
def delete(otp):
    """Delete a post.
    Ensures that the post exists and that the logged in user is the
    author of the post.
    """
    get_post(otp)
    db = get_db()
    db.execute("DELETE FROM post WHERE otp = ?", (otp,))
    db.commit()
    return redirect(url_for("steno.splash"))