from crypt import methods
import functools, random, string
from sqlite3 import SQLITE_ALTER_TABLE
from datetime import datetime
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, abort
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import PostModel, UserModel
from flaskr.auth import login, login_required
#from flaskr.db import session as db_session
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
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
    posts = PostModel.query.filter(PostModel.author_id == g.user.id).all()
    return render_template('steno/splash.html', posts=posts)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    """Create a new post for the current user."""
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            post = PostModel(
            title=request.form['title'],
            body=request.form['body'],
            author_id=g.user.id,
            otp=generate_otp(8)
        )
            db.session.add(post)
            db.session.commit()
            return render_template('steno/splash.html')

    return render_template('steno/create.html')

def generate_otp(length):
    pool = string.ascii_letters + string.digits
    return ''.join(random.choice(pool) for i in range(length))

def updatereadtime(otp):
    """Whenever a message is read, we update its readtime."""
    readtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    fetchpost = PostModel.query.filter(PostModel.otp == otp).first()
    fetchpost.readtime = readtime
    db.session.commit()
    return(otp)

def get_post(otp):
    """Gets a post by its identifying otp value."""
    updatereadtime(otp)
    post = PostModel.query.filter(PostModel.otp == otp).first()
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
    """Delete a post."""
    get_post(otp)
    post = db.session.query(PostModel).filter(PostModel.otp == otp).first()
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for("steno.splash"))