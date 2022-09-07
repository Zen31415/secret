"""."""
import os
from flask import Flask, request, g
from flaskr.auth import bp as auth_bp
from flaskr.steno import bp as steno
from flaskr.db import db as flaskr_db
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

application = Flask(__name__, static_folder='static', template_folder='templates')
application.config.from_mapping(
    SECRET_KEY='dev',
#    DATABASE=os.path.join(application.instance_path, 'flaskr.sqlite'),
    SQLALCHEMY_DATABASE_URI="postgresql://postgres:postgres@localhost:5432/secret",
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    #db = SQLAlchemy(application)
)
db = SQLAlchemy(application)
#migrate = Migrate(application, db)
application.register_blueprint(auth_bp)
application.register_blueprint(steno)

@application.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return "404 not found", 404

db.init_app(application)
flaskr_db.init_app(application)
with application.app_context():
    db.create_all()
    flaskr_db.create_all()


if __name__ == '__main__':
#    init_db_command()
    application.run(port=8000, host='0.0.0.0')
