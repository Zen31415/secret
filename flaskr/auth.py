import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import UserModel
from flask import session
from flaskr.db import session as db_session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError

bp = Blueprint('auth', __name__, url_prefix='/auth')

db = SQLAlchemy()

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        if not username:
            flash('Username is required.')
            return redirect(url_for("auth.login"))

        if not password:
            flash('Password is required.')
            return redirect(url_for("auth.login"))

        user = UserModel(
            username=request.form['username'],
            password=generate_password_hash(request.form['password'])
        )
        try:
            db_session.add(user)
            db_session.commit()
        except SQLAlchemyError as e:
            flash(str(e.__dict__['orig']))
            return redirect(url_for("auth.login"))

        flash('Registration successful')
        return redirect(url_for("auth.login"))

    elif request.method == 'GET':
        return render_template('auth/register.html')
    
@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for("steno.splash"))

        flash(error)

    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = UserModel.query.get(user_id).first()
        
                    #get_db().execute(
           # 'SELECT * FROM user WHERE id = ?', (user_id,)
        #).fetchone()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("steno.index"))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view