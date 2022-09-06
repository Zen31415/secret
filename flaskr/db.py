from email.mime import application
import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func

engine = create_engine(
    'postgresql://postgres:postgres@localhost:5432/secret',
    echo=True
)
Session = sessionmaker(bind=engine)
session = Session()

db = SQLAlchemy()
class UserModel(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(40), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return f"<User {self.id}, Username {self.username}>"

class PostModel(db.Model):
    __tablename__ = 'post'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created = db.Column(db.DateTime(timezone=False), nullable=False, default=func.now())
    title = db.Column(db.String(), nullable=False)
    body = db.Column(db.Text(), nullable=False)
    readtime = db.Column(db.DateTime(timezone=False), nullable=True, default=None)
    otp = db.Column(db.String(8), nullable=True, default=None)

    def __init__(self, id, author_id, created, title, body, readtime, otp):
        self.id = id
        self.author_id = author_id
        self.created = created
        self.title = title
        self.body = body
        self.readtime = readtime
        self.otp = otp

    def __repr__(self):
        return f"<Post: {self.id}, Author: {self.author_id}>"


def get_db():
    """Connect to the application's configured database. The connection
    is unique for each request and will be reused if this is called
    again.
    """
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'], detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    """If this request connected to the database, close the
    connection.
    """
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    """Clear existing data and create new tables."""
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    """Register database functions with the Flask app. This is called by
    the application factory.
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)